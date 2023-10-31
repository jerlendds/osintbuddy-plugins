import re
import unicodedata
from typing import List
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


def plugin_source_template(label: str, description: str, author: str) -> str:
    class_name = ''.join(x for x in filter(str.isalnum, label.title()) if not x.isspace())

    return f"""import osintbuddy as ob
from osintbuddy.elements import TextInput

class {class_name}(ob.Plugin):
    label = '{label}'
    icon = 'atom'   # https://tabler-icons.io/
    color = '#FFD166'

    author = '{author}'
    description = '{description}'

    node = [
        TextInput(label='Example', icon='radioactive')
    ]

    @ob.transform(label='To example', icon='atom')
    async def transform_example(self, node, use):
        WebsitePlugin = await ob.Registry.get_plugin('website')
        website_plugin = WebsitePlugin()
        return website_plugin.blueprint(domain=node.example)
"""



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
