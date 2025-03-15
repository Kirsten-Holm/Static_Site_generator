from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from funcs import *




TextNodeObject = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")


print(extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"))

print(TextNodeObject.__repr__())