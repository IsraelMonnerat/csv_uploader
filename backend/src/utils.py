import re
from datetime import datetime


def format_date(value_data: str) -> datetime:
    if re.search(r"\d{2}/\d{2}/\d{4}", value_data):
        date_format = "%d/%m/%Y"
    else:
        date_format = "%Y/%m/%d"
    return datetime.strptime(value_data, date_format).date()


def format_date_ymd_to_ymd(value_data: str) -> str:
    try:
        date_object = datetime.strptime(value_data, "%Y-%m-%d")
        return date_object.strftime("%Y/%m/%d")
    except ValueError:
        raise ValueError("Formato de data inválido. Esperado YYYY-MM-DD.")