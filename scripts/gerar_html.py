from pathlib import Path
import re
import html

# =========================================================
# CAMINHOS DO PROJETO
# =========================================================
# ROOT aponta para a raiz do projeto.
# Como este script fica dentro da pasta scripts/,
# usamos parents[1] para subir uma pasta.
ROOT = Path(__file__).resolve().parents[1]

# Pasta onde ficam os capítulos separados em Markdown.
CAP_DIR = ROOT / "manuscrito" / "capitulos"

# Arquivo HTML final que será gerado para o site.
OUT = ROOT / "site" / "index.html"


# =========================================================
# CONFIGURAÇÕES PRINCIPAIS DO LIVRO
# =========================================================
# Título principal do livro.
BOOK_TITLE = "HIRUI NAKI CHISUJI"

# Tradução em português do título.
BOOK_TRANSLATION = "A Linhagem Suprema"

# Título em japonês.
BOOK_JAPANESE = "比類なき血筋"

# Imagem usada como arte da capa.
# O caminho é relativo ao arquivo site/index.html.
COVER_IMAGE = "assets/capa-hirui.png"

# Dados da página de autoria.
# Pode editar os textos aqui sem mexer no resto do código.
AUTHOR_BLOCK = [
    ("Autor", "Raí Onório"),
    ("Edição", "Raí Onório"),
    ("Revisão editorial", "Revisão editorial assistida por ChatGPT"),
    ("Projeto", "HIRUI NAKI CHISUJI — Versão literária"),
]

# Sinopse exibida na Home e também no PDF do livro.
SYNOPSIS = [
    "Em uma terra feudal marcada por clãs, dívidas de sangue e pactos antigos, Rin Kurosawa aprende cedo que sobreviver exige mais do que coragem. Após perder a mãe, ver o pai definhar sob o peso da servidão e assistir o irmão ser condenado por uma mentira política, ela é empurrada para uma guerra que começou muito antes de seu nascimento.",
    "Entre os Onizuka, os Hayashi e a ameaça ancestral dos Kurotsuki, cada aliança cobra um preço. Katsuro Morikawa, capitão Hayashi movido por dever, vingança e feridas antigas, oferece salvação sem prometer inocência. Takeshi Kurosawa, guerreiro brutal e protetor, tenta transformar sobrevivência em propósito enquanto carrega as correntes invisíveis do exílio.",
    "HIRUI NAKI CHISUJI é uma história de honra, dor, herança e resistência, onde cada escolha deixa cicatrizes — e onde viver pode custar quase tanto quanto morrer.",
]

# Controle da paginação simulada.
# Quanto maior o número, menos páginas simuladas.
# Quanto menor o número, mais páginas simuladas.
CHARS_PER_PAGE = 2300

# Evita criar página nova com pouquíssimos parágrafos.
MIN_PARAGRAPHS_PER_PAGE = 4


# =========================================================
# CSS DO SITE E DO PDF
# =========================================================
# Todo o visual do site fica aqui:
# - Home
# - Autoria
# - Sumário
# - Leitor dos capítulos
# - Impressão/PDF
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

/* Reset básico para evitar diferenças estranhas entre navegadores */
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

/* =========================================================
   NAVBAR
   ========================================================= */

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

/* =========================================================
   CONTROLE DE TELAS
   ========================================================= */

.screen{
    display:none;
}

.screen.active{
    display:block;
}

/* =========================================================
   HOME
   ========================================================= */

.home-shell{
    width:min(1680px,100%);
    margin:0 auto;
    min-height:calc(100vh - 82px);
    display:grid;
    grid-template-columns:1.05fr .95fr;
}

