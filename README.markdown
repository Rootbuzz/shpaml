The django shpaml template loader uses the official python shpaml implementation
which can be found at http://shpaml.webfactional.com/ 

**Note**: the shpaml implementation from the above link is included for your convenience



## Installation ##

pip install django-shpaml-template-loader

- OR -

Copy the "shpaml_loader" directory into your python path or run ``python
setup.py install``.
  
  - OR -

  pip install django-shpaml-template-loader



## Use ##

The loader wraps existing django template loaders, so any django template loader
can be used to load shpaml templates.

Shpaml templates *must* use the file extension *.shpaml


### Template Loaders ###
  
I am using filesystem, eggs, and app_directories for examples here
but you can use any template loader provided by django
  
FOR DJANGO 1.2+
  - shpaml_loader.filesystem
  - shpaml_loader.eggs
  - shpaml_loader.app_directories
  
FOR DJANGO 1.1 and earlier:
  - shpaml_loader.filesystem_load_template_source
  - shpaml_loader.eggs_load_template_source
  - shpaml_loader.app_directories_load_template_source
     
     
### Setup ###
  
Pick one of the template loaders and add it to your TEMPLATE_LOADERS
setting in the settings.py file like so:
      
    TEMPLATE_LOADERS = (
        # Using the django 1.2+ method in this example
        'shpaml_loader.filesystem',
		    ...
    )
    
The shpaml loader **must be first** or else the django loaders will take 
over.

In django 1.2 I've found that django template caching can yield some 
pretty nice **performance gains**, but it is inconvenien for development 
(because you have to keep clearing the cache).

Here is my reccommended approach:

    TEMPLATE_LOADERS = (
        # whatever shpaml loader you want
        'shpaml_loader.filesystem',
		    ...other template loaders
    )
    
    if not DEBUG:
        TEMPLATE_LOADERS = (
            ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
        )
     
     
### How Templates Are Located ###
  	
There is a shpaml template loader for each built-in django template
loader. The templates are located using the django template loader
but pre-processed to convert the shpaml markup to HTML before being
returned.

Templates are determined to be shpaml by file extension, so they have to
be *.shpaml files or else they will not be processed.
