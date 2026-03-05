import gspread
from typing import List, Dict


def open_sheet_by_url(gc, url: str, worksheet_name: str):
    sh = gc.open_by_url(url)
    return sh.worksheet(worksheet_name)


def get_header_map(ws) -> Dict[str, int]:
    header = ws.row_values(1)
    return {name.strip().upper(): i+1 for i, name in enumerate(header)}


def iter_tickers(ws, col_map) -> List[Dict]:
    tick_col = col_map.get("TICKER")
    if not tick_col:
        raise RuntimeError("Cabeçalho 'TICKER' não encontrado na linha 1.")


    all_values = ws.get_all_values()
    items = []
    for row_idx in range(2, len(all_values)+1):
        ticker = (all_values[row_idx-1][tick_col-1] or "").strip()
        if not ticker:
            continue
        items.append({"row": row_idx, "ticker": ticker})
    return items


def update_row(ws, row: int, col_map: Dict[str, int], data: Dict[str, str]):
    for k, v in data.items():
        col = col_map.get(k.upper())
        if col:
            ws.update_cell(row, col, v)