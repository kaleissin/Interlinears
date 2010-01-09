============
Interlinears
============

This package pretty-prints plaintext `linguistic interlinears`__,
currently only to HTML.

__ http://en.wikipedia.org/wiki/Interlinear_gloss

It supports two formats:
    - ``monospace``, where What You See Is What You Get, though where HTML
      can be escaped or stripped away.
    - ``leipzig``, as by the `Leipzig Glossing Rules`__.

__ http://www.eva.mpg.de/lingua/resources/glossing-rules.php

Usage
-----

interlinears.make_html_interlinear(raw_interlinear, format='monospace', escape=``some_func``)
