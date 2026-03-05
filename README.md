# 📊 Scrapper de Ações e FIIs – StatusInvest ➡️ Google Sheets

Este é um projeto pessoal, pensado em me ajudar a tomar decisões no momento de realizar meus investimentos mensais. Percebi que gastava muito tempo para fazer a analise de um unico ativo, de um por um e tomar notas com papel e caneta. Por isso, surgiu a ideia desse projeto.
Este projeto automatiza a coleta de dados financeiros de **ações** e **fundos imobiliários (FIIs)** listados no site [StatusInvest](https://statusinvest.com.br/) e atualiza automaticamente uma planilha no **Google Sheets**.

Com ele você terá dados sempre atualizados sobre seus ativos sem precisar copiar manualmente.  

---

## 📝 Funcionalidades

✅ Scraping de dados **das Ações**:
- Ticker (informado manualmente na planilha, de acordo com o que deseja pesquisar)
- Valor Atual
- Mínimo 52 semanas
- Máximo 52 semanas
- Dividend Yield (%)
- Média Dividend Yield dos últimos 5 anos (para compor a formula de Preço Teto)
- P/VP
- P/L
- LPA (para compor a formula de Preço Justo de Graham)
- VPA (para compor a formula de Preço Justo de Graham)
- Preço Justo de Graham (calculado automaticamente na planilha)
- Preço Teto (calculado automaticamente na planilha)

✅ Scraping de dados **dos FIIs**:
- Ticker (informado manualmente na planilha, de acordo com o que deseja pesquisar)
- Valor Atual
- Mínimo 52 semanas
- Máximo 52 semanas
- Dividend Yield (%)
- P/VP

✅ Scraping de dados **dos FIAGROs**:
- Ticker (informado manualmente na planilha, de acordo com o que deseja pesquisar)
- Valor Atual
- Mínimo 52 semanas
- Máximo 52 semanas
- Dividend Yield (%)
- P/VP

✅ Atualização **em lote (batch)** no Google Sheets para evitar limites de quota do Google.

✅ Conversão automática dos números para formato **brasileiro** (ex: `3,58` em vez de `3.58`) para que a planilha interprete como número.

✅ Configuração centralizada das **colunas** e URLs no arquivo `config.py`.

---

## 🏗 Estrutura do Projeto

```bash
.
├── main.py                 # Menu interativo (buscar ações, FIIs ou tudo)
├── scrapper_acoes.py       # Scraper de ações
├── scrapper_fiis.py        # Scraper de FIIs
├── config.py               # Configuração de colunas e URLs
├── sheet_utils.py          # Funções utilitárias para Google Sheets
├── indicators_parser.py    # Parser dos indicadores HTML
├── service_account.json    # Credenciais do Google Service Account - Precisa ser criado para sua planilha pessoal
└── requirements.txt        # Dependências do projeto
```

---

## ⚙️ Como Configurar
1️⃣ Clonar o repositório
```sh
git clone https://github.com/fabricio-batista/scrapper-acoes
cd scrapper-acoes
```

2️⃣ Criar o ambiente virtual (opcional, mas recomendado)
```bash
python3 -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3️⃣ Instalar as dependências
```bash
pip install -r requirements.txt
```

4️⃣ Criar as credenciais do Google Sheets
```bash
- Vá até o Google Cloud Console
- Crie um projeto e habilite a API do Google Sheets
- Crie um Service Account
- Gere a chave JSON e salve dentro da pasta do projeto como service_account.json
- Gere sua planilha Google Sheet 
    -> Você pode fazer uma cópia do modelo [Google Sheet](https://docs.google.com/spreadsheets/d/18b2vzzzJ07ZaQGE5nJsDWJLzMW3kL8IRIzYURmrTheg/edit?usp=sharing)
- Compartilhe sua planilha com o e-mail do Service Account com permissão de Editor
```

5️⃣ Configurar as URLs e Colunas
```bash
No arquivo config.py, insira:
    -> URL do Google Sheets das ações (SHEET_URL)
    -> Colunas da planilha (já configuradas no projeto)
```
---

## ▶️ Como Usar
    IMPORTANTE: Para que o script faça as buscas corretamente, é necessario preencher manualmente, em cada aba da planilha, os TICKERs que deseja buscar as informaçoes, um por linha.

    Exemplo: 
    Na aba ações, em cada linha da coluna TICKER > 
        BBAS3
        PETR4
        ISAE4

    Na aba FIIs, em cada linha da coluna TICKER > 
        MXRF11
        XPML11
        BTLG11

    Na aba FIIs, em cada linha da coluna TICKER > 
        SNAG11
        RURA11
        RZAG11

    Observação: Os Tickers mencionados acima são meramente para fins de exemplo e NÃO são indicações de investimento.

Execute:
```bash
python3 main.py
```
Você verá o menu:
```bash
Opções: 
[1] - Buscar Ações
[2] - Buscar FIIs
[3] - Buscar FIAGRO
[4] - Atualizar tudo
[X] - Sair
Escolha uma opção:
```
Após escolher a opção, o script fará o scraping e atualizará sua planilha no Google Sheets automaticamente.

---

## 📊 Exemplo de Colunas
Ações:
```bash
TICKER | VALOR|  ATUAL|	MIN 52S| MAX 52S| D.Y.%| MEDIA D.Y (5a)| P/VP | P/L | LPA | VPA
```

FIIs:
```bash
TICKER | VALOR| ATUAL| MIN 52S| MAX 52S| D.Y.%| P/VP
```

FIAGRO:
```bash
TICKER | VALOR| ATUAL| MIN 52S| MAX 52S| D.Y.%| P/VP
```
---

## 🚀 Roadmap Futuro
    - Interface web interativa (dashboard)
    - Alertas automáticos de dividendos
    - Consolidação avançada de histórico

---

## 🛠️ Tecnologias Utilizadas
    Python 3.10+
    Cloudscraper
    BeautifulSoup4
    Gspread
    API do Google Sheets

---

## 📝 Licença
    Este projeto é de uso pessoal/educacional. Respeite os termos do StatusInvest ao utilizar.

---

## 📩 Contato

Dúvidas ou sugestões? Entre em contato com Fabricio Batista.