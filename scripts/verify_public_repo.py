"""Publication gate for this small repository. Heuristics do not replace review."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".txt", ".json", ".py", ".html", ".svg"}
CREDENTIAL = re.compile(
    r"\b(?:sk" + r"-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})"
    r"|Bearer\s+[A-Za-z0-9._~+/=-]{12,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|(?:api[_-]?key|secret|access[_-]?token|password)\s*[\"']?\s*[:=]\s*[\"'][^\"'\s]{8,}",
    re.I,
)
EMAIL = re.compile(r"[\w.+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
ABSOLUTE = re.compile(
    r"/(?:Us" + r"ers|home|private|var|tmp)/[^\s\"'<>]+|[A-Z]:\\(?:Users|Documents)\\", re.I
)
PRIVATE_TEXT = re.compile(
    r"\bClients" + r"/|\b(?:OUTREACH_LOG|QUESTION_LOG)\.csv\b"
    r"|MOVENLEARN_INTERNAL_" + "SYSTEM_AUDIT"
    r"|(?:mongodb(?:\+srv)?|postgres(?:ql)?)://", re.I
)
PHONE = re.compile(r"(?<!\w)\+[1-9][0-9 ()-]{8,}[0-9]")
PRIVATE_NAMES = {".e" + "nv", "clients", "credentials", "cookies.txt"}
CACHE_DIRS = {".git", "__pycache__"}
DUMMY_DOMAINS = {"example.invalid", "example.com", "example.org", "example.net"}


def scan_text(text):
    findings = []
    for label, rule in [("credential-like text", CREDENTIAL), ("local absolute path", ABSOLUTE),
                        ("private material", PRIVATE_TEXT), ("phone-like text", PHONE)]:
        if rule.search(text):
            findings.append(label)
    if any(match[1].lower() not in DUMMY_DOMAINS for match in EMAIL.finditer(text)):
        findings.append("non-demo email address")
    if re.search(r"\." + "env" + r"(?:\.[A-Za-z0-9_-]+)?", text):
        findings.append("environment-file reference")
    return findings


def extract_pdf(data):
    for command in ("pdfinfo", "pdftotext", "pdfdetach"):
        if not shutil.which(command):
            raise ValueError("Install Poppler for PDF publication checks")
    with tempfile.TemporaryDirectory(prefix="showcase-pdf-scan-") as temp:
        path = Path(temp) / "artifact.pdf"
        path.write_bytes(data)
        info = subprocess.check_output(["pdfinfo", str(path)], stderr=subprocess.PIPE).decode()
        if re.search(r"Encrypted:\s+yes", info):
            raise ValueError("Encrypted PDF is not permitted")
        attachments = subprocess.check_output(["pdfdetach", "-list", str(path)], stderr=subprocess.PIPE).decode()
        if not re.match(r"0 embedded files", attachments):
            raise ValueError("PDF attachments are not permitted")
        text = subprocess.check_output(["pdftotext", str(path), "-"], stderr=subprocess.PIPE).decode()
        metadata = subprocess.check_output(["pdfinfo", "-meta", str(path)], stderr=subprocess.PIPE).decode()
    if re.search(rb"/(?:JavaScript|EmbeddedFile|Launch|SubmitForm|AcroForm)\b", data):
        raise ValueError("Interactive or embedded PDF content is not permitted")
    streams = []
    for stream in re.findall(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        try:
            streams.append(zlib.decompress(stream).decode("utf-8", errors="ignore"))
        except zlib.error:
            pass
    return "\n".join([info, text, metadata] + streams)


def png_metadata(data):
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Invalid PNG")
    pos = 8
    while pos + 12 <= len(data):
        size = struct.unpack(">I", data[pos:pos+4])[0]
        kind = data[pos+4:pos+8]
        if pos+12+size > len(data):
            raise ValueError("Malformed PNG chunk")
        if kind in (b"tEXt", b"iTXt", b"zTXt", b"eXIf"):
            raise ValueError("PNG metadata must be removed before publication")
        pos += 12 + size
        if kind == b"IEND":
            if pos != len(data):
                raise ValueError("Unexpected trailing PNG data")
            return ""
    raise ValueError("PNG has no valid end chunk")


def scan_blob(name, data, manifest):
    path = Path(name)
    lowered = [part.lower() for part in path.parts]
    if any(part in PRIVATE_NAMES or part.startswith(".e" + "nv.") for part in lowered):
        return ["private filename"]
    if any(part in ("clients", ".venv", "node_modules") for part in lowered):
        return ["unexpected private or dependency directory"]
    font = manifest.get(path.name) if path.parent.as_posix() == "assets/fonts" else None
    if font:
        if hashlib.sha256(data).hexdigest() != font["sha256"]:
            return ["upstream font/license checksum mismatch"]
        return []
    try:
        if path.suffix == ".pdf":
            return scan_text(extract_pdf(data))
        if path.suffix == ".png":
            return scan_text(png_metadata(data))
        if path.suffix not in TEXT_SUFFIXES and path.name not in ("LICENSE", ".gitignore"):
            return ["unapproved file format"]
        text = data.decode("utf-8")
    except (UnicodeError, ValueError, subprocess.SubprocessError) as error:
        return ["uninspectable artifact: " + type(error).__name__]
    hits = scan_text(text)
    if path.name == ".gitignore":
        hits = [hit for hit in hits if hit != "environment-file reference"]
    if path.suffix in (".html", ".svg") and re.search(r"<script\b|onload=|javascript:|<foreignObject", text, re.I):
        hits.append("active content in static artifact")
    if path.suffix == ".svg" and re.search(r'(?:href|src)=["\'](?:https?:|file:|data:)', text):
        hits.append("external SVG dependency")
    return hits


def audit(root, history=True):
    manifest_path = root / "assets/fonts/manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    failures, scanned = [], 0
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in CACHE_DIRS for part in relative.parts):
            continue
        if path.is_symlink():
            failures.append((relative.as_posix(), ["symlink is not permitted"]))
        elif path.is_file():
            scanned += 1
            hits = scan_blob(relative.as_posix(), path.read_bytes(), manifest)
            if hits:
                failures.append((relative.as_posix(), hits))
    blobs = 0
    if history and (root / ".git").exists():
        run = lambda *args: subprocess.check_output(["git", "-C", str(root), *args])
        objects = run("rev-list", "--objects", "--all").decode().splitlines()
        for entry in objects:
            oid, _, name = entry.partition(" ")
            if run("cat-file", "-t", oid).strip() != b"blob":
                continue
            blobs += 1
            hits = scan_blob(name, run("cat-file", "-p", oid), manifest)
            if hits:
                failures.append(("history:" + oid[:10] + ":" + name, hits))
        metadata = run("log", "--all", "--format=%an <%ae>%n%cn <%ce>%n%B").decode()
        hits = scan_text(metadata)
        if hits:
            failures.append(("commit metadata", hits))
    return failures, scanned, blobs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    failures, scanned, blobs = audit(args.root)
    for path, reasons in failures:
        print(path + ": " + ", ".join(reasons))
    if failures:
        raise SystemExit(1)
    print(f"Publication patterns passed: {scanned} working files, {blobs} historical blobs")
    print("Manual content and image review still required; no scanner guarantees privacy.")


if __name__ == "__main__":
    main()

