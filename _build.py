#!/usr/bin/env python3
"""Render the two legal markdown files into the final two HTML pages.
Splits each doc by `---` into English / Spanish, parses sections under ##,
extracts ### items into TOC + numbered headings.
"""
import re
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent

PAGES = [
    {
        "src": "_PRIVACY_POLICY.md",
        "dst": "privacy/index.html",
        "kicker": "Document 01 · Effective on App Store launch",
        "title_en": "Privacy <em>Policy</em>",
        "title_es": "Pol&iacute;tica de <em>Privacidad</em>",
        "title_seo": "Privacy Policy · CycleSync",
        "desc_seo": "CycleSync Privacy Policy. 100% on-device wellness app. No backend, no accounts, no analytics, no tracking.",
        "back_root": "../",
    },
    {
        "src": "_TERMS_OF_USE.md",
        "dst": "terms/index.html",
        "kicker": "Document 02 · Effective on App Store launch",
        "title_en": "Terms <em>of Use</em>",
        "title_es": "T&eacute;rminos <em>de Uso</em>",
        "title_seo": "Terms of Use · CycleSync",
        "desc_seo": "CycleSync Terms of Use. Wellness positioning, eligibility, license, limitation of liability, governing law of Spain.",
        "back_root": "../",
    },
]

CODE_RE = re.compile(r"`([^`]+)`")
H3_NUM_RE = re.compile(r"^(\d+)\.\s+(.*)$")


def inline(text: str) -> str:
    text = escape(text)
    text = CODE_RE.sub(r"<code>\1</code>", text)
    return text


def parse_section(md: str):
    """Split a single-language section by ### headings. Return list of {num,title,html}."""
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
    """Tiny markdown → HTML for the body of a section. Supports paragraphs, bullet lists, inline code."""
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
        # paragraph: collect until blank line
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


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_seo}</title>
<meta name="description" content="{desc_seo}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='42' fill='none' stroke='%23c8324b' stroke-width='14' stroke-dasharray='66 198'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{back_root}assets/style.css">
</head>
<body>

<header class="topbar">
  <div class="topbar-inner">
    <a href="{back_root}" class="brand">
      <span class="brand-mark"></span>
      <span class="brand-name">CycleSync <em>· legal</em></span>
    </a>
    <nav class="topnav">
      <a href="{back_root}">Index</a>
      <a href="{back_root}privacy/" {privacy_active}>Privacy</a>
      <a href="{back_root}terms/" {terms_active}>Terms</a>
    </nav>
  </div>
</header>

<main class="doc-shell">
  <div class="doc-header">
    <div class="doc-header-left">
      <div class="doc-kicker">{kicker}</div>
      <h1 class="doc-h1" id="doc-title-en">{title_en}</h1>
      <h1 class="doc-h1" id="doc-title-es" style="display:none;">{title_es}</h1>
      <div class="lang-tabs" role="tablist">
        <button data-lang="en" class="active" role="tab">English</button>
        <button data-lang="es" role="tab">Espa&ntilde;ol</button>
      </div>
    </div>
    <div class="doc-meta">
      <strong>CycleSync</strong> · v1.0<br>
      Roberto Rojo Sahuquillo<br>
      Madrid &middot; Spain
    </div>
  </div>

  <aside class="doc-toc" aria-label="Table of contents">
    <div data-lang-block="en">
      <h4>On this page</h4>
      {toc_en}
    </div>
    <div data-lang-block="es" style="display:none;">
      <h4>En esta p&aacute;gina</h4>
      {toc_es}
    </div>
  </aside>

  <article class="doc-body">
    <section class="lang-section active" data-lang="en">
      {body_en}
    </section>
    <section class="lang-section" data-lang="es">
      {body_es}
    </section>
  </article>
</main>

<footer class="site-footer">
  <div class="footer-inner">
    <div>&copy; 2026 Roberto Rojo Sahuquillo &middot; Made in Spain</div>
    <div>
      <a href="{back_root}privacy/">Privacy</a>
      <a href="{back_root}terms/">Terms</a>
      <a href="mailto:rrojo.va@gmail.com">Contact</a>
    </div>
  </div>
</footer>

<script>
  (function () {{
    const tabs = document.querySelectorAll('.lang-tabs button');
    const sections = document.querySelectorAll('.lang-section');
    const tocBlocks = document.querySelectorAll('[data-lang-block]');
    const titleEN = document.getElementById('doc-title-en');
    const titleES = document.getElementById('doc-title-es');
    function setLang(l) {{
      tabs.forEach(t => t.classList.toggle('active', t.dataset.lang === l));
      sections.forEach(s => s.classList.toggle('active', s.dataset.lang === l));
      tocBlocks.forEach(b => b.style.display = b.dataset.langBlock === l ? '' : 'none');
      titleEN.style.display = l === 'en' ? '' : 'none';
      titleES.style.display = l === 'es' ? '' : 'none';
      document.documentElement.lang = l;
      try {{ localStorage.setItem('cs-legal-lang', l); }} catch (e) {{}}
    }}
    tabs.forEach(t => t.addEventListener('click', () => setLang(t.dataset.lang)));
    let saved = 'en';
    try {{ saved = localStorage.getItem('cs-legal-lang') || (navigator.language.startsWith('es') ? 'es' : 'en'); }} catch (e) {{}}
    setLang(saved);
  }})();
</script>

</body>
</html>
"""


def build_page(cfg):
    src = (ROOT / cfg["src"]).read_text(encoding="utf-8")
    # Split by `---` divider between EN and ES
    parts = re.split(r"^---\s*$", src, flags=re.M)
    if len(parts) < 2:
        raise SystemExit(f"{cfg['src']}: expected EN ---  ES separator")
    en_md = parts[0]
    es_md = parts[1]

    # Drop the leading `# Title` and `## English` / `## Español` headers; we provide our own.
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

    is_privacy = "privacy" in cfg["dst"]
    html = TEMPLATE.format(
        title_seo=cfg["title_seo"],
        desc_seo=cfg["desc_seo"],
        back_root=cfg["back_root"],
        kicker=cfg["kicker"],
        title_en=cfg["title_en"],
        title_es=cfg["title_es"],
        privacy_active='class="active"' if is_privacy else "",
        terms_active='class="active"' if not is_privacy else "",
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
