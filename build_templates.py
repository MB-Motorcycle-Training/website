#!/usr/bin/env python3
import hashlib
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = ROOT_DIR / "templates"
DATA_FILE = ROOT_DIR / "data" / "data.yaml"
BUILD_TARGETS = [
    ("index.jinja.html", "index.html"),
    ("courses.jinja.html", "courses.html"),
    ("faq.jinja.html", "faq.html"),
    ("find_us.jinja.html", "find_us.html"),
]
STYLESHEET = "style.css"

def get_stylesheet_hash() -> str:
    with open(STYLESHEET, "rb") as f:
        css_hash = hashlib.md5(f.read()).hexdigest()[:8]
    return css_hash

def main():
    # Load the YAML database data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        site_data = yaml.safe_load(f)

    # Extract global context elements
    site_settings = site_data.get("site_settings", {})
    base_data = site_data.get("base_data", {})
    pages_meta = site_data.get("pages_meta", {})
    pages_content = site_data.get("pages_content", {})

    # 3. Initialize Jinja2 Environment
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=True,  # Keeps template variable output safe
        trim_blocks=True,
        lstrip_blocks=True,
    )

    for template_name, output_name in BUILD_TARGETS:
        print("Rendering", template_name.split(".")[0])
        # Extract base handle key from filename string (e.g. 'index.html' -> 'index')
        page_key = Path(output_name).stem

        # Extract context slices
        page_meta = pages_meta.get(page_key, {})
        page_content = pages_content.get(page_key, {})

        # Jinja2 payload
        context = {
            "site_settings": site_settings,
            "base_data": base_data,
            "page_data": page_meta,
            "page_content": page_content,
        }

        try:
            template = env.get_template(template_name)
            rendered_html = template.render(context)

            # Add hash to the stylesheet
            css_hash = get_stylesheet_hash()
            rendered_html = rendered_html.replace('style.css', f'style.css?v={css_hash}')


            # Write out to repo root directory execution pathway
            output_path = ROOT_DIR / output_name
            output_path.write_text(rendered_html, encoding="utf-8")
            print(f"   ✓ Built: {output_name}")

        except Exception as e:
            print(f"   ❌ Error compiling template '{template_name}': {e}")


if __name__ == "__main__":
    main()
