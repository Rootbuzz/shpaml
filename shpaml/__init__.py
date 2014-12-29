from .shpaml import convert_text

try:
    from .loader import Loader
    from .loaders import shpaml_loaders as _loaders
  
    locals().update(_loaders)

except ImportError:
  print("Couldn't import django, shpaml.convert_text() is available, django integrations are not")
