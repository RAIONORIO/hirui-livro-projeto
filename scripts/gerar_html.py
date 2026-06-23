from pathlib import Path
import re
import html

ROOT = Path(__file__).resolve().parents[1]
CAP_DIR = ROOT / "manuscrito" / "capitulos"
OUT = ROOT / "site" / "index.html"

# =========================================================
# CONFIGURAÇÕES DO LIVRO
# =========================================================

BOOK_TITLE = "HIRUI NAKI CHISUJI"
BOOK_TITLE_STACKED = "HIRUI<br>NAKI<br>CHISUJI"
BOOK_SUBTITLE = "Romance literário"

# Edite estes dados como quiser
AUTHOR_BLOCK = [
    ("Autor", "Rai Onorio"),
    ("Edição", "Rai Onorio"),
    ("Revisão", "Projeto editorial assistido por IA"),
]

SYNOPSIS = [
    "Em uma terra feudal marcada por clãs, dívidas de sangue e pactos antigos, Rin Kurosawa aprende cedo que sobreviver exige mais do que coragem. Após perder a mãe, ver o pai definhar sob o peso da servidão e assistir o irmão ser condenado por uma mentira política, ela é empurrada para uma guerra que começou muito antes de seu nascimento.",
    "Entre os Onizuka, os Hayashi e a ameaça ancestral dos Kurotsuki, cada aliança cobra um preço. Katsuro Morikawa, capitão Hayashi movido por dever, vingança e feridas antigas, oferece salvação sem prometer inocência. Takeshi Kurosawa, guerreiro brutal e protetor, tenta transformar sobrevivência em propósito enquanto carrega as correntes invisíveis do exílio.",
    "HIRUI NAKI CHISUJI é uma história de honra, dor, herança e resistência, onde cada escolha deixa cicatrizes — e onde viver pode custar quase tanto quanto morrer."
]

# Quantidade aproximada de caracteres por página simulada
CHARS_PER_PAGE = 2300
MIN_PARAGRAPHS_PER_PAGE = 4


# =========================================================
# CSS
# =========================================================

