from django.template import TemplateDoesNotExist

import shpaml
from utils import get_django_template_loaders

def get_shpaml_loader(loader):
    if hasattr(loader, 'Loader'):
        baseclass = loader.Loader
    else:
        class baseclass(object):
            def load_template_source(self, *args, **kwargs):
                return loader.load_template_source(*args, **kwargs)
        
    class Loader(baseclass):
        def load_template_source(self, template_name, *args, **kwargs):
            if not template_name.endswith('.shpaml'):
                raise TemplateDoesNotExist(template_name)
            shpaml_source, template_path = super(Loader, self).load_template_source(template_name, *args, **kwargs)
            html = shpaml.convert_text(shpaml_source)
            return html, template_path
        
        load_template_source.is_usable = True
        
    return Loader


shpaml_loaders = dict( (name, get_shpaml_loader(loader)) 
                    for (name, loader) in get_django_template_loaders() )

# for django pre 1.2
backwards_compatible_loaders = dict(
    ("%s_load_template_source" % name, loader().load_template_source)
    for (name, loader) in shpaml_loaders.items()
)
shpaml_loaders.update(backwards_compatible_loaders)
