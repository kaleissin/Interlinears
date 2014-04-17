# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import unittest

import interlinears
from interlinears.leipzig import (
    get_blocks,
    InterlinearText,
    InterlinearError,
    InterlinearErrorMsg)

class MonospaceTest(unittest.TestCase):

    def test_empty(self):
        raw = ''
        result = interlinears.make_html_interlinear(raw, format='monospace')
        self.assertEqual(raw, result)

    def test_simple(self):
        raw = 'a b c'
        result = interlinears.make_html_interlinear(raw, format='monospace')
        self.assertEqual("<pre>%s</pre>" % raw, result)

    def test_unsanitized(self):
        raw = 'a<b'
        with self.assertRaises(ValueError) as error:
            result = interlinears.make_html_interlinear(raw, format='monospace')
            self.assertEqual(error.exception, 'Input has not been sanitized')

class TestGetBlock(unittest.TestCase):

    def test_get_block(self):
        "get_blocks() should handle *any* line-separator-convention"

        unixtext = """a\nb\n\nc\nd"""
        dostext = """a\r\nb\r\n\r\nc\r\nd"""
        mactext = """a\rb\r\rc\rd"""

        blocklen = 2
        self.assertEqual(len(get_blocks(unixtext)), blocklen, 'Failed to normalize UNIX')
        self.assertEqual(len(get_blocks(dostext)), blocklen, 'Failed to normalize DOS')
        self.assertEqual(len(get_blocks(mactext)), blocklen, 'Failed to normalize Mac')

class TestInterlinearBlock(unittest.TestCase):

    def setUp(self):
        self.il = InterlinearText.InterlinearBlock()

    def test_set_final(self):
        text = 'foo'
        self.il.set_final(text)
        self.assertEqual(text, self.il.final)

    def test_reformat(self):
        result = [(1,1), (2,2), (3,3)]
        self.il.lines = ((1,2,3), (1,2,3))
        self.assertEqual(result, list(self.il.reformat()))

    def test_to_html(self):
        self.il.lines = ((1,2,3), (1,2,3))

        result = """<div class="interlinear">
<div class="word">
<div class="line">1</div>
<div class="line">1</div>
</div>

<div class="word">
<div class="line">2</div>
<div class="line">2</div>
</div>

<div class="word">
<div class="line">3</div>
<div class="line">3</div>
</div>
</div>
"""
        self.assertEqual(self.il.to_html(), result)

    def test_add_block(self):
        text = 'a b c\n1 2 3'.split('\n')
        self.il.add_line(text[0])
        self.il.add_line(text[1])
        self.assertEqual(len(text), len(self.il.lines))

class TestInterlinearText(unittest.TestCase):

    def setUp(self):
        self.il = InterlinearText()

    def test_set_final(self):
        text = """asd ghg-jhjlk-jkljl
A B-C-D
"dfdd jgjj hjkhjk jkhjkhjkh"
""".strip().split('\n')
        ilb = self.il.InterlinearBlock()
        ilb, lines = self.il._check_final(ilb, text)
        self.assertEqual(ilb.final, '"dfdd jgjj hjkhjk jkhjkhjkh"')
        self.assertEqual(len(text)-1, len(lines))

    def test_set_no_final(self):
        text = '''asd ghg-jhjlk-jkljl
A B-C-D'''.strip().split('\n')
        ilb = self.il.InterlinearBlock()
        ilb, lines = self.il._check_final(ilb, text)
        self.assertEqual(ilb.final, '')
        self.assertEqual(len(text), len(lines))

    def test_empty(self):
        text = ''
        with self.assertRaises(InterlinearError) as error:
            self.il.do_text(text)
            self.assertEqual(error.exception, InterlinearErrorMsg.empty_block)

    def test_single_line(self):
        text = "'g jhgjhgjh'"
        expected = "<p>'g jhgjhgjh'</p>\n"
        result = self.il.do_text(text)
        self.assertEqual(expected, result)

    def test_single_simple_block(self):
        text = """asd ghg-jhjlk-jkljl sdsds rtyy-ry
A B-C-D E F-G
"""

        expected = """<div class="interlinear">
<div class="word">
<div class="line">asd</div>
<div class="line">A</div>
</div>

<div class="word">
<div class="line">ghg-jhjlk-jkljl</div>
<div class="line">B-C-D</div>
</div>

<div class="word">
<div class="line">sdsds</div>
<div class="line">E</div>
</div>

<div class="word">
<div class="line">rtyy-ry</div>
<div class="line">F-G</div>
</div>
</div>
"""

        result = self.il.do_text(text)
        self.assertEqual(expected, result)

    def test_single_wrong_token_block(self):
        text = """a b c\n1 2"""
        with self.assertRaises(InterlinearError) as e:
            result = self.il.do_text(text)
            self.assertEqual(e.exception, InterlinearErrorMsg.wrong_number_of_tokens)

        text = """a b c\n1 2 3 4"""
        with self.assertRaises(InterlinearError) as e:
            result = self.il.do_text(text)
            self.assertEqual(e.exception, InterlinearErrorMsg.wrong_number_of_tokens)

    def test_trailing_line(self):
        text = """asd ghg-jhjlk-jkljl
A B-C-D

"dfdd jgjj hjkhjk jkhjkhjkh"
"""

        expected = """<div class="interlinear">
<div class="word">
<div class="line">asd</div>
<div class="line">A</div>
</div>

<div class="word">
<div class="line">ghg-jhjlk-jkljl</div>
<div class="line">B-C-D</div>
</div>
</div>

<p>"dfdd jgjj hjkhjk jkhjkhjkh"</p>
"""
        result = self.il.do_text(text)
        self.assertEqual(expected, result)

    def test_single_complex_block(self):
        text = """asd ghg-jhjlk-jkljl
A B-C-D
"dfdd jgjj hjkhjk jkhjkhjkh"
"""

        expected = """<div class="interlinear">
<div class="word">
<div class="line">asd</div>
<div class="line">A</div>
</div>

<div class="word">
<div class="line">ghg-jhjlk-jkljl</div>
<div class="line">B-C-D</div>
</div>

<p>"dfdd jgjj hjkhjk jkhjkhjkh"</p>
</div>
"""
        result = self.il.do_text(text)
        self.assertEqual(expected, result)

    def test_double_complex_block(self):
        text = """asd ghg-jhjlk-jkljl sdsds rtyy-ry
A B-C-D E F-G
"dfdd jgjj hjkhjk jkhjkhjkh"

1 2-3-4 5 6-7
A B-C-D E F-G
"blbl ghghgh fifi yaa"
"""
        expected = """<div class="interlinear">
<div class="word">
<div class="line">asd</div>
<div class="line">A</div>
</div>

<div class="word">
<div class="line">ghg-jhjlk-jkljl</div>
<div class="line">B-C-D</div>
</div>

<div class="word">
<div class="line">sdsds</div>
<div class="line">E</div>
</div>

<div class="word">
<div class="line">rtyy-ry</div>
<div class="line">F-G</div>
</div>

<p>"dfdd jgjj hjkhjk jkhjkhjkh"</p>
</div>

<div class="interlinear">
<div class="word">
<div class="line">1</div>
<div class="line">A</div>
</div>

<div class="word">
<div class="line">2-3-4</div>
<div class="line">B-C-D</div>
</div>

<div class="word">
<div class="line">5</div>
<div class="line">E</div>
</div>

<div class="word">
<div class="line">6-7</div>
<div class="line">F-G</div>
</div>

<p>"blbl ghghgh fifi yaa"</p>
</div>
"""
        result = self.il.do_text(text)
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
