import re
from datetime import datetime


def format_date(data_nascimento: str) -> datetime:
    if re.search(r"\d{2}/\d{2}/\d{4}", data_nascimento):
        date_format = "%d/%m/%Y"
    else:
        date_format = "%Y/%m/%d"
    return datetime.strptime(data_nascimento, date_format).date()