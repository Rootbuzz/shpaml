## Installation ##

pip install django-shpaml

- OR -

Copy the "shpaml" directory into your python path or run ``python
setup.py install``.


## Use ##

The loader wraps existing django template loaders, so any django template loader
can be used to load shpaml templates.

Shpaml templates *must* use the file extension *.shpaml


### Template Loaders ###
  
I am using filesystem and app_directories for examples here
but you can use any template loader provided by django
  
FOR DJANGO 1.2+

Shapml Loader wraps other loaders (like the caching loader)

    TEMPLATE_LOADERS = (
        ('shpaml.Loader',
            ('django.template.loaders.filesystem.Loader',)
        ),
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
    
if you want Caching as well (recommended)...

    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader',
            ('shpaml.Loader',
                ('django.template.loaders.filesystem.Loader',)
            ),
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )
    )     
     
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

In django template caching can yield some 
pretty nice **performance gains**, but it is inconvenient for development 
(because you have to keep clearing the cache).

Here is my reccommended approach:

    TEMPLATE_LOADERS = (
        ('shpaml.Loader',
            ('django.template.loaders.filesystem.Loader',)
        ),
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
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


## Shpaml ##

Here is a quick and dirty shpaml reference...

### Use indentation for block tags

The goal of this tutorial is to take you through one SHPAML concept at a time. 
At each step you can edit the SHPAML to create HTML. The goal is to learn by 
reading and writing at the same time.

The most important concept in SHPAML is that you can use indentation to indicate
where HTML blocks should end with a close tag. Try adding a third item to the 
list to see it in action.

We will mostly use two spaces for indentation in this tutorial, but you can use
more if you like.

    ul
      li
        This it the first item.
      li
        This is the second item.
    
    div
        The number of spaces that you indent
        gets preserved.
        
#### Output

    <ul>
      <li>
        This it the first item.
      </li>
      <li>
        This is the second item.
      </li>
    </ul>
    
    <div>
        The number of spaces that you indent
        gets preserved.
    </div>


### Use pipes for inline content

For HTML one-liners you can use the pipe character followed by a space to 
separate markup from content.

Try adding an item to this list.

    ol
      li | apple
      li | banana
      li | orange
      
#### Output

    <ol>
      <li>apple</li>
      <li>banana</li>
      <li>orange</li>
    </ol>
      
### Use pipes for indented content 

When authoring SHPAML, you use indentation and certain punctuation to identify 
structure. This leads to terseness at one level, but what if you want your 
content to include indentation and structure?

The solution is to prefix content lines with the pipe character ('|') followed 
by a space. Try removing the second pipe to see the problem, and then reinsert 
it to see the solution.

    pre
      | Without pipes to show a block of content,
      |  SHPAML would be confused
      |    by this strangely indented
      |       text, or by me using | and
      |          < symbols.
    
    pre
      || You can also dedent text
      ||   with double pipes
    
    p
      For most text, advanced users can omit the
      pipes for maximum terseness, and SHPAML will
      just do the right thing.  It detects that lines
      have no indentation beneath them and treats them
      as content.
      
#### Output

    <pre>
      Without pipes to show a block of content,
       SHPAML would be confused
         by this strangely indented
            text, or by me using | and
               < symbols.
    </pre>
    
    <pre>
    You can also dedent text
      with double pipes
    </pre>
    
    <p>
      For most text, advanced users can omit the
      pipes for maximum terseness, and SHPAML will
      just do the right thing.  It detects that lines
      have no indentation beneath them and treats them
      as content.
    </p>
    
### Use HTML as needed 

SHPAML does not force you to abandon HTML.

Most well-formatted HTML passes through the preprocessor untouched. This can 
be helpful when dealing with legacy code or inline tags.

    <head>
      <meta http-equiv="Content-Language" content="en-us" />
    </head>
    
    body
      <div class="legacy">
        <ol>
          <li>close tags</li>
          <li>lots of angle brackets</li>
        </ol>
      </div>
    
      div class="mixed"
        p
          Use <b>indentation</b> to denote
          structure!

#### Output

    <head>
      <meta http-equiv="Content-Language" content="en-us" />
    </head>
    
    <body>
      <div class="legacy">
        <ol>
          <li>close tags</li>
          <li>lots of angle brackets</li>
        </ol>
      </div>
    
      <div class="mixed">
        <p>
          Use <b>indentation</b> to denote
          structure!
        </p>
      </div>
    </body>

### Use dot for class=... 

You can abbreviate 'div class="free_text"' as "div.free_text" as shown in the 
example.

Although it reduces typing for the HTML author, the real goal here is to make 
the HTML look more like CSS (for your designer) and jQuery too.

Try modifying the ul tag to emulate the same syntax as the div.

    div.free_text
      This is some text.
    
    ul class="list_of_names"
      li | Alice
      li | Bob
      li | Cindy
    
    div.class1.class2
      You can have multiple classes.
      
#### Output

    <div class="free_text">
      This is some text.
    </div>
    
    <ul class="list_of_names">
      <li>Alice</li>
      <li>Bob</li>
      <li>Cindy</li>
    </ul>
    
    <div class="class1 class2">
      You can have multiple classes.
    </div>
    
### Use pound for id=...

You can abbreviate 'p class="free_text" id="greeting"' as "p.free_text#greeting" 
as shown in the example.

Try adding an id to the ul tag.

    p.free_text#greeting
      Hello World!
    
    ul.list_of_names
      li | Alice
      li | Bob
      li | Cindy
      
#### Output

    <p class="free_text" id="greeting">
      Hello World!
    </p>
    
    <ul class="list_of_names">
      <li>Alice</li>
      <li>Bob</li>
      <li>Cindy</li>
    </ul>
    
### Div can be implied 

Any tag starting with "." is implied to be a div tag. The div shortcut is a 
feature borrowed from haml, as divs are used very commonly.

Try enclosing "Goodbye" inside a div tag using the implied-div syntax.

    .free_text.salutation#hello
      Hello World!
    
    #how_are_you.free_text.salutation
     How are you?
    
    Goodbye.
    
#### Output

    <div class="free_text salutation" id="hello">
      Hello World!
    </div>
    
    <div class="free_text salutation" id="how_are_you">
     How are you?
    </div>
    
    Goodbye.
    
### Comments

You can use the ::comment directive to include comments in your shpaml. 
Comments do not get written to the output.

    ::comment
      This text is for your eyes only.
    .main
      This text passes through.

#### Output

<div class="main">
  This text passes through.
</div>

### Use > for self-closing tags 

You can use '>' syntax for self-closing tags like "br" and "hr," or you can 
just use explicit HTML.

    > br
    <br />
    <br>
    <input type="text" class="widget" />
    > input.widget type="text"
    
#### Output

    <br />
    <br />
    <br>
    <input type="text" class="widget" />
    <input type="text" class="widget" />
    
### Empty Tags

Sometimes you want an empty tag with no whitespace. Use the double pipe (||)

    script type="text/javascript" ||
    
#### Output
    
    <script type="text/javascript"></script>
    
### Disabling Shpaml within a block (inline javascript or css)

Sometimes you want to disable shpaml so you can inline some js or css in a 
page. You can use the VERBATIM tag to tell shpaml not to process the contents
of a tag.

VERBATIM must be all caps, and it must be the last thing in the line

    script VERBATIM type="text/javascript"
        // this is no good...
        $("div")
            .hide()
            .fadeIn(function() {
                // uh oh
            });
            

    script type="text/javascript" VERBATIM
        // this is the way to do it :)
        $("div")
            .hide()
            .fadeIn(function() {
                // uh oh
            });
            
#### Output

    <script VERBATIM type="text/javascript">
        // this is no good...
        $("div")
            .hide()
            <div class="fadeIn(function() {">
                // uh oh
            </div>
            });
    </script>
            

    <script type="text/javascript">
        // this is the way to do it :)
        $("div")
            .hide()
            .fadeIn(function() {
                // uh oh
            });
    </script>
    
