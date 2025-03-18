from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from funcs import *




TextNodeObject = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")

node_image = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
node_link = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
                        )

nodes = split_nodes_link([node_link])

for node_ in nodes:
    print(node_)

#images = extract_markdown_images(node.text)
#for image in images:
#   print(node.text.split(f"![{image[0]}]({image[1]})"))

#print(TextNodeObject.__repr__())