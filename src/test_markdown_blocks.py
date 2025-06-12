import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace(self):
        md = """
        

This is a paragraph

        

Another paragraph

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "Another paragraph",
            ],
        )

    def test_markdown_to_blocks_single_line(self):
        md = "This is a single line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line"])

    def test_block_to_block_type(self):
        # Test headings
        self.assertEqual(
            block_to_block_type("# Heading 1"),
            BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("###### Heading 6"),
            BlockType.HEADING
        )

        # Test code blocks
        self.assertEqual(
            block_to_block_type("```\ncode block\n```"),
            BlockType.CODE
        )

        # Test quote blocks
        self.assertEqual(
            block_to_block_type("> First line\n> Second line"),
            BlockType.QUOTE
        )

        # Test unordered lists
        self.assertEqual(
            block_to_block_type("- First item\n- Second item"),
            BlockType.ULIST
        )

        # Test ordered lists
        self.assertEqual(
            block_to_block_type("1. First item\n2. Second item"),
            BlockType.OLIST
        )
        self.assertEqual(
            block_to_block_type("1. First item\n2. Second item\n3. Third item"),
            BlockType.OLIST
        )

        # Test invalid ordered list
        self.assertEqual(
            block_to_block_type("1. First item\n3. Second item"),
            BlockType.PARAGRAPH
        )

        # Test paragraphs
        self.assertEqual(
            block_to_block_type("This is a paragraph"),
            BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("This is a paragraph\nwith multiple lines"),
            BlockType.PARAGRAPH
        )
        
if __name__ == "__main__":
    unittest.main()