CSS = """
:root{
    --bg:#11100f;
    --bg-soft:#1a1512;
    --paper:#f3ead8;
    --paper-2:#efe4cf;
    --ink:#241812;
    --ink-soft:#3b2b20;
    --accent:#6f1d1b;
    --rule:#d5c2a1;
    --gold:#efe1c6;
    --gold-soft:#d9c59e;
}

*{
    box-sizing:border-box;
}

html{
    scroll-behavior:smooth;
}

body{
    margin:0;
    background:radial-gradient(circle at top,#2a211c 0,#14110f 42%,#090807 100%);
    color:var(--ink);
    font-family:Georgia,"Times New Roman",serif;
}

button{
    font:inherit;
}

a{
    color:inherit;
}

.site-header{
    position:sticky;
    top:0;
    z-index:50;
    background:rgba(10,9,8,.96);
    border-bottom:1px solid rgba(213,194,161,.25);
    backdrop-filter:blur(8px);
}

.site-header-inner{
    width:min(1680px,calc(100% - 40px));
    margin:0 auto;
    min-height:82px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:24px;
}

.brand-button{
    background:none;
    border:0;
    color:var(--gold);
    font-size:1.05rem;
    letter-spacing:.16em;
    text-transform:uppercase;
    cursor:pointer;
    padding:0;
    text-align:left;
}

.nav-actions{
    display:flex;
    align-items:center;
    gap:16px;
    flex-wrap:wrap;
}

.nav-pill{
    background:rgba(255,255,255,.03);
    color:var(--gold);
    border:1px solid rgba(213,194,161,.28);
    border-radius:999px;
    padding:12px 24px;
    cursor:pointer;
    transition:.2s ease;
}

.nav-pill:hover{
    background:rgba(255,255,255,.08);
    border-color:rgba(213,194,161,.42);
}

.screen{
    display:none;
}

.screen.active{
    display:block;
}

.home-shell{
    width:min(1680px,100%);
    margin:0 auto;
    min-height:calc(100vh - 82px);
    display:grid;
    grid-template-columns:1.1fr .9fr;
}

.home-hero{
    min-height:calc(100vh - 82px);
    display:flex;
    align-items:flex-end;
    justify-content:center;
    padding:56px;
    background:radial-gradient(circle at top,#2a211c 0,#14110f 42%,#090807 100%);
}

.home-hero-title{
    color:var(--gold);
    font-size:clamp(4rem,8vw,9.2rem);
    line-height:.9;
    letter-spacing:.04em;
    text-transform:uppercase;
    margin:0;
    text-align:left;
}

.home-synopsis{
    background:var(--paper);
    padding:64px clamp(30px,5vw,64px);
    display:flex;
    flex-direction:column;
    justify-content:flex-start;
}

.home-synopsis h2{
    margin:0 0 36px;
    color:var(--accent);
    font-weight:normal;
    font-size:clamp(2rem,3vw,3rem);
    letter-spacing:.05em;
    text-transform:uppercase;
}

.home-synopsis p{
    margin:0 0 26px;
    color:var(--ink-soft);
    font-size:1.08rem;
    line-height:1.95;
    text-align:left;
}

.page-shell{
    width:min(1280px,calc(100% - 36px));
    margin:34px auto 70px;
    background:var(--paper);
    border:1px solid rgba(213,194,161,.78);
    box-shadow:0 24px 80px rgba(0,0,0,.42);
}

.section-head{
    padding:34px clamp(24px,4vw,48px);
    border-bottom:1px solid var(--rule);
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
    flex-wrap:wrap;
}

.section-head h2{
    margin:0;
    color:var(--accent);
    font-weight:normal;
    font-size:clamp(1.7rem,3vw,2.4rem);
    letter-spacing:.08em;
    text-transform:uppercase;
}

.section-body{
    padding:36px clamp(24px,4vw,48px) 44px;
}

.meta-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:18px;
}

.meta-card{
    background:var(--paper-2);
    border:1px solid var(--rule);
    padding:22px 20px;
}

.meta-card h3{
    margin:0 0 10px;
    color:#7b6650;
    font-weight:normal;
    font-size:.92rem;
    text-transform:uppercase;
    letter-spacing:.14em;
}

.meta-card p{
    margin:0;
    color:var(--ink);
    font-size:1.04rem;
    line-height:1.6;
}

.summary-actions,
.reader-actions{
    display:flex;
    gap:14px;
    flex-wrap:wrap;
}

.action-btn{
    background:none;
    border:1px solid rgba(111,29,27,.55);
    color:var(--accent);
    border-radius:999px;
    padding:14px 26px;
    cursor:pointer;
    transition:.2s ease;
}

.action-btn:hover{
    background:rgba(111,29,27,.08);
}

.action-btn.fill{
    background:#8b201d;
    color:#fff3e6;
    border-color:#8b201d;
}

.action-btn.fill:hover{
    background:#761b18;
}

.summary-list{
    list-style:none;
    margin:0;
    padding:0;
    display:flex;
    flex-direction:column;
    gap:14px;
}

.summary-item{
    display:grid;
    grid-template-columns:1fr auto auto;
    gap:16px;
    align-items:center;
    background:rgba(255,255,255,.28);
    border:1px solid var(--rule);
    padding:18px 20px;
}

.summary-main{
    min-width:0;
}

.summary-main h3{
    margin:0 0 6px;
    color:var(--ink);
    font-weight:normal;
    font-size:1.16rem;
    line-height:1.4;
}

.summary-main p{
    margin:0;
    color:#6c5948;
    font-size:.97rem;
}

.summary-pages{
    color:#6c5948;
    font-size:.95rem;
    white-space:nowrap;
}

.reader-wrap{
    padding:28px clamp(16px,2.8vw,28px) 48px;
}

.chapter-reader{
    display:none;
}

.chapter-reader.active{
    display:block;
}

.page-card{
    width:min(980px,100%);
    margin:0 auto 34px;
    background:var(--paper);
    border:1px solid var(--rule);
    box-shadow:0 12px 36px rgba(0,0,0,.10);
    padding:42px clamp(22px,5vw,74px) 48px;
}

.page-marker{
    max-width:680px;
    margin:0 auto 22px;
    display:flex;
    align-items:center;
    gap:14px;
    color:#8a7359;
    font-size:.82rem;
    letter-spacing:.18em;
    text-transform:uppercase;
    user-select:none;
}

.page-marker::before,
.page-marker::after{
    content:"";
    flex:1;
    height:1px;
    background:var(--rule);
}

.page-marker span{
    white-space:nowrap;
}

.page-card header{
    text-align:center;
    margin:0 0 42px;
}

.label{
    display:block;
    color:#7b6650;
    text-transform:uppercase;
    letter-spacing:.16em;
    font-size:.84rem;
    margin-bottom:10px;
}

.page-card h2{
    margin:0;
    color:var(--accent);
    font-weight:normal;
    font-size:clamp(2rem,4vw,3.35rem);
    line-height:1.08;
}

.body-text{
    max-width:680px;
    margin:0 auto;
    color:var(--ink);
}

.body-text p{
    margin:0 0 .92rem;
    padding:0;
    font-size:1.06rem;
    line-height:1.78;
    text-align:justify;
    text-indent:0;
    hyphens:none;
    overflow-wrap:normal;
    word-break:normal;
}

.body-text hr{
    width:38%;
    height:1px;
    border:0;
    background:var(--rule);
    margin:34px auto;
}

.footer-note{
    text-align:center;
    color:#d8c7aa;
    margin:28px 0 64px;
    font-size:.9rem;
    letter-spacing:.08em;
}

#print-root{
    display:none;
}

/* =========================================================
   IMPRESSÃO / PDF
   ========================================================= */

@media print{
    @page{
        size:A4 portrait;
        margin:0;
    }

    html,
    body{
        margin:0 !important;
        padding:0 !important;
        background:#f3ead8 !important;
        color:var(--ink) !important;
        -webkit-print-color-adjust:exact !important;
        print-color-adjust:exact !important;
    }

    *{
        -webkit-print-color-adjust:exact !important;
        print-color-adjust:exact !important;
    }

    .site-header,
    .screen,
    .footer-note{
        display:none !important;
    }

    #print-root{
        display:block !important;
        margin:0 !important;
        padding:0 !important;
        background:#11100f !important;
    }

    .print-page{
        width:210mm;
        min-height:297mm;
        margin:0 auto !important;
        page-break-after:always;
        break-after:page;
        overflow:hidden;
    }

    .book-only{
        display:block !important;
    }

    .chapter-page{
        display:block !important;
    }

    body[data-print-mode="chapter"] .book-only{
        display:none !important;
    }

    body[data-print-mode="chapter"] .chapter-page{
        display:none !important;
    }

    body[data-print-mode="chapter"][data-print-chapter="0"] .chapter-page[data-chapter="0"],
    body[data-print-mode="chapter"][data-print-chapter="1"] .chapter-page[data-chapter="1"],
    body[data-print-mode="chapter"][data-print-chapter="2"] .chapter-page[data-chapter="2"],
    body[data-print-mode="chapter"][data-print-chapter="3"] .chapter-page[data-chapter="3"],
    body[data-print-mode="chapter"][data-print-chapter="4"] .chapter-page[data-chapter="4"],
    body[data-print-mode="chapter"][data-print-chapter="5"] .chapter-page[data-chapter="5"],
    body[data-print-mode="chapter"][data-print-chapter="6"] .chapter-page[data-chapter="6"],
    body[data-print-mode="chapter"][data-print-chapter="7"] .chapter-page[data-chapter="7"],
    body[data-print-mode="chapter"][data-print-chapter="8"] .chapter-page[data-chapter="8"],
    body[data-print-mode="chapter"][data-print-chapter="9"] .chapter-page[data-chapter="9"],
    body[data-print-mode="chapter"][data-print-chapter="10"] .chapter-page[data-chapter="10"],
    body[data-print-mode="chapter"][data-print-chapter="11"] .chapter-page[data-chapter="11"],
    body[data-print-mode="chapter"][data-print-chapter="12"] .chapter-page[data-chapter="12"],
    body[data-print-mode="chapter"][data-print-chapter="13"] .chapter-page[data-chapter="13"],
    body[data-print-mode="chapter"][data-print-chapter="14"] .chapter-page[data-chapter="14"],
    body[data-print-mode="chapter"][data-print-chapter="15"] .chapter-page[data-chapter="15"],
    body[data-print-mode="chapter"][data-print-chapter="16"] .chapter-page[data-chapter="16"],
    body[data-print-mode="chapter"][data-print-chapter="17"] .chapter-page[data-chapter="17"],
    body[data-print-mode="chapter"][data-print-chapter="18"] .chapter-page[data-chapter="18"],
    body[data-print-mode="chapter"][data-print-chapter="19"] .chapter-page[data-chapter="19"],
    body[data-print-mode="chapter"][data-print-chapter="20"] .chapter-page[data-chapter="20"],
    body[data-print-mode="chapter"][data-print-chapter="21"] .chapter-page[data-chapter="21"],
    body[data-print-mode="chapter"][data-print-chapter="22"] .chapter-page[data-chapter="22"],
    body[data-print-mode="chapter"][data-print-chapter="23"] .chapter-page[data-chapter="23"],
    body[data-print-mode="chapter"][data-print-chapter="24"] .chapter-page[data-chapter="24"],
    body[data-print-mode="chapter"][data-print-chapter="25"] .chapter-page[data-chapter="25"],
    body[data-print-mode="chapter"][data-print-chapter="26"] .chapter-page[data-chapter="26"],
    body[data-print-mode="chapter"][data-print-chapter="27"] .chapter-page[data-chapter="27"],
    body[data-print-mode="chapter"][data-print-chapter="28"] .chapter-page[data-chapter="28"],
    body[data-print-mode="chapter"][data-print-chapter="29"] .chapter-page[data-chapter="29"],
    body[data-print-mode="chapter"][data-print-chapter="30"] .chapter-page[data-chapter="30"]{
        display:block !important;
    }

    .print-cover{
        background:radial-gradient(circle at top,#2a211c 0,#14110f 42%,#090807 100%) !important;
        color:#efe1c6 !important;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        text-align:center;
        padding:28mm;
    }

    .print-cover h1{
        margin:0 0 18pt;
        font-size:40pt;
        line-height:.95;
        letter-spacing:.08em;
        font-weight:normal;
        text-transform:uppercase;
        color:#efe1c6 !important;
    }

    .print-cover p{
        margin:0;
        color:#cdb890 !important;
        font-size:11pt;
        letter-spacing:.14em;
        text-transform:uppercase;
    }

    .print-front{
        background:#f3ead8 !important;
        color:var(--ink) !important;
        padding:24mm 22mm;
    }

    .print-front h2{
        margin:0 0 18pt;
        color:var(--accent) !important;
        font-weight:normal;
        font-size:22pt;
        text-transform:uppercase;
        letter-spacing:.08em;
    }

    .print-front .meta-card{
        background:#efe4cf !important;
    }

    .print-front p,
    .print-front li,
    .print-front div{
        color:var(--ink) !important;
        font-size:12pt;
        line-height:1.7;
    }

    .print-summary-list{
        list-style:none;
        margin:22pt 0 0;
        padding:0;
    }

    .print-summary-list li{
        display:flex;
        justify-content:space-between;
        gap:18pt;
        padding:7pt 0;
        border-bottom:1px solid #d5c2a1;
    }

    .print-summary-list .title{
        color:var(--ink) !important;
    }

    .print-summary-list .pages{
        color:#6c5948 !important;
        white-space:nowrap;
    }

    .chapter-page{
        background:#f3ead8 !important;
        color:var(--ink) !important;
        padding:26mm 24mm 24mm !important;
        box-shadow:none !important;
    }

    .chapter-page .page-marker{
        max-width:none !important;
        margin:0 auto 20pt !important;
        font-size:8pt !important;
    }

    .chapter-page header{
        text-align:center !important;
        margin:0 0 34pt !important;
    }

    .chapter-page .label{
        font-size:9pt !important;
        margin-bottom:8pt !important;
    }

    .chapter-page h2{
        font-size:28pt !important;
        line-height:1.12 !important;
        color:#6f1d1b !important;
    }

    .chapter-page .body-text{
        max-width:none !important;
    }

    .chapter-page .body-text p{
        margin:0 0 10pt !important;
        font-size:12pt !important;
        line-height:1.62 !important;
        color:var(--ink) !important;
    }

    .chapter-page .body-text hr{
        margin:26pt auto !important;
    }
}

@media(max-width:1080px){
    .home-shell{
        grid-template-columns:1fr;
    }

    .home-hero{
        min-height:48vh;
        align-items:center;
    }

    .home-hero-title{
        text-align:center;
    }
}

@media(max-width:760px){
    .site-header-inner{
        width:min(100%,calc(100% - 20px));
        min-height:76px;
    }

    .brand-button{
        font-size:.95rem;
        letter-spacing:.12em;
    }

    .nav-actions{
        gap:10px;
    }

    .nav-pill{
        padding:10px 18px;
    }

    .summary-item{
        grid-template-columns:1fr;
        align-items:flex-start;
    }

    .page-card{
        padding:34px 22px 36px;
    }

    .body-text p{
        font-size:1rem;
        line-height:1.68;
        text-align:left;
    }
}
"""

