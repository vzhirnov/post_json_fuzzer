import re


#        \b(?:www\.|ww2\.)?((?:[\w-]+\.){1,}\w+)\b|
def parser_view(text):
    # TODO: are \[| with \]| really need?
    numbers = r"""(?x)(
    \d+|
    \w+|
    \*|
    \+|
    \^|
    \{.*?\}| 
    \[.*?\]| 
    \[\[\]]|
    \[|
    \]|
    \b
    )
    """
    a = re.findall(numbers, text)
    res = [x for x in a if x != '']
    return res
