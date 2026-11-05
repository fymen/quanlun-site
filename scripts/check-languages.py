#!/usr/bin/env python3
"""检查 Hugo 构建中的语言切换、站内链接、搜索及试读发布范围。"""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = []
        self.alternates = {}
        self.ids = set()
        self.canonical = ""
        self.lang = ""
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang", "")
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs["href"]
        if tag == "link" and attrs.get("hreflang"):
            self.alternates[attrs["hreflang"]] = attrs["href"]
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs)


def check(root):
    prefixes = {"zh": "/", "zh-tw": "/zh-tw/", "en": "/en/"}
    samples = {"kongjing", "breath_gap", "piquan_quanjia"}
    pages = ["", "read/", "book/", "about/", "search/", "articles/"]
    pages += [f"read/{slug}/" for slug in samples]
    for lang, prefix in prefixes.items():
        base = root / prefix.lstrip("/")
        actual = {p.parent.name for p in (base / "read").glob("*/index.html")}
        assert actual == samples, (lang, "公开试读范围", actual)
        index = json.loads((base / "index.json").read_text())
        indexed = {urlsplit(p["permalink"]).path for p in index}
        assert {p for p in indexed if "/read/" in p} == {
            prefix + f"read/{slug}/" for slug in samples
        }, (lang, "搜索索引")
        assert all(p.startswith(prefix) for p in indexed), (lang, "搜索语言")
        for relative in pages:
            page = Page(base / relative / "index.html")
            assert page.lang == lang, (lang, relative, "HTML 语言")
            assert urlsplit(page.canonical).path == prefix + relative
            assert {key: urlsplit(value).path for key, value in page.alternates.items()} == {
                key: value + relative for key, value in prefixes.items()
            }, (lang, relative, "hreflang")
            choices = {a["hreflang"]: urlsplit(a["href"]).path
                       for a in page.links if "hreflang" in a}
            assert choices == {key: value + relative for key, value in prefixes.items()
                               if key != lang}, (lang, relative, "语言切换")
            assert prefix + "#purchase" in {
                urlsplit(a["href"]).path + "#" + urlsplit(a["href"]).fragment
                for a in page.links
            }, (lang, relative, "购书菜单")
            if relative in {"read/kongjing/", "read/piquan_quanjia/"}:
                assert "footnote-1" in page.ids, (lang, relative, "脚注")
    # Follow all local page links and anchors, including feeds and translated bodies.
    for path in root.rglob("*.html"):
        page = Page(path)
        host = urlsplit(page.canonical).netloc
        for link in page.links:
            url = urlsplit(link["href"])
            if url.scheme and url.scheme not in {"http", "https"}:
                continue
            if url.netloc and url.netloc != host:
                continue
            if not url.path:
                target = path
            elif url.path.startswith("/"):
                target = root / unquote(url.path.lstrip("/"))
            else:
                target = path.parent / unquote(url.path)
            if target.is_dir():
                target /= "index.html"
            assert target.is_file(), (path, "链接不存在", link["href"])
            if url.fragment and target.suffix == ".html":
                assert unquote(url.fragment) in Page(target).ids, (
                    path, "锚点不存在", link["href"])
    print("检查通过：三种语言各公开三篇；语言切换、搜索、规范网址、站内链接、锚点和脚注正常。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="Hugo 构建输出目录")
    check(parser.parse_args().destination.resolve())
