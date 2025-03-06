import unittest

from textnode import TextNode, TextType



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node =  TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_not_eq_type(self):
        node1 = TextNode("this is a text node",TextType.BOLD)
        node2 = TextNode("this is a text node",TextType.ITALIC)
        self.assertNotEqual(node1,node2)
    
    def test_not_eq_text(self):
        node1 = TextNode("this is a text node",TextType.ITALIC)
        node2 = TextNode("this is also a text node",TextType.ITALIC)
        self.assertNotEqual(node1,node2)
    
    def test_url(self):
        node_no_url = TextNode("this TextNode has no url",TextType.ITALIC)
        self.assertEqual(node_no_url.url,None)

    def test_not_eq_url(self):
        node1 = TextNode("this is a text node",TextType.ITALIC,"https://youtube.com")
        node2 = TextNode("this is a text node",TextType.ITALIC)
        self.assertNotEqual(node1,node2)


if __name__ == "__main__":
    unittest.main()