import os
import markdown
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from urllib.parse import quote

CONTENT_DIR = "docs"
OUTPUT_DIR  = "site"
TEMPLATE_FILE = "template.html"

env = Environment(loader=FileSystemLoader("."))
template = env.get_template(TEMPLATE_FILE)

def build_sidebar(current_path: Path = None) -> str:
    lines = []
    root = Path(CONTENT_DIR)

    def walk(p: Path, level=0):
        for item in sorted(p.iterdir()):
            if item.is_dir():
                name = item.name.replace("-", " ").title()
                lines.append("  " * level + f"<li><strong>{name}</strong></li>")
                lines.append("  " * level + "<ul>")
                walk(item, level + 1)
                lines.append("  " * level + "</ul>")
            elif item.suffix == ".md" and item.name != "index.md":
                rel = item.relative_to(root).with_suffix("")
                url = quote(str(rel).replace(os.sep, "/"))
                title = item.stem.replace("-", " ").title()
                active = " active" if current_path and current_path == item else ""
                lines.append("  " * level + f'<li><a href="/{url}.html" class="{active.strip()}">{title}</a></li>')

    lines.append("<ul>")
    lines.append('<li><a href="/index.html" class="{}">Home</a></li>'.format(
        'active' if current_path and current_path.name == "index.md" else ""
    ))
    walk(root)
    lines.append("</ul>")
    return "\n".join(lines)

def md_to_html(md_path: Path):
    with md_path.open(encoding="utf-8") as f:
        text = f.read()
    title = md_path.stem.replace("-", " ").title()
    if text.startswith("# "):
        title = text.split("\n", 1)[0][2:].strip()
    html = markdown.markdown(text, extensions=["extra", "toc", "fenced_code", "tables"])
    return title, html

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    content_path = Path(CONTENT_DIR)
    for md_file in content_path.rglob("*.md"):
        rel_path = md_file.relative_to(content_path)
        out_file = Path(OUTPUT_DIR) / rel_path.with_suffix(".html")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        title, content_html = md_to_html(md_file)
        sidebar_html = build_sidebar(md_file)
        rendered = template.render(title=title, content=content_html, sidebar_html=sidebar_html)
        with out_file.open("w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"Generato: {out_file}")
    if (Path(OUTPUT_DIR) / "index.html").exists():
        print("Build completato ✓")

if __name__ == "__main__":
    main()
