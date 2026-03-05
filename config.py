import os
from dotenv import load_dotenv

load_dotenv()

# URLs
SHEET_URL = os.getenv("SHEET_URL")

WORKSHEET_ACOES = "ações"
WORKSHEET_FIIS = "fiis"
WORKSHEET_FIAGRO = "fiagro"

# Colunas esperadas na planilha
COLUNAS_ACOES = ["VALOR ATUAL", "MIN 52s", "MAX 52s", "D.Y.%", "MEDIA D.Y (5 a)", "P/VP", "P/L", "LPA", "VPA"]
COLUNAS_FIIS = ["VALOR ATUAL", "MIN 52s", "MAX 52s", "D.Y.%", "P/VP"]
COLUNAS_FIAGRO = ["VALOR ATUAL", "MIN 52s", "MAX 52s", "D.Y.%", "P/VP"]
