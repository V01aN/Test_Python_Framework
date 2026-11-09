import re

from utils.phone_specs import PhoneSpecs

_WS = r"[\s\u00a0\u202f]"   # обычный, неразрывный и узкий пробелы

PRICE_RE = re.compile(r"(?:от[\s\u00a0\u202f]+)?(\d[\d\s\u00a0\u202f]*,\d{2})")

def parse_price(price: str) -> float:
    m = PRICE_RE.search(price)
    if not m:
        raise ValueError(f"Не удалось распарсить цену: {price!r}")
    digits = re.sub(_WS, "", m.group(1))       # '10 700,00' -> '10700,00'
    return float(digits.replace(",", "."))

def format_price(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")

SCREEN_RE = re.compile(r"экран\s*(\d+(?:[.,]\d+)?)")

def parse_screen_size(screen_size: str) -> float:
    m = SCREEN_RE.search(screen_size)
    if not m:
        raise ValueError(f"Не удалось распарсить диагональ: {screen_size!r}")
    return float(m.group(1).replace(",", "."))

def format_screen_size(size: float) -> str:
    size = round(size, 3)
    if size == int(size):
        return f'{int(size)}"'
    return f'{size}"'

DIAGONAL_RE  = re.compile(r"экран\s*(\d+(?:[.,]\d+)?)")   # 6.3 / 6,3
RESOLUTION_RE = re.compile(r"\((\d+x\d+)\)")              # (1206x2622)
RAM_RE       = re.compile(r"ОЗУ\s*(\d+)\s*ГБ")            # ОЗУ 12 ГБ

def _line_starting_with(lines: list[str], prefix: str) -> str:
    for ln in lines:
        if ln.startswith(prefix):
            return ln
    raise ValueError(f"Нет строки с префиксом {prefix!r} в: {lines!r}")

def parse_specs(text: str) -> PhoneSpecs:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    m_diag = DIAGONAL_RE.search(_line_starting_with(lines, "экран"))
    m_res  = RESOLUTION_RE.search(_line_starting_with(lines, "экран"))
    m_ram  = RAM_RE.search(_line_starting_with(lines, "ОЗУ"))

    if not (m_diag and m_res and m_ram):
        raise ValueError(f"Не удалось распарсить характеристики: {text!r}")

    return PhoneSpecs(
        os=lines[0],                                   # первая строка — ОС
        diagonal=float(m_diag.group(1).replace(",", ".")),
        resolution=m_res.group(1),
        ram_gb=int(m_ram.group(1)),
    )

