"""Resolve local Markdown and HTML links, including Markdown heading fragments."""
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.links.extend(attrs[key] for key in ("href", "src") if key in attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])


def fragments(path):
    text = path.read_text()
    if path.suffix == ".md":
        result, seen = set(), {}
        for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.M):
            slug = re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")
            number = seen.get(slug, 0)
            seen[slug] = number + 1
            result.add(slug + ("-" + str(number) if number else ""))
        return result
    parser = HTMLLinks()
    parser.feed(text)
    return parser.ids


def check(root=ROOT):
    failures, external, count = [], set(), 0
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts or path.suffix not in (".md", ".html"):
            continue
        text = path.read_text()
        if path.suffix == ".md":
            fence = chr(96) * 3
            text = re.sub(fence + ".*?" + fence, "", text, flags=re.S)
            links = re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", text)
        else:
            parser = HTMLLinks()
            parser.feed(text)
            links = parser.links + re.findall(r"url\(['\"]?([^)'\"\s]+)", text)
        for link in links:
            parsed = urlsplit(link)
            if parsed.scheme in ("https", "http"):
                external.add(link)
                continue
            if parsed.scheme or parsed.netloc:
                failures.append((path.name, "unexpected URL scheme"))
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
            if not target.is_relative_to(root.resolve()) or not target.exists():
                failures.append((path.relative_to(root).as_posix(), link))
            elif parsed.fragment and target.suffix in (".md", ".html"):
                if unquote(parsed.fragment) not in fragments(target):
                    failures.append((path.relative_to(root).as_posix(), link))
            count += 1
    return failures, count, external


if __name__ == "__main__":
    failures, count, external = check()
    for path, target in failures:
        print(path + ": unresolved " + target)
    if failures:
        raise SystemExit(1)
    print(f"Resolved {count} local links; {len(external)} external URLs require separate checking.")

