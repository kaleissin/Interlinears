# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import string
from pprint import pprint, pformat

__all__ = ['InterlinearError', 'InterlinearText', 'InterlinearErrorMsg']

class InterlinearErrorMsg(object):
    empty_block = 'Empty block'
    wrong_number_of_tokens = 'Not the same number of tokens on each line'

class InterlinearError(Exception):
    pass

def get_blocks(text):
    """Normalize lineends and split on double newline"""

    lines = text.strip().splitlines()
    text = '\n'.join(lines)
    return text.split('\n\n')

def get_nonempty_tokens(text):
    return [_f for _f in text if _f]

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
                    raise InterlinearError(InterlinearErrorMsg.wrong_number_of_tokens)

        def add_line(self, block):
            tokens = get_nonempty_tokens(block.split())
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

    def __init__(self):
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
        return '\n'.join(block_list)

    def do_block(self, block):
        """Accepts a single paragraph of interlinearized plaintext and converts it to HTML."""

        il = self.InterlinearBlock()

        lines = block.split('\n')
        if not get_nonempty_tokens(lines):
            raise InterlinearError(InterlinearErrorMsg.empty_block)

        il, lines = self._check_final(il, lines)

        if len(lines) > 1:
            for line in lines:
                il.add_line(line)
            return il.to_html()
        return '<p>%s</p>\n' % block

