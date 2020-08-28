from typing import List, Dict


def parse_data(data: str, columns: List) -> Dict:
    lst_data = data.split(",")
    return {k: v for k, v in zip(columns, lst_data)}
