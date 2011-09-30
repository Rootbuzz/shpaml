import re


_filters = []

def register_filter(regex, priority=100):
    def wrapper(filter):
        filter.priority = priority
        filter.regex = re.compile(regex)
        
        _filters.append(filter)
        _filters = sorted(_filters, key=lambda f: f.priority)
        return filter
    
    return wrapper

def render_shpaml_tree(shpaml_tree):
    output = []
    
    for node in shpaml_tree:
        rendered = render_node(node)
        
        if isinstance(rendered, basestring):
            # Strings go straight into the output list
            output.append(rendered)
        else:
            # iterables have their items appended
            output.extend(rendered)
            
    return "\n".join(output)
        
def render_shpaml_node(node):
    for filter in _filers:
        if filter.regex.match(node.code):
            return filter(node)
