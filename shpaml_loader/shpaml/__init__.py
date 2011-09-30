from .parser import parse_shpaml_tree
from .renderer import render

def convert_text(text_blob):
    tree = parse_shpaml_tree(text_blob)
    return render_shpaml_tree(tree)