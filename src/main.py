from textnode import TextNode
from textnode import TextType




TextNodeObject = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")


print(TextNodeObject.__repr__())