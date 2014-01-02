"""
Based on django's caching template loader.
"""

import hashlib
from . import shpaml
from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader, get_template_from_string, find_template_loader, make_origin

class Loader(BaseLoader):
    is_usable = True

    def __init__(self, loaders):
        self._loaders = loaders
        self._cached_loaders = []

    @property
    def loaders(self):
        # Resolve loaders on demand to avoid circular imports
        if not self._cached_loaders:
            for loader in self._loaders:
                loader = find_template_loader(loader)
                
                class InnerLoader(loader.__class__):
                    is_usable = True
                    def load_template_source(self, *args, **kwargs):
                        src = super(InnerLoader, self).load_template_source(*args, **kwargs)
                        return (shpaml.convert_text(src[0]), src[1])
                
                self._cached_loaders.append(InnerLoader())
        return self._cached_loaders

    def find_template(self, name, dirs=None):
        if not name.endswith(".shpaml"):
            raise TemplateDoesNotExist(name)
        
        for loader in self.loaders:
            try:
                template, display_name = loader(name, dirs)
                return (template, make_origin(display_name, loader, name, dirs))
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist(name)

    def load_template(self, template_name, template_dirs=None):
        if not template_name.endswith('.shpaml'):
            raise TemplateDoesNotExist(template_name)
        
        template, origin = self.find_template(template_name, template_dirs)
        if not hasattr(template, 'render'):
            try:
                template = get_template_from_string(template, origin, template_name)
            except TemplateDoesNotExist:
                # If compiling the template we found raises TemplateDoesNotExist,
                # back off to returning the source and display name for the template
                # we were asked to load. This allows for correct identification (later)
                # of the actual template that does not exist.
                return template, origin
        
        return template, None