.home-cover{
    position:relative;
    min-height:calc(100vh - 82px);
    display:flex;
    align-items:flex-start;
    justify-content:center;
    padding:72px 56px 56px;
    background:radial-gradient(circle at top,#2a211c 0,#14110f 42%,#090807 100%);
    text-align:center;
    overflow:hidden;
}

.home-cover::after{
    content:"";
    position:absolute;
    inset:0;
    z-index:1;
    background:
        linear-gradient(to bottom,rgba(0,0,0,.10) 0%,rgba(0,0,0,.30) 42%,rgba(0,0,0,.70) 100%),
        radial-gradient(circle at top,rgba(239,225,198,.10),rgba(0,0,0,0) 46%);
    pointer-events:none;
}

.home-cover-art{
    position:absolute;
    inset:0;
    z-index:0;
    width:100%;
    height:100%;
    object-fit:cover;
    object-position:center;
    opacity:.88;
    filter:brightness(.78) contrast(1.05) saturate(.95);
}

.home-cover-inner{
    position:relative;
    z-index:2;
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:16px;
    text-shadow:0 4px 20px rgba(0,0,0,.72);
}

.home-cover-inner{
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:16px;
}

.home-title-main{
    margin:0;
    color:var(--gold);
    font-size:clamp(2.6rem,4.6vw,5.8rem);
    line-height:1;
    letter-spacing:.08em;
    font-weight:normal;
    text-transform:uppercase;
}

.home-title-translation{
    margin:0;
    color:var(--gold-soft);
    font-size:clamp(1rem,1.4vw,1.35rem);
    line-height:1.3;
    letter-spacing:.08em;
}

.home-title-japanese{
    margin:0;
    color:var(--gold);
    font-family:"Yu Mincho","Hiragino Mincho ProN","Noto Serif JP",serif;
    font-size:clamp(2.2rem,3.8vw,4.6rem);
    line-height:1.15;
    letter-spacing:.08em;
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

/* =========================================================
   PÁGINAS INTERNAS: AUTORIA, SUMÁRIO E LEITOR
   ========================================================= */

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

/* Cards da página de autoria */
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

/* Botões do site */
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

/* Sumário na tela */
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

/* Leitor dos capítulos */
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

/* Texto literário dos capítulos */
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

/* A raiz de impressão fica escondida na tela.
   Ela só aparece quando o usuário gera PDF/imprime. */
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

    /* Esconde a interface do site durante a impressão */
    .site-header,
    .screen,
    .footer-note{
        display:none !important;
    }

    /* Mostra apenas o conteúdo próprio para PDF */
    #print-root{
        display:block !important;
        margin:0 !important;
        padding:0 !important;
        background:#11100f !important;
    }

    .print-page{
        display:block;
        width:210mm;
        min-height:297mm;
        margin:0 auto !important;
        page-break-after:always;
        break-after:page;
        overflow:hidden;
    }

    /* Modo PDF do livro:
       imprime capa, autoria, sinopse, sumário e todos os capítulos. */
    body[data-print-mode="book"] .book-only{
        display:block !important;
    }

    body[data-print-mode="book"] .chapter-page{
        display:block !important;
    }

    /* Modo PDF do capítulo:
       esconde capa, autoria, sinopse, sumário e todos os capítulos. */
    body[data-print-mode="chapter"] .book-only{
        display:none !important;
    }

    body[data-print-mode="chapter"] .chapter-page{
        display:none !important;
    }

    /* No modo PDF do capítulo, só o capítulo selecionado aparece. */
    body[data-print-mode="chapter"] .chapter-page.print-selected{
        display:block !important;
    }

    /* Capa do PDF */
.print-cover{
    position:relative !important;
    overflow:hidden !important;
    background:radial-gradient(circle at top,#2a211c 0,#14110f 42%,#090807 100%) !important;
    color:#efe1c6 !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
    align-items:center !important;
    text-align:center !important;
    padding:38mm 22mm 24mm !important;
}

.print-cover::after{
    content:"" !important;
    position:absolute !important;
    inset:0 !important;
    z-index:1 !important;
    background:
        linear-gradient(to bottom,rgba(0,0,0,.10) 0%,rgba(0,0,0,.34) 44%,rgba(0,0,0,.76) 100%),
        radial-gradient(circle at top,rgba(239,225,198,.10),rgba(0,0,0,0) 46%) !important;
}

.print-cover-art{
    position:absolute !important;
    inset:0 !important;
    z-index:0 !important;
    width:100% !important;
    height:100% !important;
    object-fit:cover !important;
    object-position:center !important;
    opacity:.88 !important;
    filter:brightness(.78) contrast(1.05) saturate(.95) !important;
}

.print-cover-inner{
    position:relative !important;
    z-index:2 !important;
    display:flex !important;
    flex-direction:column !important;
    align-items:center !important;
    gap:13pt !important;
    width:100% !important;
    text-shadow:0 4px 18px rgba(0,0,0,.72) !important;
}

    .print-title-main{
        margin:0 !important;
        color:#efe1c6 !important;
        font-size:34pt !important;
        line-height:1 !important;
        letter-spacing:.08em !important;
        font-weight:normal !important;
        text-transform:uppercase !important;
        white-space:nowrap !important;
    }

    .print-title-translation{
        margin:0 !important;
        color:#d9c59e !important;
        font-size:12pt !important;
        line-height:1.3 !important;
        letter-spacing:.08em !important;
    }

    .print-title-japanese{
        margin:0 !important;
        color:#efe1c6 !important;
        font-family:"Yu Mincho","Hiragino Mincho ProN","Noto Serif JP",serif !important;
        font-size:30pt !important;
        line-height:1.15 !important;
        letter-spacing:.08em !important;
    }

    /* Páginas de autoria, sinopse e sumário no PDF */
    .print-front{
        background:#f3ead8 !important;
        color:var(--ink) !important;
        padding:24mm 22mm !important;
    }

    .print-front h2{
        margin:0 0 18pt !important;
        color:var(--accent) !important;
        font-weight:normal !important;
        font-size:22pt !important;
        text-transform:uppercase !important;
        letter-spacing:.08em !important;
    }

    .print-front .meta-grid{
        display:grid !important;
        grid-template-columns:1fr 1fr !important;
        gap:14pt !important;
    }

    .print-front .meta-card{
        background:#efe4cf !important;
        border:1px solid #d5c2a1 !important;
        padding:14pt !important;
    }

    .print-front p,
    .print-front li,
    .print-front div{
        color:var(--ink) !important;
        font-size:12pt !important;
        line-height:1.7 !important;
    }

    .print-summary-list{
        list-style:none !important;
        margin:22pt 0 0 !important;
        padding:0 !important;
    }

    .print-summary-list li{
        display:flex !important;
        justify-content:space-between !important;
        gap:18pt !important;
        padding:7pt 0 !important;
        border-bottom:1px solid #d5c2a1 !important;
    }

    .print-summary-list .title{
        color:var(--ink) !important;
    }

    .print-summary-list .pages{
        color:#6c5948 !important;
        white-space:nowrap !important;
    }

    /* Página de capítulo no PDF */
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

/* =========================================================
   RESPONSIVO
   ========================================================= */

@media(max-width:1080px){
    .home-shell{
        grid-template-columns:1fr;
    }

    .home-cover{
        min-height:48vh;
        align-items:center;
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
# JAVASCRIPT DO SITE
# =========================================================
# Controla:
# - troca de telas
# - abertura de capítulos
# - impressão/PDF do livro
# - impressão/PDF de capítulo específico
JS = """
(function(){
    // Guarda as telas principais do site.
    const screens = {
        home: document.getElementById('screen-home'),
        auth: document.getElementById('screen-auth'),
        summary: document.getElementById('screen-summary'),
        reader: document.getElementById('screen-reader')
    };

    // Mostra uma tela e esconde as outras.
    window.showScreen = function(name){
        Object.values(screens).forEach(el => el.classList.remove('active'));

        if(screens[name]){
            screens[name].classList.add('active');
            window.scrollTo({top:0, behavior:'smooth'});
        }
    };

    // Abre um capítulo específico no leitor.
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

    // Prepara impressão do livro inteiro.
    window.printBook = function(){
        document.body.setAttribute('data-print-mode', 'book');
        document.body.removeAttribute('data-print-chapter');

        document.querySelectorAll('.chapter-page').forEach(el => {
            el.classList.remove('print-selected');
        });

        window.print();
    };

    // Prepara impressão de um capítulo específico.
    window.printChapter = function(num){
        document.body.setAttribute('data-print-mode', 'chapter');
        document.body.setAttribute('data-print-chapter', String(num));

        document.querySelectorAll('.chapter-page').forEach(el => {
            el.classList.remove('print-selected');
        });

        document.querySelectorAll('.chapter-page[data-chapter="' + num + '"]').forEach(el => {
            el.classList.add('print-selected');
        });

        window.print();
    };

    // Depois da impressão, volta o modo padrão para livro inteiro.
    window.addEventListener('afterprint', function(){
        document.body.setAttribute('data-print-mode', 'book');
        document.body.removeAttribute('data-print-chapter');

        document.querySelectorAll('.chapter-page').forEach(el => {
            el.classList.remove('print-selected');
        });
    });

    // Modo padrão caso o usuário use Ctrl+P direto.
    document.body.setAttribute('data-print-mode', 'book');
})();
"""


# =========================================================
# FUNÇÕES DE APOIO
# =========================================================

# Palavras que devem continuar minúsculas ao gerar título pelo nome do arquivo.
LOWER_WORDS = {
    "a", "o", "as", "os",
    "de", "da", "do", "das", "dos",
    "e", "em", "na", "no", "nas", "nos",
    "que", "se", "para", "por", "com",
    "um", "uma", "ao", "à", "às", "aos"
}


def safe(text: str) -> str:
    """
    Escapa textos para HTML.

    Isso impede que caracteres especiais quebrem o HTML.
    Exemplo:
    < vira &lt;
    > vira &gt;
    """
    return html.escape(text, quote=True)


def title_from_filename(path: Path) -> str:
    """
    Cria um título legível a partir do nome do arquivo.

    Exemplo:
    05-a-casa-onde-a-guerra-respira.md
    vira:
    A Casa Onde a Guerra Respira
    """
    name = re.sub(r"^\d+[-_ ]*", "", path.stem)
    name = name.replace("-", " ").replace("_", " ").strip()

    words = []

    for word in name.split():
        lw = word.lower()

        if lw in LOWER_WORDS:
            words.append(lw)
        else:
            words.append(lw.capitalize())

    return " ".join(words)


def chapter_number_from_filename(path: Path) -> int:
    """
    Pega o número do capítulo pelo começo do nome do arquivo.

    Exemplo:
    07-mascaras-na-estrada.md
    retorna:
    7
    """
    match = re.match(r"^(\d+)", path.stem)
    return int(match.group(1)) if match else 0


def parse_markdown_chapter(path: Path) -> dict:
    """
    Lê um arquivo Markdown de capítulo e extrai:
    - número do capítulo
    - título
    - blocos de texto

    O formato esperado é:
    # Capítulo 7
    ## Máscaras na Estrada

    Texto do capítulo...
    """
    text = path.read_text(encoding="utf-8").strip()
    lines = text.splitlines()

    num = None
    title = None
    raw_lines = []

    for line in lines:
        clean = line.strip()

        # Detecta linha do tipo: # Capítulo 7
        if clean.startswith("# Capítulo"):
            match = re.search(r"(\d+)", clean)
            num = int(match.group(1)) if match else chapter_number_from_filename(path)
            continue

        # Detecta linha do tipo: ## Título do Capítulo
        if clean.startswith("## "):
            title = clean[3:].strip()
            continue

        # Todo o resto entra como corpo do capítulo.
        raw_lines.append(line)

    # Se não achou número no conteúdo, usa o número do arquivo.
    if num is None:
        num = chapter_number_from_filename(path)

    # Se não achou título no conteúdo, usa o nome do arquivo.
    if not title:
        title = title_from_filename(path)

    blocks = []
    buffer = []

    def flush_buffer():
        """
        Fecha o parágrafo atual e manda para a lista de blocos.
        """
        nonlocal buffer

        if buffer:
            blocks.append(" ".join(x.strip() for x in buffer if x.strip()))
            buffer = []

    for line in raw_lines:
        clean = line.strip()

        # Linha com --- vira separador visual no HTML.
        if clean == "---":
            flush_buffer()
            blocks.append("__HR__")
            continue

        # Linha com texto entra no parágrafo atual.
        if clean:
            buffer.append(clean)
        else:
            # Linha vazia fecha o parágrafo.
            flush_buffer()

    flush_buffer()

    return {
        "num": num,
        "title": title,
        "blocks": blocks
    }


def paginate_blocks(blocks, chars_per_page=CHARS_PER_PAGE, min_blocks=MIN_PARAGRAPHS_PER_PAGE):
    """
    Divide o texto em páginas simuladas.

    Isso não é paginação editorial profissional.
    É uma simulação por quantidade de caracteres para leitura no site e PDF.
    """
    if not blocks:
        return [[]]

    pages = []
    current = []
    current_chars = 0

    for block in blocks:
        # Separadores contam como um pequeno espaço.
        block_cost = 120 if block == "__HR__" else len(block)
        proposed_chars = current_chars + block_cost

        # Cria nova página quando passa do limite.
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
    """
    Transforma blocos de texto em HTML.

    Parágrafo vira <p>.
    Separador __HR__ vira <hr>.
    """
    parts = []

    for block in blocks:
        if block == "__HR__":
            parts.append("<hr>")
        else:
            parts.append(f"<p>{safe(block)}</p>")

    return "\n".join(parts)


def format_page_range(start_page: int, end_page: int) -> str:
    """
    Formata intervalo de páginas.

    Exemplo:
    Página 5
    ou
    Páginas 5–12
    """
    if start_page == end_page:
        return f"Página {start_page}"

    return f"Páginas {start_page}–{end_page}"


def build_chapters():
    """
    Lê todos os capítulos da pasta manuscrito/capitulos,
    ordena pelo número e calcula páginas simuladas.
    """
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


# =========================================================
# RENDERIZAÇÃO DAS TELAS DO SITE
# =========================================================

def render_home():
    """
    Gera a tela Home:
    - capa visual
    - sinopse
    """
    synopsis_html = "\n".join(f"<p>{safe(p)}</p>" for p in SYNOPSIS)

    return f"""
<section class="screen screen-home active" id="screen-home">
    <div class="home-shell">
        <div class="home-cover">
    <img class="home-cover-art" src="{safe(COVER_IMAGE)}" alt="">
    <div class="home-cover-inner">
        <h1 class="home-title-main">{safe(BOOK_TITLE)}</h1>
        <p class="home-title-translation">{safe(BOOK_TRANSLATION)}</p>
        <p class="home-title-japanese">{safe(BOOK_JAPANESE)}</p>
    </div>
</div>

        <div class="home-synopsis">
            <h2>Sinopse</h2>
            {synopsis_html}
        </div>
    </div>
</section>
""".strip()


def render_authorship():
    """
    Gera a tela de Autoria.
    """
    meta_html = "\n".join(
        f"""
        <article class="meta-card">
            <h3>{safe(label)}</h3>
            <p>{safe(value)}</p>
        </article>
        """.strip()
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
    """
    Gera a tela de Sumário:
    - lista todos os capítulos
    - mostra intervalo de páginas simuladas
    - botão para abrir capítulo
    - botão para PDF do capítulo
    - botão para PDF do livro
    """
    items = []

    for chapter in chapters:
        page_range = format_page_range(chapter["start_page"], chapter["end_page"])

        items.append(
            f"""
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
            """.strip()
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
    """
    Gera o leitor de capítulos.
    Cada capítulo vira uma tela interna com páginas simuladas.
    """
    chapter_views = []

    for chapter in chapters:
        page_cards = []

        for page in chapter["pages"]:
            # O cabeçalho do capítulo aparece só na primeira página do capítulo.
            header_html = ""

            if page["local_page"] == 1:
                header_html = f"""
                <header>
                    <span class="label">Capítulo {chapter["num"]}</span>
                    <h2>{safe(chapter["title"])}</h2>
                </header>
                """.strip()

            page_cards.append(
                f"""
                <article class="page-card">
                    <div class="page-marker"><span>Página {page["global_page"]}</span></div>

                    {header_html}

                    <div class="body-text">
                        {render_body_blocks(page["blocks"])}
                    </div>
                </article>
                """.strip()
            )

        chapter_views.append(
            f"""
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
            """.strip()
        )

    return f"""
<section class="screen" id="screen-reader">
    {"".join(chapter_views)}
</section>
""".strip()


# =========================================================
# RENDERIZAÇÃO DO CONTEÚDO PARA PDF
# =========================================================

def render_print_root(chapters):
    """
    Gera uma versão separada do conteúdo apenas para impressão/PDF.

    Isso evita imprimir navbar, botões e telas escondidas.
    Também permite que o PDF do livro tenha:
    - capa
    - autoria
    - sinopse
    - sumário
    - capítulos

    E que o PDF de capítulo imprima apenas o capítulo escolhido.
    """
    auth_cards = "\n".join(
        f"""
        <article class="meta-card">
            <h3>{safe(label)}</h3>
            <p>{safe(value)}</p>
        </article>
        """.strip()
        for label, value in AUTHOR_BLOCK
    )

    synopsis_html = "\n".join(f"<p>{safe(p)}</p>" for p in SYNOPSIS)

    summary_items = "\n".join(
        f"""
        <li>
            <span class="title">Capítulo {chapter["num"]} — {safe(chapter["title"])}</span>
            <span class="pages">{format_page_range(chapter["start_page"], chapter["end_page"])}</span>
        </li>
        """.strip()
        for chapter in chapters
    )

    print_pages = []

    # Capa do PDF do livro.
    print_pages.append(
        f"""
        <section class="print-page print-cover book-only">
    <img class="print-cover-art" src="{safe(COVER_IMAGE)}" alt="">
    <div class="print-cover-inner">
        <h1 class="print-title-main">{safe(BOOK_TITLE)}</h1>
        <p class="print-title-translation">{safe(BOOK_TRANSLATION)}</p>
        <p class="print-title-japanese">{safe(BOOK_JAPANESE)}</p>
    </div>
</section>
        """.strip()
    )

    # Página de autoria do PDF do livro.
    print_pages.append(
        f"""
        <section class="print-page print-front book-only">
            <h2>Autoria</h2>

            <div class="meta-grid">
                {auth_cards}
            </div>
        </section>
        """.strip()
    )

    # Página de sinopse e sumário do PDF do livro.
    print_pages.append(
        f"""
        <section class="print-page print-front book-only">
            <h2>Sinopse</h2>

            {synopsis_html}

            <h2 style="margin-top:28pt;">Sumário</h2>

            <ol class="print-summary-list">
                {summary_items}
            </ol>
        </section>
        """.strip()
    )

    # Páginas dos capítulos no PDF.
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
                f"""
                <section class="print-page chapter-page" data-chapter="{chapter["num"]}">
                    <div class="page-marker"><span>Página {page["global_page"]}</span></div>

                    {header_html}

                    <div class="body-text">
                        {render_body_blocks(page["blocks"])}
                    </div>
                </section>
                """.strip()
            )

    return f'<div id="print-root">{"".join(print_pages)}</div>'


# =========================================================
# FUNÇÃO PRINCIPAL
# =========================================================

def main():
    """
    Função principal do script.

    Ela:
    1. lê os capítulos em Markdown
    2. calcula páginas simuladas
    3. monta o HTML completo
    4. salva em site/index.html
    """
    chapters, total_pages = build_chapters()

    # Navbar fixa do site.
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

    # Documento HTML final.
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