from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CAPITULOS_DIR = ROOT / "manuscrito" / "capitulos"
SAIDA = ROOT / "manuscrito" / "HIRUI_NAKI_CHISUJI_REVISADO_COMPLETO.md"

def deve_ignorar(arquivo: Path) -> bool:
    nome = arquivo.name.lower()

    if not nome.endswith(".md"):
        return True

    if ".backup." in nome or nome.endswith(".backup.md"):
        return True

    if nome.startswith("_"):
        return True

    return False

def main():
    capitulos = sorted(
        arquivo
        for arquivo in CAPITULOS_DIR.glob("*.md")
        if not deve_ignorar(arquivo)
    )

    if not capitulos:
        raise RuntimeError(f"Nenhum capítulo encontrado em: {CAPITULOS_DIR}")

    partes = []

    for indice, capitulo in enumerate(capitulos):
        texto = capitulo.read_text(encoding="utf-8").strip()

        if not texto:
            print(f"Aviso: capítulo vazio ignorado: {capitulo.name}")
            continue

        partes.append(texto)

        if indice < len(capitulos) - 1:
            partes.append("\n\n---\n\n")

    conteudo_final = "".join(partes).rstrip() + "\n"

    SAIDA.write_text(conteudo_final, encoding="utf-8")

    print("Manuscrito geral atualizado com sucesso.")
    print(f"Arquivo gerado: {SAIDA}")
    print(f"Capítulos incluídos: {len(capitulos)}")

    for capitulo in capitulos:
        print(f"- {capitulo.name}")

if __name__ == "__main__":
    main()
