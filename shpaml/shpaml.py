import re

__version__ = '1.00b'

def convert_text(in_body):
    '''

    You can call convert_text directly to convert shpaml markup
    to HTML markup.
    '''
    return convert_shpaml_tree(in_body)


PASS_SYNTAX = 'PASS'
FLUSH_LEFT_SYNTAX = '|| '
FLUSH_LEFT_EMPTY_LINE = '||'
TAG_WHITESPACE_ATTRS = re.compile('(\S+)([ \t]*?)(.*)')
TAG_AND_REST = re.compile(r'((?:[^ \t\.#]|\.\.)+)(.*)')
CLASS_OR_ID = re.compile(r'([.#])((?:[^ \t\.#]|\.\.)+)')
COMMENT_SYNTAX = re.compile(r'^::comment$')
VERBATIM_SYNTAX = re.compile('(.+) VERBATIM$')
DJANGO_TAG_SYNTAX = re.compile(r'^%[ \t]*(.+)')

DIV_SHORTCUT = re.compile(r'^(?:#|(?:\.(?!\.)))')


quotedText = r"""(?:(?:'(?:\\'|[^'])*')|(?:"(?:\\"|[^"])*"))"""
AUTO_QUOTE = re.compile("""([ \t]+[^ \t=]+=)(""" + quotedText + """|[^ \t]+)""")
def AUTO_QUOTE_ATTRIBUTES(attrs):
    def _sub(m):
        attr = m.group(2)
        if attr[0] in "\"'":
            return m.group(1) + attr
        return m.group(1) + '"' + attr + '"'
    return re.sub(AUTO_QUOTE, _sub,attrs)

def syntax(regex):
    def wrap(f):
        f.regex = re.compile(regex)
        return f
    return wrap

@syntax('([ \t]*)(.*)')
def INDENT(m):
    prefix, line = m.groups()
    line = line.rstrip()
    if line == '':
        prefix = ''
    return prefix, line

@syntax('^([<{\(\)]\S.*)')
def RAW_HTML(m):
    return m.group(1).rstrip()

@syntax('= ?(.*)')
def DJANGO_VAR(m):
    return "{{ %s }}" % m.group(1).rstrip()

@syntax('%[ \t]*(.*)')
def DJANGO_TAG(m):
    return "{%% %s %%}" % m.group(1).rstrip()

@syntax('^\| (.*)')
def TEXT(m):
    return m.group(1).rstrip()

@syntax('(.*?) > (.*)')
def OUTER_CLOSING_TAG(m):
    tag, text = m.groups()
    text = convert_line(text)
    return enclose_tag(tag, text)

@syntax('(.*?) \|= (.*)')
def DJANGO_VAR_ENCLOSING_TAG(m):
    tag, text = m.groups()
    text = "{{ %s }}" % text.strip()
    return enclose_tag(tag, text)

@syntax('%(.*) \| (.*)')
def TEXT_ENCLOSING_DJANGO_TAG(m):
    tag, text = m.groups()
    return enclose_django_tag(tag, text)

@syntax('%(.*) \|= (.*)')
def DJANGO_VAR_ENCLOSING_DJANGO_TAG(m):
    tag, text = m.groups()
    text = "{{ %s }}" % text.strip()
    return enclose_django_tag(tag, text)

@syntax('%(.*) \|% (.*)')
def DJANGO_TAG_ENCLOSING_DJANGO_TAG(m):
    tag, text = m.groups()
    text = "{%% %s %%}" % text.strip()
    return enclose_django_tag(tag, text)

@syntax('%[ \t]*(.*) \|\|')
def EMPTY_DJANGO_TAG(m):
    tag = m.groups()[0]
    return enclose_django_tag(tag, "")

@syntax('(.*?) \|\|')
def EMPTY_TAG(m):
    tag = m.groups()[0]
    return enclose_tag(tag, "")

@syntax('(.*?) \|% (.*)')
def DJANGO_TAG_ENCLOSING_TAG(m):
    tag, text = m.groups()
    text = "{%% %s %%}" % text.strip()
    return enclose_tag(tag, text)

@syntax('(.*?) \| (.*)')
def TEXT_ENCLOSING_TAG(m):
    tag, text = m.groups()
    return enclose_tag(tag, text)

@syntax('> (.*)')
def SELF_CLOSING_TAG(m):
    tag = m.group(1).strip()
    return '<%s>' % apply_jquery(tag)[0]

@syntax('(.*)')
def RAW_TEXT(m):
    return m.group(1).rstrip()

