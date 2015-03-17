# pyfive

pyfive is an alternative to templates for generation of HTML 5. 


## Using pyfive

To use pyfive, import all from the package.

    from pyfive import *

This adds functions corresponding to HTML 5 elements to the module namespace, plus a special function, 
`raw`.

The signature for all HTML element functions is the same.

    def html(*children, **attributes)
    
A children argument can be either the value returned by another pyfive, or text. Text 
values are escaped using cgi.escape.

The function `raw` is the exception.

    def raw(data):
    
This pseudo element passes data through unescaped.  You might want to use this to include 
a script, or other raw HTML.

Values returned by the pyfive functions are intended to be immmutable, so you can 
create, say, a header and use it in lots of documents.

    
## Text Encoding

pyfive uses Unicode internally, and prefers that you pass it Unicode data.  String 
objects are assumed to be UTF-8 encoded and converted; conversion errors are not ignored.

The default encoding for HTML 5 is UTF-8.  The object methods `__str__` (Python 2) and `__bytes__` 
(Python 3) both return UTF-8 encoded data.  If you want data with a different encoding, 
use `unicode(doc).encode('your-encoding')`.  In any case, you should add a meta element 
specifying the charset as the first child of the head element.


## Examples

### Get the package version:

    >>> import pyfive
    >>> print(pyfive.__version__)
    0.0.0
    
### Generation of a document:

    >>> from pyfive import *
    >>> 
    >>> doc = html(
    ...     body(
    ...         h1('pyfive', id="title"), 
    ...         p('pyfive is an alternative to templates for generation of HTML.', Class='blurb'), 
    ...         script(type='text/javascript', src='http://www.the.gov/tracking_code.js')
    ...         )
    ...     )
    >>> 


### Generation of a header element:

    >>> doc_header = header(
    ...     h1('pyfive', id="title"), 
    ...     p('pyfive is an alternative to templates for generation of HTML.')
    ...     )
    >>> print(doc_header)
    <header><h1 id="title">pyfive</h1><p>pyfive is an alternative to templates for generation of HTML.</p></header>
    
### Inline Formatting

    >>> from pyfive import *
    >>> 
    >>> print (p('This text contains a ', b('bold'), ' tag.'))
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
    >>> doc = body(
    ...     script(raw(chumhum_analytics), type="text/javascript")
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
    >>> print(ul(*(li(item) for item in option_items)))
    <ul><li>Red</li><li>Green</li><li>Blue</li></ul>

### Template

    >>> from pyfive import *

    >>> context = {'username': 'poindexter'}
    >>> template = str(p('You are logged in as {username}.', Class='welcome'))
    >>> print(template.format(**context))
    <p class="welcome">You are logged in as poindexter.</p>
    