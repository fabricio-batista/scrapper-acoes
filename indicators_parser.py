import re
from bs4 import BeautifulSoup
from typing import Optional, Dict


def extract_indicators_from_div(html: str, label_map: Dict[str, str]) -> Dict[str, Optional[str]]:
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", class_="indicators")
    result = {v: None for v in label_map.values()}

    if div:
        blocks = div.find_all("div", recursive=True)
        for block in blocks:
            try:
                h3 = block.find("h3")
                value = block.find("strong")

                if h3 is None or value is None:
                    continue

                label = h3.get_text(strip=True).lower()
                val = value.get_text(strip=True)

                key = label_map.get(label)
                if key:
                    result[key] = val
            except Exception as e:
                print(f"[DEBUG][EXCEPTION] Erro ao processar bloco: {e}")
                continue

    return result