LINE_METHODS = [
        RAW_HTML,
        DJANGO_VAR,
        EMPTY_DJANGO_TAG,
        TEXT_ENCLOSING_DJANGO_TAG,
        DJANGO_TAG_ENCLOSING_DJANGO_TAG,
        DJANGO_VAR_ENCLOSING_DJANGO_TAG,
        DJANGO_TAG,
        TEXT,
        OUTER_CLOSING_TAG,
        DJANGO_TAG_ENCLOSING_TAG,
        DJANGO_VAR_ENCLOSING_TAG,
        EMPTY_TAG,
        TEXT_ENCLOSING_TAG,
        SELF_CLOSING_TAG,
        RAW_TEXT,
        ]


def convert_shpaml_tree(in_body):
    """Returns HTML as a basestring.

    Parameters
    ----------

      in_body : basestring
        SHPAML source code.

    Implementation Notes
    --------------------

    This is just a wrapper around the indent function, which requires
    a bunch of other arguments that specify various characteristics
    about the language we are trying to parse. This function just
    passes in values that are specific to SHPAML.
    """
    return indent(in_body,
            branch_method=html_block_tag,
            leaf_method=convert_line,
            pass_syntax=PASS_SYNTAX,
            flush_left_syntax=FLUSH_LEFT_SYNTAX,
            flush_left_empty_line=FLUSH_LEFT_EMPTY_LINE,
            indentation_method=find_indentation)

def html_block_tag(output, block, recurse):
    append = output.append
    prefix, tag = block[0]
    if RAW_HTML.regex.match(tag):
        append(prefix + tag)
        recurse(block[1:])
    elif COMMENT_SYNTAX.match(tag):
        pass
    elif VERBATIM_SYNTAX.match(tag):
        m = VERBATIM_SYNTAX.match(tag)
        tag = m.group(1).rstrip()
        start_tag, end_tag = apply_jquery_sugar(tag)
        append(prefix + start_tag)
        stream(append, block[1:])
        append(prefix + end_tag)
    elif DJANGO_TAG_SYNTAX.match(tag):
        m = DJANGO_TAG_SYNTAX.match(tag)
        tag = m.group(1).rstrip()
        start_tag, end_tag = apply_django_sugar(tag)
        append(prefix + start_tag)
        recurse(block[1:])
        append(prefix + end_tag)
    else:
        start_tag, end_tag = apply_jquery_sugar(tag)
        append(prefix + start_tag)
        recurse(block[1:])
        append(prefix + end_tag)

def stream(append, prefix_lines):
    for prefix, line in prefix_lines:
        if line == '':
            append('')
        else:
            append(prefix + line)

def convert_line(line):
    prefix, line = find_indentation(line.strip())
    for method in LINE_METHODS:
        m = method.regex.match(line)
        if m:
            return prefix + method(m)

def apply_django_sugar(tag):
    start_tag = '{%% %s %%}' % tag
    end_tag = '{%% end%s %%}' % tag.split(" ")[0]
    return (start_tag, end_tag)

def apply_jquery_sugar(markup):
    if DIV_SHORTCUT.match(markup):
        markup = 'div' + markup
    start_tag, tag = apply_jquery(markup)
    return ('<%s>' % start_tag, '</%s>' % tag)

def apply_jquery(markup):
    tag, whitespace, attrs = TAG_WHITESPACE_ATTRS.match(markup).groups()
    tag, rest = tag_and_rest(tag)
    ids, classes = ids_and_classes(rest)
    attrs = AUTO_QUOTE_ATTRIBUTES(attrs)
    if classes:
        attrs += ' class="%s"' % classes
    if ids:
        attrs += ' id="%s"' % ids
    start_tag = tag + whitespace + attrs
    return start_tag, tag

def ids_and_classes(rest):

    if not rest: return '', ''

    ids = []
    classes=[];

    def _match(m):
        if m.group(1) == '#':
            ids.append(m.group(2))
        else:
            classes.append(m.group(2))

    CLASS_OR_ID.sub(_match, rest)
    return jfixdots(ids), jfixdots(classes)

def jfixdots(a): return fixdots(' '.join(a))
def fixdots(s): return s.replace('..', '.')


def tag_and_rest(tag):
    m = TAG_AND_REST.match(tag)
    if m:
        return fixdots(m.group(1)), m.group(2)
    else:
        return fixdots(tag), None

def enclose_tag(tag, text):
    start_tag, end_tag = apply_jquery_sugar(tag)
    return start_tag + text + end_tag

