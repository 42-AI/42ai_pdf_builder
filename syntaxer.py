import re

IS_MULTILINE = False

def __remove_syntax(string):
    res = re.sub(r'<font[^\>]*>([^<]*)</font>', '\g<1>', string, re.MULTILINE)
    res = re.sub(r'<font[^\>]*>([^<]*)</font>', '\g<1>', res, re.MULTILINE)
    res = re.sub(r'<font[^\>]*>([^<]*)</font>', '\g<1>', res, re.MULTILINE)
    return res

def python(string):
    syntaxed = string
    
    syntaxed = re.sub(
        r'^(>>>)',
        '<font textcolor=#a8a8a8>\g<1></font>',
        syntaxed,
        flags=re.MULTILINE
    )
    
    syntaxed = re.sub(
        r'(?:(?<=^)|(?<=\s))(import|continue|break|yield|return|pass|from|def|return|lambda|as|for|while|with|if|or|and|not|is|in|class)(?=$|\s)',
        '<font textcolor=#cc33ff>\g<1></font>',
        syntaxed,
        flags=re.MULTILINE
    )

    syntaxed = re.sub(
        r'(\w+)(?=\()',
        '<font textcolor=#0099ff>\g<1></font>',
        syntaxed,
    )

    syntaxed = re.sub(
        r'(True|False|None)',
        '<font textcolor=#ff9900>\g<1></font>',
        syntaxed,
    )

    syntaxed = re.sub(
        r'^([^=]*)(#.*)$',
        lambda obj: f'{obj.group(1)}<font textcolor=#a8a8a8>{__remove_syntax(obj.group(2))}</font>',
        syntaxed,
        flags=re.MULTILINE
    )

    syntaxed = re.sub(
        r'((?:\"[^\"]*\")|(?:\'[^\']*\'))',
        lambda obj: f'<font textcolor=#40ff00>{__remove_syntax(obj.group(1))}</font>',
        syntaxed,
        flags=re.DOTALL
    )

    return syntaxed


def default(string):
    syntaxed_string = string

    syntaxed_string = re.sub(
        r'(\$>)',
        '<font textcolor=#a8a8a8>\g<1></font>',
        syntaxed_string,
    )

    return syntaxed_string


syntax_dict = {
    'default': default,
    'language-python': python,
    'language-py': python,
    'language-console': default,
    'language-bash': default,
}

