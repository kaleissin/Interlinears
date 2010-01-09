# -*- coding: UTF-8 -*-

def _escape(unistr):
    return unistr.replace(u'&', u'&amp;').replace(u'<', u'&lt;').replace(u'>', u'&gt;').replace(u'"', u'&quot;').replace(u"'", u'&#39;')

def make_html_interlinear(raw_interlinear, format=u'monospace', escape=_escape):
    """Returns htmlified, web-safe version of interlinear
    
    ``format``
        Default: monospace, which wraps the string in <pre>-tags.

    ``escape``
        function that escapes HTML-syntax, that is: <, >, ", ', &
    """

    if not raw_interlinear.strip():
        return u''
    interlinear = raw_interlinear
    # TODO: SIL shoebox/toolbox-format interlnears
    if format == u'leipzig':
        il = InterlinearText()
        return il.do_text(interlinear)
    return u'<pre>%s</pre>' % escape(interlinear)
