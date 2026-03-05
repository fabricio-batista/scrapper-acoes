import time
import re
import cloudscraper
from bs4 import BeautifulSoup
import gspread
import random

from config import SHEET_URL, WORKSHEET_FIIS, COLUNAS_FIIS
from sheet_utils import open_sheet_by_url, get_header_map, iter_tickers


def _br_to_float(s):
    if not s:
        return None
    s = s.replace("R$", "").replace("%", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(s)
    except:
        return None


def _format(val, is_currency=False, is_percent=False):
    if val is None:
        return "N/A"
    if is_currency:
        return f"R$ {val:.2f}".replace(".", ",")
    if is_percent:
        return f"{val:.2f}%".replace(".", ",")
    return f"{val:.2f}".replace(".", ",")


def scrape_fiis():
    gc = gspread.service_account(filename="service_account.json")
    ws = open_sheet_by_url(gc, SHEET_URL, WORKSHEET_FIIS)
    col_map = get_header_map(ws)
    rows = iter_tickers(ws, col_map)

    all_updates = []

    for item in rows:
        row = item["row"]
        ticker = item["ticker"]
        url = f"https://statusinvest.com.br/fundos-imobiliarios/{ticker}"

        try:
            scraper = cloudscraper.create_scraper()
            resp = scraper.get(url, timeout=20)

            # Para salvar na arvore do projeto o HTML para debug
            # with open(f"debug_{ticker}.html", "w", encoding="utf-8") as f:
            #     f.write(resp.text)

            soup = BeautifulSoup(resp.text, "html.parser")

            # === BLOCOS DE EXTRAÇÃO ===
            def find_val(label):
                h3 = soup.find("h3", string=re.compile(label, re.IGNORECASE))
                if h3:
                    val = h3.find_next("strong", class_="value")
                    return val.text.strip() if val else "N/A"
                return "N/A"

            valor_atual = find_val("Valor atual")
            min_52 = find_val("Min. 52 semanas")
            max_52 = find_val("Máx. 52 semanas")

            # ===== Dividend Yield (estrutura específica) =====
            dy_block = soup.find("div", title=re.compile("Dividend Yield com base", re.IGNORECASE))
            dy_value = "N/A"
            if dy_block:
                val_tag = dy_block.find("strong", class_="value")
                if val_tag:
                    dy_value = val_tag.text.strip()

            pvp = find_val("P/VP")

            # === FORMATANDO EM LISTA ===
            row_data = [
                valor_atual,
                min_52,
                max_52,
                _format(_br_to_float(dy_value), is_percent=True),
                _format(_br_to_float(pvp)),
            ]

            all_updates.append((row, row_data))
            print(f"[FIIS][{row}] {ticker} -> OK")

            time.sleep(random.uniform(1.5, 3))  # para evitar bloqueios no site

        except Exception as e:
            print(f"[FIIS][{row}] {ticker} -> ERRO: {e}")
            time.sleep(2)

    # Atualizar tudo em batch no Google Sheets
    try:
        for row, row_data in all_updates:
            start_col = col_map[COLUNAS_FIIS[0]]
            end_col = col_map[COLUNAS_FIIS[-1]]
            range_ = f"{gspread.utils.rowcol_to_a1(row, start_col)}:{gspread.utils.rowcol_to_a1(row, end_col)}"
            ws.update(range_, [row_data])
        print("[FIIS] Atualização concluída com sucesso (batch).")
    except Exception as e:
        print(f"[FIIS] ERRO ao atualizar planilha em lote: {e}")
