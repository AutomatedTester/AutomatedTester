import feedparser
import pathlib
import re

root = pathlib.Path(__file__).parent.resolve()


def fetch_blog_entries():

    entries = feedparser.parse("https://www.theautomatedtester.co.uk/blog/index.xml")['entries']

    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]


def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(
        marker, chunk, marker)
    return r.sub(chunk, content)


if __name__ == "__main__":
    readme = root / "README.md"
    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url})".format(**entry)
         for entry in entries]
    )
    readme_contents = readme.open().read()
    rewritten = replace_chunk(readme_contents, "blog", entries_md)
    readme.open("w").write(rewritten)
