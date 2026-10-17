# Como publicar o FRSE com GitHub Desktop (Mac)

Este pacote já contém toda a estrutura do repositório, o conteúdo inicial do site e o workflow de publicação. **Não é necessário instalar Python ou Zensical no Mac para publicar:** o GitHub Actions fará a compilação automaticamente.

## Primeira publicação

1. **Descompacte** `frse-ready-to-deploy.zip`. Dentro haverá uma pasta `frse` com arquivos, incluindo a pasta oculta `.github` (não exclua essa pasta).
2. Abra o **GitHub Desktop**, faça login na conta `edson-ao-junior` e vá para **File → New Repository**.
3. Em **Name**, informe `frse`, escolha uma pasta onde o repositório ficará salvo no Mac e clique em **Create Repository**. Não selecione opções para criar README, licença ou gitignore, pois o pacote já tem arquivos equivalentes. Crie na sua pasta habitual de repositórios, e não dentro da pasta extraída do ZIP.
4. No Finder, copie **todo o conteúdo da pasta `frse` extraída**, incluindo a pasta oculta `.github`, para a pasta local `frse` recém-criada pelo GitHub Desktop. Não copie a pasta extraída para dentro dela, ou você terá `frse/frse`. No Finder, use **Command + Shift + .** para visualizar arquivos ocultos, se necessário.
5. Volte ao GitHub Desktop. Na guia **Changes**, confira os arquivos. Informe **Summary** `Initial FRSE research website` e clique em **Commit to main**.
6. Clique em **Publish repository**. Confira que a conta é `edson-ao-junior`, que o nome é **frse**, e **desmarque** a opção **Keep this code private** para que o repositório seja público. Clique em **Publish Repository**.
7. Abra **https://github.com/edson-ao-junior/frse** no navegador. Entre em **Settings → Pages**; em **Build and deployment → Source**, selecione **GitHub Actions**. Você NÃO precisa criar outro workflow: `.github/workflows/docs.yml` já está pronto.
8. Entre na guia **Actions** do repositório, selecione **Publish FRSE website** e clique em **Run workflow**, se necessário. Ao terminar com sucesso, acesse **https://edson-ao-junior.github.io/frse/**.

**Observações:** No primeiro envio, o workflow pode ocorrer antes de habilitar o Pages e falhar. Isso não indica erro do projeto. Depois de escolher GitHub Actions em Settings → Pages, execute-o novamente pela guia Actions. Se você criar o repositório com branch diferente de `main`, renomeie-o para `main` antes de publicar ou ajuste o arquivo `.github/workflows/docs.yml`.

## Para atualizar o site depois

1. Modifique um arquivo `.md` dentro de `docs/` no seu editor favorito, ou edite os arquivos de metadados em `metadata/`.
2. No GitHub Desktop, confira **Changes**, faça **Commit to main** e clique em **Push origin**.
3. O workflow publica a versão atualizada sem intervenções adicionais.

## Onde fazer mudanças

| O que mudar | Arquivo |
| --- | --- |
| Texto inicial, cartões e indicadores da homepage | `docs/index.md` |
| Descrição e perguntas da pesquisa | `docs/overview/` |
| Estudos e seus status | `metadata/studies.json` |
| Publicações e seus status | `metadata/publications.json` |
| Texto detalhado do Study 1 | `docs/studies/s01-multivocal-review/index.md` |
| Roadmap geral | `docs/roadmap/index.md` |
| Funding | `docs/about/funding.md` e `README.md` |
| Cores, cartões e layout | `docs/stylesheets/extra.css` |
| Menus | `zensical.toml` |

**Os catálogos de Estudos, Status e Publicações são gerados automaticamente a partir dos arquivos JSON.** Não edite diretamente `docs/studies/index.md`, `docs/progress/status.md` e `docs/research-outputs/publications.md`, pois serão substituídos no próximo deploy.

## Publicação local opcional

Caso futuramente deseje pré-visualizar o site no Mac antes de enviar:

```bash
python3 -m pip install zensical
python3 scripts/generate_catalog.py
zensical serve
```

Depois abra `http://127.0.0.1:8000/` no navegador.

## Para gerenciar atividades

No navegador, acesse a aba **Projects** do seu perfil GitHub, crie um projeto chamado `FRSE Research Roadmap`, adicione campos como `Work Package`, `Study`, `Status`, `Deliverable`, `Start date` e `Target date`, e vincule issues criadas no repositório `frse`. O GitHub Project não pode ser criado somente com o upload deste ZIP; isso é uma configuração inicial manual.

## Atenção à publicação de materiais

O conteúdo inicial é público e descritivo. **Não** copie protocolos com informações privadas, dados de participantes, manuscritos em avaliação ou PDFs protegidos por direitos autorais diretamente para o repositório público. Antes de disponibilizar dados e código para reutilização, defina licenças específicas e revise direitos e eventuais embargos.
