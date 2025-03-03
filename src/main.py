from textnode import TextNode, TextType
from htmlnode import HTMLNode,LeafNode




TextNodeObject = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")



print(TextNodeObject.__repr__())