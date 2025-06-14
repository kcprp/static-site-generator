import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
    extract_title
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


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        md = """
# This is a title

This is a paragraph
"""
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_extract_title_missing(self):
        md = """
This is a paragraph

## This is a heading but not a title
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_multiple_h1(self):
        md = """
# First title

# Second title
"""
        title = extract_title(md)
        self.assertEqual(title, "First title")


if __name__ == "__main__":
    unittest.main()