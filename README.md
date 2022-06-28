#pythtml

pythtml is an alternative to templates for generation of HTML 5. 

![tox](https://github.com/ccwrangler/ccwrangler-api/actions/workflows/tox.yml/badge.svg)

## Python Requirements

pythtml does not support Python 2.  It is tested with Python 3.7+

## Using pythtml

To use pythtml, import all from the package.

    from pythtml import *

This adds functions corresponding to HTML 5 elements to the module namespace, plus a special class, 
`Raw`.

The signature for most HTML element classes is the same.

    class P(_Element):
        def __init__(self, *children, **attributes)
    
A children argument is another pythtml element. 

Attribute parameters are demangled as follows:
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

## Raw HTMl

The Raw pseudo-element allows for the insertion of string data into an HTML document.  Typically one would
use this to add script elements.  The Raw initializer has a keyword parameter escape_data with default value False.  Pass True
to escape some reserved HTML characters in data.

## Text Encoding

The default encoding for HTML 5 is UTF-8, but you can supply a different encoding in HTML.__init__. The dunder method `Html.__bytes__` returns data
encoded in the specified encoding.

A meta element specifying the charset is inserted for you as the first child element of
the head element.


## Examples

### Get the package version:

    >>> import pythtml
    >>> print(pythtml.__version__)
    0.0.0
    
### Generation of a document:

    >>> from pythtml import *
    >>> 
    >>> doc = Html(
    ...     Head(Title('pythtml')),
    ...     Body(
    ...         H1('pythtml', id="title"), 
    ...         P('pythtml is an alternative to templates for generation of HTML.', class_='blurb'), 
    ...         Script(type='text/javascript', src='http://www.the.gov/tracking_code.js')
    ...         )
    ...     )
    >>> 


### Generation of a meta
### Generation of a header element:

    >>> doc_header = header(
    ...     H1('pythtml', id="title"), 
    ...     P('pythtml is an alternative to templates for generation of HTML.')
    ...     )
    >>> print(doc_header)
    <header><h1 id="title">pythtml</h1><p>pythtml is an alternative to templates for generation of HTML.</p></header>
    
### Inline Formatting

    >>> from pythtml import *
    >>> 
    >>> print (P('This text contains a ', B('bold'), ' tag.'))
    <p>This text contains a <b>bold</b> tag.</p>
    
### Add script code without escaping:

    >>> from pythtml import *
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

    >>> from pythtml import *
    >>> 
    >>> option_items = ['Red', 'Green', 'Blue']
    >>> print(Ul(*(Li(item) for item in option_items)))
    <ul><li>Red</li><li>Green</li><li>Blue</li></ul>

### Template

    >>> from pythtml import *

    >>> context = {'username': 'poindexter'}
    >>> template = str(P('You are logged in as {username}.', class_='welcome'))
    >>> print(template.format(**context))
    <p class="welcome">You are logged in as poindexter.</p>


## Development

### Unit Tests

From the root of the repository, run unit tests:

    pytest --cov=src --cov-report term-missing tests

Run tox to test all supported Python versions:

    tox
