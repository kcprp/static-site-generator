import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from split_nodes import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a not text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_url_is_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def different_properties(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertNotEqual(node, node2)
        
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestTextNodeSplitNodes(unittest.TestCase):
    def test_code_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )
        
    def test_bold_node(self):
        node = TextNode("This is a text with a *bolded* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ] 
        )
        
    def test_multiple_code_blocks(self):
        node = TextNode("This is a text with `first` and `second` code block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with ", TextType.TEXT),
                TextNode("first", TextType.CODE),
                TextNode(" and ", TextType.TEXT), 
                TextNode("second", TextType.CODE),
                TextNode(" code block", TextType.TEXT), 
            ]
        )
        
        
    def test_missing_delimeter(self):
        node = TextNode("This is a text node", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid Markdown syntax: * not in any text node")
        
        
        

if __name__ == "__main__":
    unittest.main()