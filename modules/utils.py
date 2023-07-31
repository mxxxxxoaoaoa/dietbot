

def validate_markdown(string: str):
    quotes = [
        "`",
        "_",
        "*",
        "~",
        "[",
        "]",
        ">",
        "#",
        "+",
        "=",
        "|",
        "{",
        "}",
        "!",
        "-",
        "(",
        ")",
        "."
    ]
    for quote in quotes:
        string = string.replace(quote, "\{}".format(quote))
    return string