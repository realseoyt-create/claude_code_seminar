#!/usr/bin/env python3
"""
슬라이드 PDF 생성기
content.yaml → HTML → PDF (Playwright)
"""
import yaml
import asyncio
import re
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def load_content(path: str = "content.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def render_html(content: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(Path(__file__).parent / "templates")),
        autoescape=False,
    )
    # md_bold: **text** → <strong>text</strong>, *text* → <em>text</em>
    def md_bold(text: str) -> str:
        if not text:
            return ""
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", str(text))
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        text = text.replace("\\n", "<br>").replace("\n", "<br>")
        return text

    env.filters["md"] = md_bold
    template = env.get_template("slide.html")
    return template.render(
        metadata=content.get("metadata", {}),
        slides=content.get("slides", []),
    )


async def export_pdf(html: str, output_path: str = "output.pdf") -> None:
    from playwright.async_api import async_playwright

    tmp = Path("_slides_tmp.html")
    tmp.write_text(html, encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        await page.goto(f"file://{tmp.absolute()}")
        await page.wait_for_load_state("networkidle")
        # 폰트 로딩 대기
        await page.wait_for_timeout(2000)
        await page.pdf(
            path=output_path,
            width="1280px",
            height="720px",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        await browser.close()

    tmp.unlink()
    print(f"✅ {output_path} 생성 완료")


def main():
    content_path = sys.argv[1] if len(sys.argv) > 1 else "content.yaml"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.pdf"

    print(f"📄 {content_path} 로딩 중...")
    content = load_content(content_path)
    slide_count = len(content.get("slides", []))
    print(f"🎴 슬라이드 {slide_count}장 발견")

    print("🖌  HTML 렌더링 중...")
    html = render_html(content)

    print("🖨  PDF 출력 중 (Playwright)...")
    asyncio.run(export_pdf(html, output_path))


if __name__ == "__main__":
    main()
