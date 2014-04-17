# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import re

UNWANTED_RE = '''[<>"']'''

def make_html_interlinear(raw_interlinear, format='monospace'):
    """Returns htmlified, web-safe version of interlinear
    
    ``format``
        Default: monospace, which wraps the string in <pre>-tags.
    """

    if not raw_interlinear.strip():
        return ''
    if re.search(UNWANTED_RE, raw_interlinear):
        raise ValueError('Input has not been sanitized')
    interlinear = raw_interlinear
    # TODO: SIL shoebox/toolbox-format interlnears
    if format == 'leipzig':
        il = InterlinearText()
        return il.do_text(interlinear)
    return '<pre>%s</pre>' % interlinear
