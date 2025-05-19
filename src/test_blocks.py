import unittest

from blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocklist = markdown_to_blocks(md)
        self.assertListEqual(
            blocklist,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_block(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here

- This is a list
- with items
"""
        blocklist = markdown_to_blocks(md)
        self.assertListEqual(
            blocklist,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_boundary(self):
        block = "####### This is a bad heading"
        block2 = "###### This is a good heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block2), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```This is a code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_improper(self):
        block = "```This is a bad code block``"
        block2 = "``This one too```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block2), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        md = """
>This is a quote
>type block
        """
        self.assertEqual(
            block_to_block_type(markdown_to_blocks(md)[0]), BlockType.QUOTE
        )

    def test_block_to_block_type_quote_improper(self):
        md = """
>This is a quote
gone bad
        """
        self.assertEqual(
            block_to_block_type(markdown_to_blocks(md)[0]), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_ulist(self):
        md = """
- This is an
- unordered list
        """
        self.assertEqual(
            block_to_block_type(markdown_to_blocks(md)[0]), BlockType.ULIST
        )

    def test_block_to_block_type_ulist_improper(self):
        md = """
- This is a bad
unordered list
        """
        self.assertEqual(
            block_to_block_type(markdown_to_blocks(md)[0]), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_olist(self):
        md = """
1. This is a
2. ordered
3. list
        """
        self.assertEqual(
            block_to_block_type(markdown_to_blocks(md)[0]), BlockType.OLIST
        )

    def test_block_to_block_type_olist_improper_no_number(self):
        md = """
1. This is a
2. bad
list
        """
        self.assertEqual(
            block_to_block_type(markdown_to_blocks(md)[0]), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_ulist_improper_bad_number_order(self):
        md = """
1. This is a
3. bad
2. list
        """
        self.assertEqual(
            block_to_block_type(markdown_to_blocks(md)[0]), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_olist_improper_bad_number_start(self):
        md = """
2. This is a
3. bad
4. list
        """
        self.assertEqual(
            block_to_block_type(markdown_to_blocks(md)[0]), BlockType.PARAGRAPH
        )
