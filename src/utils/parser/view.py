import re


def parser_view(text):
    numbers = r"""(?x)(
    \#.*?\$|
    \d+\^s|
    \w+\^b|
    [-+]?\d*\.\d+|
    \-?\d+|
    (?:www\.|ww2\.)?(?:[\w-]+\.){1,}\w+|
    \w+|
    \+|
    \*|
    \-|
    \||
    \{.*?\}.*|
    \[+.*?\]+|
    \b
    )
    """
    a = re.findall(numbers, text)
    res = [x for x in a if x != '']  # TODO fix it, get rid of excess quotes in res list
    return res