# =========================================================
# JS
# =========================================================

JS = """
(function(){
    const screens = {
        home: document.getElementById('screen-home'),
        auth: document.getElementById('screen-auth'),
        summary: document.getElementById('screen-summary'),
        reader: document.getElementById('screen-reader')
    };

    window.showScreen = function(name){
        Object.values(screens).forEach(el => el.classList.remove('active'));
        if(screens[name]){
            screens[name].classList.add('active');
            window.scrollTo({top:0, behavior:'smooth'});
        }
    };

    window.openChapter = function(num){
        showScreen('reader');

        document.querySelectorAll('.chapter-reader').forEach(el => {
            el.classList.remove('active');
        });

        const target = document.querySelector('.chapter-reader[data-chapter="' + num + '"]');
        if(target){
            target.classList.add('active');
            window.scrollTo({top:0, behavior:'smooth'});
        }
    };

    window.printBook = function(){
        document.body.setAttribute('data-print-mode', 'book');
        document.body.removeAttribute('data-print-chapter');
        window.print();
    };

    window.printChapter = function(num){
        document.body.setAttribute('data-print-mode', 'chapter');
        document.body.setAttribute('data-print-chapter', String(num));
        window.print();
    };

    window.addEventListener('afterprint', function(){
        document.body.setAttribute('data-print-mode', 'book');
        document.body.removeAttribute('data-print-chapter');
    });

    document.body.setAttribute('data-print-mode', 'book');
})();
"""

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

