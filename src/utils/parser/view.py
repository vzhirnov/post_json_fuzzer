import re


def parser_view(text):
    # TODO: are \[| with \]| really need?
    numbers = r"""(?x)(
    \-?\d+|
    (?:www\.|ww2\.)?(?:[\w-]+\.){1,}\w+|
    \w+|
    \+|
    \^|
    \{.*?\}| 
    \[.*?\]| 
    \[\[\]]|
    \[|
    \]
    \b
    )
    """
    a = re.findall(numbers, text)
    res = [x for x in a if x != '']
    return res
