from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode




TextNodeObject = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")


print(TextNodeObject.__repr__())