import re


def email_validator(data: str) -> bool:
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return True if re.search(pattern, data) else False
