from pathlib import Path
import pymupdf
root = Path(__file__).resolve().parents[1]
pdf = root / "site/demos/data/raw/2025_pdfs/20016861.pdf"
with pymupdf.open(pdf) as document:
    assert len(document) == 1, "Expected the captured one-page House PTR"
    page = document[0]
    assert "McGuire" in page.get_text(), "Wrong House source"
    svg = page.get_svg_image(text_as_path=True)
    assert "<svg" in svg and "viewBox" in svg
out = root / "site/assets/house-ptr-20016861.svg"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(svg, encoding="utf-8")
print(f"Rendered original House PDF to vector SVG: {len(svg):,} bytes")