LOWER_WORDS = {
    "a", "o", "as", "os",
    "de", "da", "do", "das", "dos",
    "e", "em", "na", "no", "nas", "nos",
    "que", "se", "para", "por", "com",
    "um", "uma", "ao", "à", "às", "aos"
}


def safe(text: str) -> str:
    return html.escape(text, quote=True)


def title_from_filename(path: Path) -> str:
    name = re.sub(r"^\d+[-_ ]*", "", path.stem).replace("-", " ").replace("_", " ").strip()
    words = []
    for word in name.split():
        lw = word.lower()
        if lw in LOWER_WORDS:
            words.append(lw)
        else:
            words.append(lw.capitalize())
    return " ".join(words)


def chapter_number_from_filename(path: Path) -> int:
    match = re.match(r"^(\d+)", path.stem)
    return int(match.group(1)) if match else 0


def parse_markdown_chapter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8").strip()
    lines = text.splitlines()

    num = None
    title = None
    raw_lines = []

    for line in lines:
        clean = line.strip()

        if clean.startswith("# Capítulo"):
            match = re.search(r"(\d+)", clean)
            num = int(match.group(1)) if match else chapter_number_from_filename(path)
            continue

        if clean.startswith("## "):
            title = clean[3:].strip()
            continue

        raw_lines.append(line)

    if num is None:
        num = chapter_number_from_filename(path)

    if not title:
        title = title_from_filename(path)

    blocks = []
    buffer = []

    def flush_buffer():
        nonlocal buffer
        if buffer:
            blocks.append(" ".join(x.strip() for x in buffer if x.strip()))
            buffer = []

    for line in raw_lines:
        clean = line.strip()

        if clean == "---":
            flush_buffer()
            blocks.append("__HR__")
            continue

        if clean:
            buffer.append(clean)
        else:
            flush_buffer()

    flush_buffer()

    return {
        "num": num,
        "title": title,
        "blocks": blocks
    }