def enclose_django_tag(tag, text):
    start_tag, end_tag = apply_django_sugar(tag)
    return start_tag + text + end_tag

def find_indentation(line):
    """Returns a pair of basestrings.

    The first consists of leading spaces and tabs in line. The second
    is the remainder of the line with any trailing space stripped off.

    Parameters
    ----------

      line : basestring
    """
    return INDENT(INDENT.regex.match(line))

############ Generic indentation stuff follows

def get_indented_block(prefix_lines):
    """Returns an integer.

    The return value is the number of lines that belong to block begun
    on the first line.

    Parameters
    ----------

      prefix_lines : list of basestring pairs
        Each pair corresponds to a line of SHPAML source code. The
        first element of each pair is indentation. The second is the
        remaining part of the line, except for trailing newline.
    """
    prefix, line = prefix_lines[0]
    len_prefix = len(prefix)

    # Find the first nonempty line with len(prefix) <= len(prefix)
    i = 1
    while i < len(prefix_lines):
        new_prefix, line = prefix_lines[i]
        if line and len(new_prefix) <= len_prefix:
            break
        i += 1

    # Rewind to exclude empty lines
    while i-1 > 0 and prefix_lines[i-1][1] == '':
        i -= 1

    return i

def indent(text,
            branch_method,
            leaf_method,
            pass_syntax,
            flush_left_syntax,
            flush_left_empty_line,
            indentation_method,
            get_block = get_indented_block,
            ):
    """Returns HTML as a basestring.

    Parameters
    ----------

      text : basestring
        Source code, typically SHPAML, but could be a different (but
        related) language. The remaining parameters specify details
        about the language used in the source code. To parse SHPAML,
        pass the same values as convert_shpaml_tree.

      branch_method : function
        convert_shpaml_tree passes html_block_tag here.
      leaf_method : function
        convert_shpaml_tree passes convert_line here.

      pass_syntax : basestring
        convert_shpaml_tree passes PASS_SYNTAX here.
      flush_left_syntax : basestring
        convert_shpaml_tree passes FLUSH_LEFT_SYNTAX here.
      flush_left_empty_line : basestring
        convert_shpaml_tree passes FLUSH_LEFT_EMPTY_LINE here.

      indentation_method : function
        convert_shpaml_tree passes INDENT here.

      get_block : function
        Defaults to get_indented_block.
    """
    text = text.rstrip()
    lines = text.split('\n')
    output = []
    indent_lines(
            lines,
            output,
            branch_method,
            leaf_method,
            pass_syntax,
            flush_left_syntax,
            flush_left_empty_line,
            indentation_method,
            get_block = get_indented_block,
            )
    return '\n'.join(output) + '\n'

def indent_lines(lines,
            output,
            branch_method,
            leaf_method,
            pass_syntax,
            flush_left_syntax,
            flush_left_empty_line,
            indentation_method,
            get_block,
            ):
    """Returns None.

    The way this function produces output is by adding strings to the
    list that's passed in as the second parameter.

    Parameters
    ----------

      lines : list of basestring's
        Each string is a line of a SHPAML source code
        (trailing newlines not included).
      output : empty list
        Explained earlier...

    The remaining parameters are exactly the same as in the indent
    function:

      * branch_method
      * leaf_method
      * pass_syntax
      * flush_left_syntax
      * flush_left_empty_line
      * indentation_method
      * get_block
    """
    append = output.append
    def recurse(prefix_lines):
        while prefix_lines:
            prefix, line = prefix_lines[0]
            if line == '':
                prefix_lines.pop(0)
                append('')
                continue

            block_size = get_block(prefix_lines)
            if block_size == 1:
                prefix_lines.pop(0)
                if line == pass_syntax:
                    pass
                elif line.startswith(flush_left_syntax):
                    append(line[len(flush_left_syntax):])
                elif line.startswith(flush_left_empty_line):
                    append('')
                else:
                    append(prefix + leaf_method(line))
            else:
                block = prefix_lines[:block_size]
                prefix_lines = prefix_lines[block_size:]
                branch_method(output, block, recurse)
        return
    prefix_lines = list(map(indentation_method, lines))
    recurse(prefix_lines)

if __name__ == "__main__":
    # if file name is given convert file, else convert stdin
    import sys
    if len(sys.argv) == 2:
        shpaml_text = open(sys.argv[1]).read()
    else:
        shpaml_text = sys.stdin.read()
    sys.stdout.write(convert_text(shpaml_text))
