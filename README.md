<img src="assets/prof_amr_logo.png" alt="Prof.AMR" height="56">

# Prova Digital Obsidian

Cofre do Obsidian e painel em HTML com julgados do Supremo Tribunal Federal e do Superior Tribunal de Justiça sobre prova digital e cadeia de custódia, organizados por eixo temático, para uso de qualquer agente processual [investigador, acusador, defensor ou julgador].

| Julgados | STJ | STF | Eixos | Termos do Glossário |
|---|---|---|---|---|
| 74 | 71 | 3 | 11 | 93 |

Autor: Alexandre Morais da Rosa [Prof.AMR, [profamr.org](https://www.profamr.org)].

## Dois Modos de Uso

| Modo | Exigência | Caminho |
|---|---|---|
| Painel em HTML | Navegador | [Abrir o painel](https://profamr404.github.io/prova-digital-obsidian/) |
| Cofre do Obsidian | Obsidian instalado no computador | Passos 1 a 4 abaixo |

O painel em HTML traz as abas Ementas, Grafo, Glossário de Termos, Base Legal e Instruções de Uso. O cofre traz o mesmo conteúdo em notas ligadas entre si, com busca, grafo e edição no próprio computador.

## Passo 1: Instalar o Obsidian

O Obsidian é um editor de notas em Markdown. As notas ficam em uma pasta do computador, chamada cofre [*vault*].

1. Abrir a página [Download Obsidian](https://obsidian.md/download).
2. Windows: em **Windows**, clicar em **Universal**, abrir o arquivo baixado e seguir as instruções.
3. macOS: em **macOS**, clicar em **Universal**, abrir o arquivo baixado e arrastar o Obsidian para a pasta Aplicativos.
4. Linux: escolher **AppImage**, **Snap** ou Flatpak, conforme a [documentação oficial de instalação](https://obsidian.md/help/install).

## Passo 2: Baixar o Cofre

1. Clicar em [Download ZIP](https://github.com/ProfAMR404/prova-digital-obsidian/archive/refs/heads/main.zip), ou no botão verde **Code** desta página e depois em **Download ZIP**.
2. Extrair o arquivo `.zip` em uma pasta do computador [exemplo: Documentos].
3. Localizar, dentro da pasta extraída, a pasta `Cofre-Prova-Digital`. A pasta `Cofre-Prova-Digital` é o cofre.

## Passo 3: Abrir o Cofre no Obsidian

1. Abrir o Obsidian.
2. Na tela de cofres, ao lado de **Open folder as vault** [Abrir pasta como cofre], clicar em **Open**.
3. Selecionar a pasta `Cofre-Prova-Digital` e confirmar.
4. Com outro cofre já aberto: clicar no nome do cofre, no canto inferior esquerdo, escolher **Manage vaults** e repetir os itens 2 e 3.

O rótulo dos botões acompanha o idioma da interface do Obsidian. Fonte dos passos: [Manage vaults](https://obsidian.md/help/manage-vaults).

## Passo 4: Plugins

O cofre usa só recursos nativos do Obsidian [links entre notas, propriedades, blocos recolhíveis, busca e grafo]. Nenhum plugin precisa ser instalado.

## Navegação no Cofre

| Onde | Conteúdo |
|---|---|
| `Painel de Ementas Prova Digital` | Página inicial, com o Sumário dos Eixos e as entradas do cofre |
| `00 Painel` | Nota "Abrir o Painel", painel em HTML, dados em JSON e gerador do cofre |
| `Eixos` | 11 eixos temáticos; o Eixo 11 divide a quebra da cadeia de custódia em seis subgrupos |
| `Julgados` | 74 notas, uma por julgado, com citação, link do inteiro teor e ementa em transcrição literal dentro de bloco recolhível |
| `Relatores` e `Órgãos Julgadores` | Julgados de cada relator e de cada órgão |
| `Base Legal` | Dispositivos do CPP e súmulas com transcrição literal; links dos Procedimentos Operacionais Padrão de perícia do MJSP |
| `Glossário` | 93 termos digitais, cada termo com os julgados que mencionam o termo |
| `Todos os Julgados` | Tabela geral com relator, órgão, data e eixo |

Recursos do Obsidian para o estudo:

1. **Grafo** [*Graph view*]: mostra as ligações entre julgados, eixos, relatores, dispositivos, termos e precedentes citados.
2. **Busca** [*Search*]: localiza palavra ou expressão em todas as ementas.
3. **Links reversos** [*Backlinks*]: lista, em cada nota, as notas que apontam para a nota aberta.
4. **Propriedades e tags**: cada julgado traz tribunal, classe, relator, órgão, datas e eixo; as tags `tribunal/stj`, `tribunal/stf` e `eixo/01` a `eixo/11` filtram a busca.

## Conteúdo do Repositório

| Item | Descrição |
|---|---|
| `index.html` | Painel em HTML, servido em [profamr404.github.io/prova-digital-obsidian](https://profamr404.github.io/prova-digital-obsidian/) |
| `Cofre-Prova-Digital/` | Cofre do Obsidian |
| `Cofre-Prova-Digital/00 Painel/painel.json` | Dados do painel: julgados, eixos, glossário, base legal e normas |
| `Cofre-Prova-Digital/00 Painel/gen_vault.py` | Gerador do cofre a partir do JSON |
| `LICENSE` | Texto da licença CC BY 4.0 |

## Regeneração do Cofre

O gerador recria as notas a partir de `painel.json`. O comando sobrescreve as notas geradas. Requisito: Python 3.

```bash
cd Cofre-Prova-Digital
python3 "00 Painel/gen_vault.py" "00 Painel/painel.json" . https://profamr404.github.io/prova-digital-obsidian/
```

## Fontes dos Textos

As ementas reproduzem o texto dos acórdãos, em transcrição literal, com link para o inteiro teor no portal do tribunal em cada item. Os dispositivos do Código de Processo Penal e os enunciados de súmula reproduzem o texto oficial, com link para a fonte.

## Licença

A organização em eixos, o glossário, as notas e o código deste repositório ficam sob a licença [Creative Commons Atribuição 4.0 Internacional, CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pt-br). Atribuição: Alexandre Morais da Rosa, Prova Digital Obsidian, profamr.org. Os textos de acórdãos, leis e súmulas pertencem às fontes oficiais indicadas.

## Referências

- OBSIDIAN. *Download and install Obsidian*. Disponível em: <https://obsidian.md/help/install>. Acesso em: 11 nov. 2026.
- OBSIDIAN. *Manage vaults*. Disponível em: <https://obsidian.md/help/manage-vaults>. Acesso em: 11 nov. 2026.
