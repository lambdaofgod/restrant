#!/usr/bin/env python3
import requests
from urllib.parse import urlparse
from enum import Enum
from pathlib import Path


URLType = Enum("URLType", ["LocalFile", "HTTPURL"])


def get_type(url):
    try:
        result = urlparse(url)
        return URLType.HTTPURL
    except ValueError:
        p = Path(url)
        if p.expanduser().exists():
            return URLType.LocalFile
        else:
            raise NotImplementedError(f"Invalid URL type: {url}")


def load_code(code_url):
    url_type = get_type(code_url)

    if url_type is URLType.LocalFile:
        with open(code_url, "r") as file:
            code = file.read()
    elif url_type is URLType.HTTPURL:
        response = requests.get(code_url)
        if response.status_code == 200:
            code = response.text
        else:
            print(
                f"Error: Unable to fetch code from URL. Status code: {response.status_code}"
            )
    return code
