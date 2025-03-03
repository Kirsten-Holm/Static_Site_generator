import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_string_eq(self):
        node = HTMLNode("this is supposed to be a tag","this is supposed to be a value",["this is a child","this is also a child"],{"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.props_to_html()," href=\"https://www.google.com\" target=\"_blank\"")


    def test_node_does_print(self):
        node = HTMLNode("this is supposed to be a tag","this is supposed to be a value",["this is a child","this is also a child"],{"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.__repr__(),f"HTMLNode({node.tag},{node.value},{node.children},{node.props})")




    





if __name__ == "__main__":
    unittest.main()