### Django Template Tags

Lines starting with a percent sign (%) will be converted to django template 
tags.

if the template tag as contents an "end" tag will be added, otherwise it will 
be treated as having no end tag (double pipe syntax and PASS are supported as 
well)

you can also user the pipe percent (|%) operator for non-closing template tags
similarly to the pipe operator...

    %block content
        this will get an "endblock" tag because it has contents
        
        form action="."
            the csrf token tag doesn't get a closing tag because it 
            has no contents...
            %csrf_token
            
            {{ form.as_p }}
            
            button type="reset" | Cancel
            button type="submit" | Save
            
     This is an empty block:
     footer
        &copy; Me
        span.current-time |% now "Y"
        
        %block more_footer ||
            
#### Output
    
    {% block content %}
        this will get an "endblock" tag because it has contents
        
        <form action=".">
            the csrf token tag doesn't get a closing tag because it 
            has no contents...
            {% csrf_token %}
            
            {{ form.as_p }}
            
            <button type="reset">Cancel</button>
            <button type="submit">Save</button>
        </form>
    {% endblock %}
    
    This is an empty block:
    <footer>
        &copy; Me
        <span class="current-year">{% now "Y" %}</span>
        
        {% block more_footer %}{% endblock %}
    </footer>
    
### Django Variable Insertion

You can insert django variables using the equals sign (=). You can
also use the pipe equals operator similarly to the pipe operator.
    
    .profile-info
        a href="{{ user.get_absolute_url }}" |= user.get_full_name
        p.user-name
            strong | username:
            = user.username
    
#### Output

    <div class="profile-info">
        <a href="{{ user.get_absolute_url }}">{{ user.get_full_name }}</a>
        <p class="user-name">
            <strong>username:</strong>
            {{ user.username }}
        </p>
    </div>
        
### Other shortcuts 

You can leave quotes off attribute values when the name and value are single 
words.

You can also have multiple inline tags on the same line.

    > input type=text name=department value="Computer Science"
    
    .greeting > strong > p | Hello

#### Output

    <input type="text" name="department" value="Computer Science" />

    <div class="greeting"><strong><p>Hello</p></strong></div>
    