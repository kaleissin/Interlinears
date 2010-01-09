# -*- coding: UTF-8 -*-

import string
from pprint import pprint, pformat

class InterlinearErrorMsg(object):
    empty_block = 'Empty block'
    wrong_number_of_tokens = 'Not the same number of tokens on each line'

class InterlinearError(Exception):
    pass

def get_blocks(text):
    """Normalize lineends and split on double newline"""

    lines = text.strip().splitlines()
    text = u'\n'.join(lines)
    return text.split(u'\n\n')

class InterlinearText(object):

    class InterlinearBlock(object):
        wrapfmt = '<div class="interlinear">\n%s</div>\n'
        wordfmt = '<div class="word">\n%s\n</div>\n'
        linefmt = '<div class="line">%s</div>'
        ft_fmt = '<p>%s</p>\n'

        def __init__(self):
            self.num_tokens = 0
            self.lines = []
            self.final = ''

        def _check_length(self, tokens):
            if not self.num_tokens:
                self.num_tokens = len(tokens)
            else:
                if len(tokens) != self.num_tokens:
                    raise InterlinearError, InterlinearErrorMsg.wrong_number_of_tokens
                    #raise InterlinearError, '%s: %s != %i' % (InterlinearErrorMsg.wrong_number_of_tokens, tokens, self.num_tokens)

        def add_line(self, block):
            tokens = filter(None, block.split())
            self._check_length(tokens)
            self.lines.append(tokens)

        def reformat(self):
            return zip(*self.lines)

        def set_final(self, line):
            self.final = line

        def to_html(self):
            word_list = []
            for block in self.reformat():
                line_list = []
                for word in block:
                    line_list.append(self.linefmt % word)
                word_list.append(self.wordfmt % '\n'.join(line_list))
            if self.final:
                word_list.append(self.ft_fmt % self.final)
            return self.wrapfmt % '\n'.join(word_list)

    def __init__(self, text=None):
        if text:
            self.text = text
        else:
            self.text = ''
        self.text_blocks = []

    def _check_final(self, il, lines):
        quotes = (u'"', u"'", u'`', u'«', u'»')
        special_final = u''
        if lines[-1][0] in quotes:
            special_final = lines[-1]
            lines = lines[:-1]
            il.set_final(special_final)
        return il, lines

    def do_text(self, text):
        """Accepts one or more paragraphs of interlinearized plaintext and
        converts them all to HTML."""

        self.text = text
        blocks = get_blocks(text)
        self.text_blocks = blocks
        block_list = []
        for block in blocks:
            block_list.append(self.do_block(block))
        return u'\n'.join(block_list)

    def do_block(self, block):
        """Accepts a single paragraph of interlinearized plaintext and converts it to HTML."""

        il = self.InterlinearBlock()

        lines = block.split('\n')
        if not filter(None, lines):
            raise InterlinearError, InterlinearErrorMsg.empty_block
        
        il, lines = self._check_final(il, lines)

        if len(lines) > 1:
            for line in lines:
                il.add_line(line)
            return il.to_html()
        return '<p>%s</p>\n' % block

# ---- Tests
import unittest

class TestInterlinearBlock(unittest.TestCase):

    def setUp(self):
        self.il = InterlinearText.InterlinearBlock()

    def testSetFinal(self):
        text = 'foo'
        self.il.set_final(text)
        self.assertEqual(text, self.il.final)

    def testReformat(self):
        result = [(1,1), (2,2), (3,3)]
        self.il.lines = ((1,2,3), (1,2,3))
        self.assertEqual(result, self.il.reformat())

    def testGetBlock(self):
        "get_blocks() should handle *any* line-separator-convention"

        unixtext = """a\nb\n\nc\nd"""
        dostext = """a\r\nb\r\n\r\nc\r\nd"""
        mactext = """a\rb\r\rc\rd"""
        #mixedtext = """a\nb\r\nc\rd"""

        blocklen = 2
        self.assertEqual(len(get_blocks(unixtext)), blocklen, 'Failed to normalize UNIX')
        self.assertEqual(len(get_blocks(dostext)), blocklen, 'Failed to normalize DOS')
        self.assertEqual(len(get_blocks(mactext)), blocklen, 'Failed to normalize Mac')
        #self.assertEqual(len(get_blocks(mixedtext)), blocklen, 'Failed to normalize mixed')

    def testToHtml(self):
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

    def testAddBlock(self):
        text = 'a b c\n1 2 3'.split('\n')
        self.il.add_line(text[0])
        self.il.add_line(text[1])
        self.assertEqual(len(text), len(self.il.lines))

