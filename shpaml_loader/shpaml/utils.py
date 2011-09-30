import re


DIV_SHORTCUT = re.compile(r'^(?:#|(?:\.(?!\.)))')
TAG_WHITESPACE_ATTRS = re.compile('(\S+)([ \t]*?)(.*)')
AUTO_QUOTE = re.compile("""([ \t]+[^ \t=]+=)(""" + quotedText + """|[^ \t]+)""")

def django_sugar(tag):
    start_tag = '{%% %s %%}' % tag
    end_tag = '{%% end%s %%}' % tag.split(" ")[0]
    return (start_tag, end_tag)

def jquery_sugar(markup):
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

def jfixdots(a): 
    return fixdots(' '.join(a))

def fixdots(s): 
    return s.replace('..', '.')

def tag_and_rest(tag):
    m = TAG_AND_REST.match(tag)
    if m:
        return fixdots(m.group(1)), m.group(2)
    else:
        return fixdots(tag), None
    
def AUTO_QUOTE_ATTRIBUTES(attrs):
    def _sub(m):
        attr = m.group(2)
        if attr[0] in "\"'":
            return m.group(1) + attr
        return m.group(1) + '"' + attr + '"'
    return re.sub(AUTO_QUOTE, _sub, attrs)