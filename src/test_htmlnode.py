import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_string_eq(self):
        node = HTMLNode("this is supposed to be a tag","this is supposed to be a value",["this is a child","this is also a child"],{"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.props_to_html()," href=\"https://www.google.com\" target=\"_blank\"")


    def test_node_does_print(self):
        node = HTMLNode("this is supposed to be a tag","this is supposed to be a value",["this is a child","this is also a child"],{"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.__repr__(),f"HTMLNode({node.tag},{node.value},{node.children},{node.props})")



class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img","this is some value text",{"src": "url/of/image.jpg","alt": "Description of Image"})
        self.assertEqual(node.to_html(),"<img src=\"url/of/image.jpg\" alt=\"Description of Image\" />")

    
if __name__ == "__main__":
    unittest.main()