def paginate_blocks(blocks, chars_per_page=CHARS_PER_PAGE, min_blocks=MIN_PARAGRAPHS_PER_PAGE):
    if not blocks:
        return [[]]

    pages = []
    current = []
    current_chars = 0

    for block in blocks:
        block_cost = 120 if block == "__HR__" else len(block)
        proposed_chars = current_chars + block_cost

        if current and len(current) >= min_blocks and proposed_chars > chars_per_page:
            pages.append(current)
            current = [block]
            current_chars = block_cost
        else:
            current.append(block)
            current_chars = proposed_chars

    if current:
        pages.append(current)

    return pages


def render_body_blocks(blocks):
    parts = []
    for block in blocks:
        if block == "__HR__":
            parts.append("<hr>")
        else:
            parts.append(f"<p>{safe(block)}</p>")
    return "\n".join(parts)


def format_page_range(start_page: int, end_page: int) -> str:
    if start_page == end_page:
        return f"Página {start_page}"
    return f"Páginas {start_page}–{end_page}"


def build_chapters():
    chapter_files = sorted(CAP_DIR.glob("*.md"))
    chapters = [parse_markdown_chapter(p) for p in chapter_files]
    chapters.sort(key=lambda c: c["num"])

    global_page = 1

    for chapter in chapters:
        pages = paginate_blocks(chapter["blocks"])
        chapter["pages"] = []
        chapter["start_page"] = global_page

        for idx, page_blocks in enumerate(pages, start=1):
            chapter["pages"].append({
                "local_page": idx,
                "global_page": global_page,
                "blocks": page_blocks
            })
            global_page += 1

        chapter["end_page"] = global_page - 1
        chapter["page_count"] = len(chapter["pages"])

    return chapters, global_page - 1


