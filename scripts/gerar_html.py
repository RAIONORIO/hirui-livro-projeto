from pathlib import Path
import re
import html

ROOT = Path(__file__).resolve().parents[1]
CAP_DIR = ROOT / "manuscrito" / "capitulos"
OUT = ROOT / "site" / "index.html"

CSS = """
:root{
    --bg:#11100f;
    --paper:#f3ead8;
    --ink:#241812;
    --accent:#6f1d1b;
    --rule:#d5c2a1;
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
    font-family:Georgia,'Times New Roman',serif;
}

.cover{
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    padding:48px 24px;
    color:#efe1c6;
}

.cover h1{
    margin:0;
    font-size:clamp(3.2rem,8vw,7.2rem);
    line-height:.92;
    letter-spacing:.08em;
    font-weight:normal;
    text-transform:uppercase;
}

.shell{
    width:min(980px,calc(100% - 28px));
    margin:0 auto 80px;
    background:var(--paper);
    border:1px solid rgba(213,194,161,.75);
    box-shadow:0 24px 80px rgba(0,0,0,.45);
}

.toc{
    padding:56px min(72px,8vw) 44px;
    border-bottom:1px solid var(--rule);
}

.toc h2{
    text-align:center;
    color:var(--accent);
    font-weight:normal;
    letter-spacing:.18em;
    text-transform:uppercase;
    margin:0 0 32px;
}

.toc ol{
    columns:2;
    column-gap:54px;
    margin:0;
    padding-left:1.5rem;
}

.toc li{
    break-inside:avoid;
    margin:0 0 .62rem;
    line-height:1.45;
}

.toc a{
    color:#3b2b20;
    text-decoration:none;
    border-bottom:1px dotted rgba(111,29,27,.45);
}

.chapter{
    padding:64px min(86px,8vw) 56px;
    border-bottom:1px solid var(--rule);
}

.chapter header{
    text-align:center;
    margin:0 0 54px;
}

.label{
    display:block;
    color:#7b6650;
    text-transform:uppercase;
    letter-spacing:.16em;
    font-size:.82rem;
}

.chapter h2{
    margin:.45rem 0 0;
    color:var(--accent);
    font-weight:normal;
    font-size:clamp(1.8rem,4vw,2.8rem);
    line-height:1.15;
}

/* MIOLO DO LIVRO */
.body-text{
    max-width:680px;
    margin:0 auto;
}

.body-text p{
    margin:0 0 .82rem;
    padding:0;
    font-size:1.04rem;
    line-height:1.72;
    text-align:justify;
    text-indent:0;
    hyphens:none;
    overflow-wrap:normal;
    word-break:normal;
}

/* Evita que o navegador quebre palavras de forma feia */
.body-text{
    word-break:normal;
    overflow-wrap:normal;
}

/* Separação elegante entre blocos especiais, caso apareçam */
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

@media(max-width:720px){
    .shell{
        width:min(100%,calc(100% - 18px));
    }

    .toc{
        padding:42px 28px 34px;
    }

    .toc ol{
        columns:1;
    }

    .chapter{
        padding:44px 26px 38px;
    }

    .chapter header{
        margin-bottom:42px;
    }

    .body-text{
        max-width:100%;
    }

    .body-text p{
        font-size:1rem;
        line-height:1.65;
        text-align:left;
        text-indent:0;
        margin-bottom:.9rem;
        hyphens:none;
        overflow-wrap:normal;
        word-break:normal;
    }
}
"""


def titulo_por_nome_arquivo(path):
    nome = path.stem
    nome = re.sub(r"^\d+[-_ ]*", "", nome)
    nome = nome.replace("-", " ").replace("_", " ").strip()

    palavras_minusculas = {
        "a", "o", "as", "os",
        "de", "da", "do", "das", "dos",
        "e", "em", "na", "no", "nas", "nos",
        "que", "se", "para", "por", "com"
    }

    palavras = []
    for palavra in nome.split():
        p = palavra.lower()
        if p in palavras_minusculas:
            palavras.append(p)
        else:
            palavras.append(p.capitalize())

    return " ".join(palavras)


def numero_por_nome_arquivo(path):
    match = re.match(r"^(\d+)", path.stem)
    if not match:
        return 0
    return int(match.group(1))


def md_to_chapter(path):
    text = path.read_text(encoding="utf-8").strip()
    lines = text.splitlines()

    num = None
    title = None
    body_lines = []

    for line in lines:
        clean = line.strip()

        if clean.startswith("# Capítulo"):
            m = re.search(r"(\d+)", clean)
            num = int(m.group(1)) if m else numero_por_nome_arquivo(path)

        elif clean.startswith("## "):
            title = clean[3:].strip()

        else:
            body_lines.append(line)

    if num is None:
        num = numero_por_nome_arquivo(path)

    if not title:
        title = titulo_por_nome_arquivo(path)

    paras = []
    buff = []

    for line in body_lines:
        clean = line.strip()

        if clean:
            buff.append(clean)
        else:
            if buff:
                paras.append(" ".join(buff))
                buff = []

    if buff:
        paras.append(" ".join(buff))

    return {
        "num": num,
        "title": title,
        "paras": paras
    }


def main():
    chapters = [md_to_chapter(p) for p in sorted(CAP_DIR.glob("*.md"))]
    chapters.sort(key=lambda c: c["num"])

    toc = "\n".join(
        f'<li><a href="#cap-{c["num"]}">Capítulo {c["num"]} — {html.escape(c["title"])}</a></li>'
        for c in chapters
    )

    body = []

    for c in chapters:
        paras = "\n".join(
            f"<p>{html.escape(p)}</p>"
            for p in c["paras"]
        )

        body.append(
            f'''
<section class="chapter" id="cap-{c["num"]}">
<header>
<span class="label">Capítulo {c["num"]}</span>
<h2>{html.escape(c["title"])}</h2>
</header>
<div class="body-text">
{paras}
</div>
</section>
'''.strip()
        )

    doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HIRUI NAKI CHISUJI</title>
<style>{CSS}</style>
</head>
<body>
<section class="cover">
<h1>HIRUI<br>NAKI<br>CHISUJI</h1>
</section>

<main class="shell">
<nav class="toc">
<h2>Sumário</h2>
<ol start="0">
{toc}
</ol>
</nav>

{"".join(body)}
</main>

<p class="footer-note">HIRUI NAKI CHISUJI</p>
</body>
</html>"""

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")

    print(f"HTML gerado em: {OUT}")
    print(f"Capítulos: {len(chapters)}")


if __name__ == "__main__":
    main()