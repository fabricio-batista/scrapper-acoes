import time
import re
import cloudscraper
from bs4 import BeautifulSoup
import gspread
import json
import html

from collections import defaultdict
from statistics import mean
from config import SHEET_URL, WORKSHEET_ACOES, COLUNAS_ACOES
from sheet_utils import open_sheet_by_url, get_header_map, iter_tickers
from indicators_parser import extract_indicators_from_div


def _br_to_float(s):
    if not s:
        return None
    s = s.replace("R$", "").replace("%", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(s)
    except:
        return None


def _format(val, is_currency=False, is_percent=False, force_str=False):
    if val is None:
        return "N/A"
    if force_str:  # força formato brasileiro com vírgula
        return str(val).replace(".", ",")
    if is_currency:
        return f"R$ {val:.2f}".replace(".", ",")
    if is_percent:
        return f"{val:.2f}%".replace(".", ",")
    return f"{val:.2f}".replace(".", ",")


def get_media_dy_5a_from_html(soup):
    """
    Extrai do input#results os proventos pagos e calcula a média
    anual dos últimos 5 anos (dividendos e JCP somados).
    """
    try:
        input_el = soup.find("input", {"id": "results"})
        if not input_el:
            return "N/A"

        raw_json = input_el["value"]
        decoded = html.unescape(raw_json)
        data = json.loads(decoded)

        por_ano = defaultdict(float)
        for item in data:
            ed = item.get("ed")  # data de pagamento, ex: "21/08/2025"
            valor = item.get("v", 0)
            if ed and valor:
                try:
                    ano = int(ed.split("/")[-1])
                    por_ano[ano] += float(valor)
                except:
                    continue

        # últimos 5 anos
        ultimos5 = sorted(por_ano.keys(), reverse=True)[:5]
        valores = [por_ano[a] for a in ultimos5]

        if not valores:
            return "N/A"

        media = mean(valores)
        return f"{media:.2f}".replace(".", ",")
    except Exception as e:
        print(f"[DEBUG] Erro ao calcular média DY 5a: {e}")
        return "N/A"


def scrape_acoes():
    gc = gspread.service_account(filename="service_account.json")
    ws = open_sheet_by_url(gc, SHEET_URL, WORKSHEET_ACOES)
    col_map = get_header_map(ws)
    rows = iter_tickers(ws, col_map)

    # Montar a matriz para atualizar de uma vez
    all_updates = []

    for item in rows:
        row = item["row"]
        ticker = item["ticker"]
        url = f"https://statusinvest.com.br/acoes/{ticker}"

        try:
            scraper = cloudscraper.create_scraper()
            resp = scraper.get(url, timeout=20)

            # Para salvar na arvore do projeto o HTML para debug
            # with open(f"debug_{ticker}.html", "w", encoding="utf-8") as f:
            #    f.write(resp.text)

            soup = BeautifulSoup(resp.text, "html.parser")

            # Extrair VALOR ATUAL
            valor_atual_el = soup.find("h3", string="Valor atual")
            valor_atual = (
                valor_atual_el.find_next("strong", class_="value").text.strip()
                if valor_atual_el else "N/A"
            )

            # Extrair MIN 52S
            min_52_el = soup.find("h3", string=re.compile("Min\. 52 semanas"))
            min_52 = (
                min_52_el.find_next("strong", class_="value").text.strip()
                if min_52_el else "N/A"
            )

            # Extrair MAX 52S
            max_52_el = soup.find("h3", string=re.compile("Máx\. 52 semanas"))
            max_52 = (
                max_52_el.find_next("strong", class_="value").text.strip()
                if max_52_el else "N/A"
            )

            # Indicadores adicionais
            label_map = {
                "d.y": "D.Y.%",
                "p/vp": "P/VP",
                "p/l": "P/L",
                "lpa": "LPA",
                "vpa": "VPA"
            }
            indicators = extract_indicators_from_div(resp.text, label_map)

            media_dy_5a = get_media_dy_5a_from_html(soup)

            # Prepara lista na mesma ordem de COLUNAS_ACOES
            row_data = [
                valor_atual,
                min_52,
                max_52,
                _format(_br_to_float(indicators["D.Y.%"]), is_percent=True),
                media_dy_5a,
                _format(_br_to_float(indicators["P/VP"])),
                _format(_br_to_float(indicators["P/L"])),
                _format(_br_to_float(indicators["LPA"]), force_str=True),
                _format(_br_to_float(indicators["VPA"]), force_str=True),
            ]

            all_updates.append((row, row_data))
            print(f"[AÇÕES][{row}] {ticker} -> OK")

        except Exception as e:
            print(f"[AÇÕES][{row}] {ticker} -> ERRO: {e}")

        time.sleep(1.0)

    # Atualizar tudo de uma vez no Google Sheets
    try:
        for row, row_data in all_updates:
            start_col = col_map[COLUNAS_ACOES[0]]
            end_col = col_map[COLUNAS_ACOES[-1]]
            range_ = f"{gspread.utils.rowcol_to_a1(row, start_col)}:{gspread.utils.rowcol_to_a1(row, end_col)}"
            ws.update(range_, [row_data])
        print("[AÇÕES] Atualização concluída com sucesso (batch).")
    except Exception as e:
        print(f"[AÇÕES] ERRO ao atualizar planilha em lote: {e}")
