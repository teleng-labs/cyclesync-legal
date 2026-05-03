#!/usr/bin/env python3
"""Render the two legal markdown files into the final HTML pages.
Splits each doc by `---` into English / Spanish, parses sections under ##,
extracts ### items into TOC + numbered headings.
The output is bilingual; the global i18n.js toggle hides/shows whichever language.
"""
import re
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent

PAGES = [
    {
        "src": "_PRIVACY_POLICY.md",
        "dst": "privacy/index.html",
        "kicker_en": "Document 01 · Effective on App Store launch",
        "kicker_es": "Documento 01 · Vigente desde el lanzamiento en App Store",
        "title_en": "Privacy <em>Policy</em>",
        "title_es": "Pol&iacute;tica de <em>Privacidad</em>",
        "title_seo_en": "Privacy Policy · CycleSync",
        "title_seo_es": "Política de Privacidad · CycleSync",
        "desc_seo_en": "CycleSync Privacy Policy. 100% on-device wellness app. No backend, no accounts, no analytics, no tracking.",
        "desc_seo_es": "Política de Privacidad de CycleSync. App de bienestar 100% en el dispositivo. Sin backend, sin cuentas, sin analítica, sin tracking.",
        "back_root": "../",
        "is_privacy": True,
    },
    {
        "src": "_TERMS_OF_USE.md",
        "dst": "terms/index.html",
        "kicker_en": "Document 02 · Effective on App Store launch",
        "kicker_es": "Documento 02 · Vigente desde el lanzamiento en App Store",
        "title_en": "Terms <em>of Use</em>",
        "title_es": "T&eacute;rminos <em>de Uso</em>",
        "title_seo_en": "Terms of Use · CycleSync",
        "title_seo_es": "Términos de Uso · CycleSync",
        "desc_seo_en": "CycleSync Terms of Use. Wellness positioning, eligibility, license, limitation of liability, governing law of Spain.",
        "desc_seo_es": "Términos de Uso de CycleSync. Posicionamiento de bienestar, elegibilidad, licencia, limitación de responsabilidad, ley aplicable de España.",
        "back_root": "../",
        "is_privacy": False,
    },
]

CODE_RE = re.compile(r"`([^`]+)`")
H3_NUM_RE = re.compile(r"^(\d+)\.\s+(.*)$")


def inline(text: str) -> str:
    text = escape(text)
    text = CODE_RE.sub(r"<code>\1</code>", text)
    return text


def parse_section(md: str):
    """Split a single-language section by ### headings."""
    blocks = re.split(r"^### ", md, flags=re.M)
    intro = blocks[0].strip()
    items = []
    for raw in blocks[1:]:
        head, _, body = raw.partition("\n")
        head = head.strip()
        m = H3_NUM_RE.match(head)
        if m:
            num = m.group(1)
            title = m.group(2).strip()
        else:
            num = ""
            title = head
        items.append({"num": num, "title": title, "html": render_body(body)})
    return intro, items


def render_body(md: str) -> str:
    lines = md.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"  <li>{inline(lines[i][2:].strip())}</li>")
                i += 1
            out.append("</ul>")
            continue
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("- ") and not lines[i].startswith("### "):
            para.append(lines[i].rstrip())
            i += 1
        text = " ".join(para).strip()
        out.append(f"<p>{inline(text)}</p>")
    return "\n".join(out)


def render_lang(items, slug_prefix):
    parts = []
    for it in items:
        sid = f"{slug_prefix}-{it['num']}" if it['num'] else f"{slug_prefix}-{re.sub('[^a-z0-9]+', '-', it['title'].lower()).strip('-')}"
        num = f'<span class="num">{int(it["num"]):02d}</span>' if it["num"] else ""
        parts.append(f'<h3 id="{sid}">{num}<span>{escape(it["title"])}</span></h3>')
        parts.append(it["html"])
    return "\n".join(parts)


def render_toc(items, slug_prefix):
    if not items:
        return ""
    lis = []
    for it in items:
        sid = f"{slug_prefix}-{it['num']}" if it['num'] else f"{slug_prefix}-{re.sub('[^a-z0-9]+', '-', it['title'].lower()).strip('-')}"
        lis.append(f'<li><a href="#{sid}">{escape(it["title"])}</a></li>')
    return "<ol>\n" + "\n".join(lis) + "\n</ol>"


# Note: the doc body uses `lang-section` blocks marked data-lang-section="en"/"es".
# A small inline script (also in this template) syncs visibility with the global cs-lang.
TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-en="{title_seo_en}" data-es="{title_seo_es}">{title_seo_en}</title>
<meta name="description"
      data-i18n-attr="content"
      data-content-en="{desc_seo_en}"
      data-content-es="{desc_seo_es}"
      content="{desc_seo_en}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='42' fill='none' stroke='%23c8324b' stroke-width='14' stroke-dasharray='66 198'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{back_root}assets/style.css?v=1777836658">
