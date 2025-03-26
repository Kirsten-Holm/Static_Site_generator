from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from funcs import *




TextNodeObject = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")

imagenode = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png) and here is a third ![third image](https://i.imgur.com/clunk.png)"
            "![foruth image](https://i.imgur.com/punnk.png)",
            TextType.TEXT)

nodes = split_nodes_image([imagenode])

for node in nodes:
    print(node)


"""
text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

nodes = text_to_textnodes(text)

for node in nodes:
    print(node)
"""