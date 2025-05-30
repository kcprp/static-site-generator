import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
        
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_with_many_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_with_many_parent(self):
        child_node = LeafNode("b", "first child")
        parent_node = ParentNode("span", [child_node])
        child_node2 = LeafNode("p", "second child")
        parent_node2 = ParentNode("div", [child_node2])
        single_node = LeafNode("p", "hello")
        
        uber_parent = ParentNode(
            "div",
            [
                parent_node,
                parent_node2,
                single_node
            ]
        )
        
        self.assertEqual(
            uber_parent.to_html(),
            "<div><span><b>first child</b></span><div><p>second child</p></div><p>hello</p></div>"
        )

if __name__ == "__main__":
    unittest.main()