
import json
import requests
from fake_useragent import UserAgent
from lxml import html

from misc.root import get_root


def get_words() -> list[str]:
    with open(get_root() + "/data/dictionary.json") as jsonfile:
        return json.load(jsonfile)


def parse():
    url = "https://www.wordunscrambler.net/word-list/wordle-word-list"
    headers = {
        "UserAgent": UserAgent().random
    }
    xpath = '//div[@class="content"]/div[@class="light-box text-left"]/ul/li/a/text()'

    response = requests.get(url, headers=headers)
    tree = html.document_fromstring(response.text)
    dictionary: list[str] = tree.xpath(xpath)

    with open(get_root() + "/data/dictionary.json", 'w') as jsonfile:
        json.dump(dictionary, jsonfile)


if __name__ == "__main__":
    parse()
