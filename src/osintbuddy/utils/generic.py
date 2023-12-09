import re
import unicodedata
from typing import List, Union
from urllib import parse
from pydantic import EmailStr


MAP_KEY = '___obmap___'


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def find_emails(value: str) -> List[EmailStr]:
    emails = []
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", value)
    if match is not None:
        email = match.group(0)
        # if trailing dot, remove. @todo improve regex
        if email[len(email) - 1] == ".":
            emails.append(email[0: len(email) - 2])
        else:
            emails.append(email)
    return list(set(emails))


def to_clean_domain(value: str) -> str:
    if "http://" not in value and "https://" not in value:
        value = "https://" + value
    url = parse.urlparse(value)
    split_domain = url.netloc.split(".")
    if len(split_domain) >= 3:
        split_domain.pop(0)
    domain = ".".join(split_domain)
    return domain


# Slugify and related code is from the Django project, thanks guys!
# Project URL: https://github.com/django/django
# https://github.com/django/django/blob/main/django/utils/text.py
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def to_camel_case(value: str):
    value_list = value.replace(' ', '_').lower().split('_')
    return value_list[0] + ''.join(e.title() for e in value_list[1:])


def to_snake_case(name):
    name = to_camel_case(name.replace('-', '_'))
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

# Convert all keys in dict to snake_case
def dkeys_to_snake_case(data: dict) -> Union[dict, List[dict]]:
    def to_snake(s):
        return re.sub('([A-Z]\w+$)', '_\\1', s).lower()

    if isinstance(data, list):
        return [dkeys_to_snake_case(i) if isinstance(i, (dict, list)) else i for i in data]
    return {to_snake(a):dkeys_to_snake_case(b) if isinstance(b, (dict, list)) else b for a, b in data.items()}