def render_home():
    synopsis_html = "\n".join(f"<p>{safe(p)}</p>" for p in SYNOPSIS)

    return f"""
<section class="screen screen-home active" id="screen-home">
    <div class="home-shell">
        <div class="home-hero">
            <h1 class="home-hero-title">{BOOK_TITLE_STACKED}</h1>
        </div>
        <div class="home-synopsis">
            <h2>Sinopse</h2>
            {synopsis_html}
        </div>
    </div>
</section>
""".strip()


def render_authorship():
    meta_html = "\n".join(
        f'''
        <article class="meta-card">
            <h3>{safe(label)}</h3>
            <p>{safe(value)}</p>
        </article>
        '''.strip()
        for label, value in AUTHOR_BLOCK
    )

    return f"""
<section class="screen" id="screen-auth">
    <div class="page-shell">
        <div class="section-head">
            <h2>Autoria</h2>
            <div class="reader-actions">
                <button class="action-btn" onclick="showScreen('home')">Voltar ao início</button>
                <button class="action-btn" onclick="showScreen('summary')">Ir para o sumário</button>
            </div>
        </div>
        <div class="section-body">
            <div class="meta-grid">
                {meta_html}
            </div>
        </div>
    </div>
</section>
""".strip()


def render_summary(chapters):
    items = []

    for chapter in chapters:
        page_range = format_page_range(chapter["start_page"], chapter["end_page"])
        items.append(
            f'''
            <li class="summary-item">
                <div class="summary-main">
                    <h3>Capítulo {chapter["num"]} — {safe(chapter["title"])}</h3>
                    <p>{page_range}</p>
                </div>
                <div class="summary-pages">{chapter["page_count"]} página(s)</div>
                <div class="summary-actions">
                    <button class="action-btn" onclick="openChapter({chapter["num"]})">Abrir capítulo</button>
                    <button class="action-btn" onclick="printChapter({chapter["num"]})">PDF do capítulo</button>
                </div>
            </li>
            '''.strip()
        )

    return f"""
<section class="screen" id="screen-summary">
    <div class="page-shell">
        <div class="section-head">
            <h2>Sumário</h2>
            <div class="summary-actions">
                <button class="action-btn" onclick="showScreen('home')">Voltar ao início</button>
                <button class="action-btn fill" onclick="printBook()">PDF do livro</button>
            </div>
        </div>
        <div class="section-body">
            <ol class="summary-list">
                {"".join(items)}
            </ol>
        </div>
    </div>
</section>
""".strip()


