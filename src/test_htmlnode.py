import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
            })
        expected = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_eq(self):
        node = HTMLNode(tag="<p>", value="hello")
        node2 = HTMLNode(tag="<p>", value="hello")

        self.assertEqual(node.__repr__(), node2.__repr__())

    def test_eq_false(self):
        node = HTMLNode(tag="<p>", value="hello")
        node2 = HTMLNode(tag="<p>", value="hello", props={"href": "https://www.google.com"})

        self.assertNotEqual(node.__repr__(), node2.__repr__())


if __name__ == "__main__":
    unittest.main()