<style>
  /* Hide whichever language is not active. The global toggle sets <html lang>. */
  html[lang="en"] [data-lang-section="es"] {{ display: none; }}
  html[lang="es"] [data-lang-section="en"] {{ display: none; }}
</style>
</head>
<body>

<header class="topbar">
  <div class="topbar-inner">
    <a href="{back_root}" class="brand">
      <span class="brand-mark"></span>
      <span class="brand-name">CycleSync</span>
    </a>
    <button class="topnav-toggle" type="button" aria-label="Menu"><span class="bars"><span></span></span><span class="label-txt" data-en="Menu" data-es="Menú">Menu</span></button>
    <nav class="topnav">
      <a href="{back_root}" data-en="Home" data-es="Inicio">Home</a>
      <a href="{back_root}app/" data-en="The App" data-es="La App">The App</a>
      <a href="{back_root}science/" data-en="Science" data-es="Ciencia">Science</a>
      <a href="{back_root}privacy/" {privacy_active} data-en="Privacy" data-es="Privacidad">Privacy</a>
      <a href="{back_root}terms/" {terms_active} data-en="Terms" data-es="Términos">Terms</a>
    </nav>
  </div>
</header>

<main class="doc-shell">
  <div class="doc-header">
    <div class="doc-header-left">
      <div class="doc-kicker" data-en="{kicker_en}" data-es="{kicker_es}">{kicker_en}</div>
      <h1 class="doc-h1" data-en="{title_en}" data-es="{title_es}">{title_en}</h1>
    </div>
    <div class="doc-meta">
      <strong>CycleSync</strong> · v1.0<br>
      Forge Labs<br>
      <span data-en="Alicante · Spain" data-es="Alicante · España">Alicante · Spain</span>
    </div>
  </div>

  <aside class="doc-toc" aria-label="Table of contents">
    <div data-lang-section="en">
      <h4>On this page</h4>
      {toc_en}
    </div>
    <div data-lang-section="es">
      <h4>En esta página</h4>
      {toc_es}
    </div>
  </aside>

  <article class="doc-body">
    <section data-lang-section="en">
      {body_en}
    </section>
    <section data-lang-section="es">
      {body_es}
    </section>
  </article>
</main>

<footer class="site-footer">
  <div class="footer-inner">
    <div data-en="© 2026 Forge Labs · Crafted in Alicante, Spain"
         data-es="© 2026 Forge Labs · Hecho en Alicante, España">© 2026 Forge Labs · Crafted in Alicante, Spain</div>
    <div>
      <a href="{back_root}" data-en="Home" data-es="Inicio">Home</a>
      <a href="{back_root}app/" data-en="The App" data-es="La App">The App</a>
      <a href="{back_root}science/" data-en="Science" data-es="Ciencia">Science</a>
      <a href="{back_root}privacy/" data-en="Privacy" data-es="Privacidad">Privacy</a>
      <a href="{back_root}terms/" data-en="Terms" data-es="Términos">Terms</a>
      <a href="mailto:rrojo.va@gmail.com" data-en="Contact" data-es="Contacto">Contact</a>
    </div>
  </div>
</footer>

<script src="{back_root}assets/i18n.js?v=1777836658"></script>

</body>
</html>
"""


def build_page(cfg):
    src = (ROOT / cfg["src"]).read_text(encoding="utf-8")
    parts = re.split(r"^---\s*$", src, flags=re.M)
    if len(parts) < 2:
        raise SystemExit(f"{cfg['src']}: expected EN ---  ES separator")
    en_md = parts[0]
    es_md = parts[1]

    def clean(md):
        md = re.sub(r"^# .*$", "", md, count=1, flags=re.M)
        md = re.sub(r"^## .*$", "", md, count=1, flags=re.M)
        return md.strip()

    _, items_en = parse_section(clean(en_md))
    _, items_es = parse_section(clean(es_md))

    body_en = render_lang(items_en, "en")
    body_es = render_lang(items_es, "es")
    toc_en = render_toc(items_en, "en")
    toc_es = render_toc(items_es, "es")

    html = TEMPLATE.format(
        title_seo_en=cfg["title_seo_en"],
        title_seo_es=cfg["title_seo_es"],
        desc_seo_en=cfg["desc_seo_en"],
        desc_seo_es=cfg["desc_seo_es"],
        back_root=cfg["back_root"],
        kicker_en=cfg["kicker_en"],
        kicker_es=cfg["kicker_es"],
        title_en=cfg["title_en"],
        title_es=cfg["title_es"],
        privacy_active='class="active"' if cfg["is_privacy"] else "",
        terms_active='class="active"' if not cfg["is_privacy"] else "",
        toc_en=toc_en,
        toc_es=toc_es,
        body_en=body_en,
        body_es=body_es,
    )

    out = ROOT / cfg["dst"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


for cfg in PAGES:
    build_page(cfg)