def render_reader(chapters):
    chapter_views = []

    for chapter in chapters:
        page_cards = []

        for page in chapter["pages"]:
            header_html = ""
            if page["local_page"] == 1:
                header_html = f"""
                <header>
                    <span class="label">Capítulo {chapter["num"]}</span>
                    <h2>{safe(chapter["title"])}</h2>
                </header>
                """.strip()

            page_cards.append(
                f'''
                <article class="page-card">
                    <div class="page-marker"><span>Página {page["global_page"]}</span></div>
                    {header_html}
                    <div class="body-text">
                        {render_body_blocks(page["blocks"])}
                    </div>
                </article>
                '''.strip()
            )

        chapter_views.append(
            f'''
            <section class="chapter-reader" data-chapter="{chapter["num"]}">
                <div class="page-shell">
                    <div class="section-head">
                        <h2>Capítulo {chapter["num"]} — {safe(chapter["title"])}</h2>
                        <div class="reader-actions">
                            <button class="action-btn" onclick="showScreen('summary')">Voltar ao sumário</button>
                            <button class="action-btn" onclick="printChapter({chapter["num"]})">PDF deste capítulo</button>
                            <button class="action-btn fill" onclick="printBook()">PDF do livro</button>
                        </div>
                    </div>
                    <div class="reader-wrap">
                        {"".join(page_cards)}
                    </div>
                </div>
            </section>
            '''.strip()
        )

    return f"""
<section class="screen" id="screen-reader">
    {"".join(chapter_views)}
</section>
""".strip()


def render_print_root(chapters):
    auth_cards = "\n".join(
        f'''
        <article class="meta-card">
            <h3>{safe(label)}</h3>
            <p>{safe(value)}</p>
        </article>
        '''.strip()
        for label, value in AUTHOR_BLOCK
    )

    synopsis_html = "\n".join(f"<p>{safe(p)}</p>" for p in SYNOPSIS)

    summary_items = "\n".join(
        f'''
        <li>
            <span class="title">Capítulo {chapter["num"]} — {safe(chapter["title"])}</span>
            <span class="pages">{format_page_range(chapter["start_page"], chapter["end_page"])}</span>
        </li>
        '''.strip()
        for chapter in chapters
    )

    print_pages = [
        f'''
        <section class="print-page print-cover book-only">
            <h1>{BOOK_TITLE_STACKED}</h1>
            <p>{safe(BOOK_TITLE)}</p>
        </section>
        '''.strip(),

        f'''
        <section class="print-page print-front book-only">
            <h2>Autoria</h2>
            <div class="meta-grid">
                {auth_cards}
            </div>
        </section>
        '''.strip(),

        f'''
        <section class="print-page print-front book-only">
            <h2>Sinopse</h2>
            {synopsis_html}
            <h2 style="margin-top:28pt;">Sumário</h2>
            <ol class="print-summary-list">
                {summary_items}
            </ol>
        </section>
        '''.strip()
    ]

    for chapter in chapters:
        for page in chapter["pages"]:
            header_html = ""
            if page["local_page"] == 1:
                header_html = f"""
                <header>
                    <span class="label">Capítulo {chapter["num"]}</span>
                    <h2>{safe(chapter["title"])}</h2>
                </header>
                """.strip()

            print_pages.append(
                f'''
                <section class="print-page chapter-page" data-chapter="{chapter["num"]}">
                    <div class="page-marker"><span>Página {page["global_page"]}</span></div>
                    {header_html}
                    <div class="body-text">
                        {render_body_blocks(page["blocks"])}
                    </div>
                </section>
                '''.strip()
            )

    return f'<div id="print-root">{"".join(print_pages)}</div>'


def main():
    chapters, total_pages = build_chapters()

    nav = f"""
<header class="site-header">
    <div class="site-header-inner">
        <button class="brand-button" onclick="showScreen('home')">{safe(BOOK_TITLE)}</button>
        <div class="nav-actions">
            <button class="nav-pill" onclick="showScreen('auth')">Autoria</button>
            <button class="nav-pill" onclick="showScreen('summary')">Sumário</button>
        </div>
    </div>
</header>
""".strip()

    doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{safe(BOOK_TITLE)}</title>
<style>{CSS}</style>
</head>
<body data-print-mode="book">
{nav}
{render_home()}
{render_authorship()}
{render_summary(chapters)}
{render_reader(chapters)}
{render_print_root(chapters)}
<p class="footer-note">{safe(BOOK_TITLE)}</p>
<script>{JS}</script>
</body>
</html>"""

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")

    print(f"HTML gerado em: {OUT}")
    print(f"Capítulos: {len(chapters)}")
    print(f"Páginas simuladas: {total_pages}")


if __name__ == "__main__":
    main()