class TestInterlinearText(unittest.TestCase):

    def _get_actual_result(self, text):
        il = InterlinearText()
        self.actual_result = il.do_text(text)

    def body(self, text, expected_result):
        self._get_actual_result(text)
        self.assertEqual(expected_result, self.actual_result)

    def testSetFinal1(self):
        text = """asd ghg-jhjlk-jkljl
A B-C-D
"dfdd jgjj hjkhjk jkhjkhjkh"
""".strip().split('\n')
        ilt = InterlinearText()
        ilb = InterlinearText.InterlinearBlock()
        ilb, lines = ilt._check_final(ilb, text)
        self.assertEqual(ilb.final, '"dfdd jgjj hjkhjk jkhjkhjkh"')
        self.assertEqual(len(text)-1, len(lines))

    def testSetFinal2(self):
        text = '''asd ghg-jhjlk-jkljl
A B-C-D
"dfdd jgjj hjkhjk jkhjkhjkh"'''.strip().split('\n')
        ilt = InterlinearText()
        ilb = InterlinearText.InterlinearBlock()
        ilb, lines = ilt._check_final(ilb, text)
        self.assertEqual(ilb.final, '"dfdd jgjj hjkhjk jkhjkhjkh"')
        self.assertEqual(len(text)-1, len(lines))

    def testEmpty(self):
        text = ''
        try:
            self._get_actual_result(text)
        except InterlinearError, e:
            self.assertEqual(e.args[0], InterlinearErrorMsg.empty_block)

    def testSingleLine(self):
        text = "'g jhgjhgjh'"
        result = "<p>'g jhgjhgjh'</p>\n"
        self.body(text, result)

    def testSingleSimpleBlock(self):
        text = """asd ghg-jhjlk-jkljl sdsds rtyy-ry
A B-C-D E F-G
"""

        result = """<div class="interlinear">
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

        self.body(text, result)

    def testSingleWrongTokenBlock(self):
        text = """a b c\n1 2"""
        try:
            self._get_actual_result(text)
        except InterlinearError, e:
            self.assertEqual(e.args[0], InterlinearErrorMsg.wrong_number_of_tokens)
        else:
            self.fail('Failed to stop on wrong number of tokens')
    
    def testTrailingLine(self):
        text = """asd ghg-jhjlk-jkljl
A B-C-D

"dfdd jgjj hjkhjk jkhjkhjkh"
"""

        result = """<div class="interlinear">
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
        self._get_actual_result(text)
        self.body(text, result)

    def testSingleComplexBlock(self):
        text = """asd ghg-jhjlk-jkljl
A B-C-D
"dfdd jgjj hjkhjk jkhjkhjkh"
"""

        result = """<div class="interlinear">
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
        self._get_actual_result(text)
        self.body(text, result)

    def testDoubleComplexBlock(self):
        text = """asd ghg-jhjlk-jkljl sdsds rtyy-ry
A B-C-D E F-G
"dfdd jgjj hjkhjk jkhjkhjkh"

1 2-3-4 5 6-7
A B-C-D E F-G
"blbl ghghgh fifi yaa"
"""
        result = """<div class="interlinear">
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
        self._get_actual_result(text)
        self.body(text, result)

    def testAdHocBlock(self):
        """For developing integration tests

        First print the actual_result and decide if that is correct:

        print self.actual_result

        If correct, copy what is in self.actual_result to result, below,
        then uncomment the self.body-line
        """
        text = """a
b

c
d
"""
        #result =
        self._get_actual_result(text)
        #self.body(text, result)

if __name__ == '__main__':
    unittest.main()
