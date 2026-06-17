# HIRUI NAKI CHISUJI — Projeto de Revisão

Este projeto organiza a história em formato editável, com o manuscrito separado por capítulos e um gerador de HTML final.

## Objetivo

Manter uma versão principal editável da obra, corrigir furos de roteiro com controle e gerar um HTML de leitura apenas quando o texto estiver pronto.

## Fluxo correto

1. Edite os capítulos em `manuscrito/capitulos/`.
2. Consulte e atualize os arquivos de controle em `lore/`.
3. Rode o script `scripts/gerar_html.py`.
4. Abra `site/index.html` no navegador.

## Regra principal

Não edite o HTML final manualmente, a não ser para teste visual. O texto oficial deve ficar em Markdown.

## Estrutura

```text
hirui-livro-projeto/
├── manuscrito/
│   ├── HIRUI_NAKI_CHISUJI_REVISADO_COMPLETO.md
│   └── capitulos/
├── lore/
│   ├── cronologia.md
│   ├── personagens.md
│   ├── regras-de-poder.md
│   ├── pendencias-de-roteiro.md
│   └── nomes-dos-capitulos.md
├── site/
│   └── index.html
├── scripts/
│   └── gerar_html.py
└── README.md
```

## Comando para gerar HTML

Dentro da pasta do projeto, rode:

```bash
python scripts/gerar_html.py
```

O resultado será atualizado em:

```text
site/index.html
```

## Padrão de escrita

Use prosa de livro. Evite formato de mangá ou roteiro.

Errado:

```text
RIN
— Eu tinha nove anos.

CENA NO FLASHBACK
```

Certo:

```text
Rin puxou a manga para cima, revelando a cicatriz antiga.

— Eu tinha nove anos — disse ela.
```

## Decisões já fixadas

- Goratsu não morre por suicídio.
- Goratsu assassina Daikan por impulso.
- Goratsu tenta assumir o poder, mas vira o senhor de um clã em colapso.
- Takeshi deve evoluir devagar, sem ascensão instantânea.
- A relação de Takeshi com Hana deve crescer como vínculo político e emocional gradual.
- O antigo Capítulo X passa a ser Capítulo 28.
- A primeira parte pode terminar com descoberta maior e casamento/noivado para selar a união dos clãs.
- O final da guerra não deve ser final absoluto: deve abrir espaço para problemas maiores.
