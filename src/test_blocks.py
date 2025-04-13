from funcs import *
from blocks import Blocktype,block_to_block
import unittest


class TestBlockToBlock (unittest.TestCase):

    def test_headings(self):
        block = "#### This is a heading, or atleast i hope it is"

        self.assertEqual(block_to_block(block), Blocktype.HEADING)

    def test_code(self):
        block = "```\nThis is a code block, or atleast i hope it is\n```"

        self.assertEqual(block_to_block(block), Blocktype.CODE)
    
    def test_quote_oneline(self):
        block = ">This is a quote, or atleast i hope it is"

        self.assertEqual(block_to_block(block), Blocktype.QUOTE)

    def test_quote_multiline(self):
        block = """> This is a quote
> That spans
> Many lines
> I sure hope it works"""
        self.assertEqual(block_to_block(block),Blocktype.QUOTE)

    def test_u_list(self):
        block = "- This is a list\n- or atleast i hope it is\n- im fairly sure it works"

        self.assertEqual(block_to_block(block), Blocktype.UNORDERED_LIST)

    def test_o_list(self):
        block = "1. This is a list\n2. or atleast i hope it is\n3. im fairly sure it works"

        self.assertEqual(block_to_block(block), Blocktype.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is just a simple paragraph, should def work i hope"

        self.assertEqual(block_to_block(block),Blocktype.PARAGRAPH)