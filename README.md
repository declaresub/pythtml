# pyfive

pyfive is an alternative to templates for generation of HTML 5. 


## Python Requirements

pyfive does not support Python 2.  It has been tested with Python 3.4-3.6.

## Using pyfive

To use pyfive, import all from the package.

    from pyfive import *

This adds functions corresponding to HTML 5 elements to the module namespace, plus a special class, 
`Raw`.

The signature for most HTML element classes is the same.

    class P(_Element):
        def __init__(self, *children, **attributes)
    
A children argument can be either another pyfive element, or text. Text 
values are escaped using cgi.escape. Attribute parameters are demangled as follows:
keyword_ -> keyword
data\_foo_bar -> data-foo-bar

Underscores in names not beginning with data_ are left as is.

Some classes have a different \_\_init__ method.

    class Html(_Element):
        def __init__(self, head, body, *, encoding='utf-8', **attributes):
        
You must supply head and body elements.  An element `<meta charset="encoding">` will be 
inserted as the first element of the head element.

    class Raw(_Element):
        def __init__(self, data):

This pseudo element passes data through unescaped.  You might
want to use this to include a script, or other raw HTML.  There are examples below.

Empty elements (e.g. img) omit the *children parameter in \_\_init__.

    
## Text Encoding

The default encoding for HTML 5 is UTF-8.  The magic method `Html.__bytes__` returns UTF-8 encoded
data. If you want data with a different encoding, use `str(doc).encode('your-encoding')`.
A meta element specifying the charset is inserted for you as the first child element of
the head element.

## Development

Use the venv script included in the repository to create virtual environments.

### Create a virtual environment

    ./venv create dev
    
Specify a python version:

    ./venv create --pyversion 3.4 dev3.4
    
The command creates a new virtual environment and installs everything in requirements.txt.
Virtual environments are created in /path/to/repository/.venv .

Remove a virtual environment:

    ./venv remove dev3.4
    
Activate a virtual environment:

    ./venv shell dev3.6
    
You can omit the name if there is only one virtual environment.  This command creates a new
bash shell.  Other shells could be supported if anyone else ever works on pyfive.

## Examples

### Get the package version:

    >>> import pyfive
    >>> print(pyfive.__version__)
    0.0.0
    
### Generation of a document:

    >>> from pyfive import *
    >>> 
    >>> doc = Html(
    ...     Head(Title('pyfive')),
    ...     Body(
    ...         H1('pyfive', id="title"), 
    ...         P('pyfive is an alternative to templates for generation of HTML.', class_='blurb'), 
    ...         Script(type='text/javascript', src='http://www.the.gov/tracking_code.js')
    ...         )
    ...     )
    >>> 


### Generation of a meta
### Generation of a header element:

    >>> doc_header = header(
    ...     H1('pyfive', id="title"), 
    ...     P('pyfive is an alternative to templates for generation of HTML.')
    ...     )
    >>> print(doc_header)
    <header><h1 id="title">pyfive</h1><p>pyfive is an alternative to templates for generation of HTML.</p></header>
    
### Inline Formatting

    >>> from pyfive import *
    >>> 
    >>> print (P('This text contains a ', B('bold'), ' tag.'))
    <p>This text contains a <b>bold</b> tag.</p>
    
### Add script code without escaping:

    >>> from pyfive import *
    >>> 
    >>> chumhum_analytics = """
    ...     (function(i,s,o,g,r,a,m){i['ChumhumAnalyticsObject']=r;i[r]=i[r]||function(){
    ...     (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    ...     m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    ...     })(window,document,'script','//analytics.chumhum.com/analytics.js','ca');
    ...     ca('create', 'ID-0000000-3', 'auto');
    ...     ca('send', 'pageview');
    ...     """.strip()
    >>> 
    >>> doc = Body(
    ...     Script(Raw(chumhum_analytics), type="text/javascript")
    ...     )
    >>> print(doc)
    <body><script type="text/javascript">(function(i,s,o,g,r,a,m){i['ChumhumAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','//analytics.chumhum.com/analytics.js','ca');
        ca('create', 'ID-0000000-3', 'auto');
        ca('send', 'pageview');</script></body>

### Iteration

    >>> from pyfive import *
    >>> 
    >>> option_items = ['Red', 'Green', 'Blue']
    >>> print(Ul(*(Li(item) for item in option_items)))
    <ul><li>Red</li><li>Green</li><li>Blue</li></ul>

### Template

    >>> from pyfive import *

    >>> context = {'username': 'poindexter'}
    >>> template = str(P('You are logged in as {username}.', class_='welcome'))
    >>> print(template.format(**context))
    <p class="welcome">You are logged in as poindexter.</p>


