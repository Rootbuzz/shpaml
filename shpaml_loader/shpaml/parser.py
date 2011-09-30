import re
    
indent_matcher = re.compile(r"(\W*)(.*)\W*")
def parse_indentation(text_blob):
    return [indent_matcher.match(line) for line in text_blob.splitlines() if line]

def parse_shpaml_tree(text_blob):
    parsed = parse_indentation(text_blob)
    output = ShpamlNode()
    
    def recurse(parent, lines):
        current_node = parent.create_node(*lines.pop(0))
        parent.children.append(current_node)
        
        children_to_parse = []
        
        while lines:
            # white space, shpaml notation
            node = parent.create_node(*lines.pop(0))
            
            # skip empty lines
            if not node:
                children_to_parse.append(node)
                continue
            
            if len(node.indent) == len(current_node.indent):
                assert node.indent == current_node.indent, "Mixed indentation on line %s" % node.line_no
                recurse(current_node, children_to_parse)
                parent.children.append(node)
                current_node = node
                
    recurse(output, parsed)
    return output
            

class ShpamlNode(object):
    parent = None
    children = []
    
    def __init__(self, indent=None, code=None):
        self.indent = indent if code else ''
        self.code = code or None
        if indent is None and code is None:
            self.line_count = 0
            self.root_node = self
        
    def __bool__(self): 
        return self.code
    
    def create_node(self, *args, **kwargs):
        node = self.__class__(*args, **kwargs)
        self.root_node.line_count += 1
        node.root_node = self.root_node
        node.line_no = self.root_node.line_count

