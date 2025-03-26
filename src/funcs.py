from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode,TextType
import re



def text_node_to_html_node(text_node):

    match text_node.TextType:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
        case _:
            raise ValueError ("TextType not supported, what did you do?")



def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        if node.TextType != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_nodes = []

        text_split = node.text.split(delimiter)

        if len(text_split)%2 == 0:
            raise ValueError ("Invalid Markdown Syntax, no closing delimiter!")

        for i in range(len(text_split)):
            if text_split[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(text_split[i],TextType.TEXT))
            else:
                split_nodes.append(TextNode(text_split[i],text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
        



def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return links


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.TextType != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_text = node.text
        images = extract_markdown_images(node_text)

        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            text_split= node_text.split(f"![{image[0]}]({image[1]})", 1)


            if len(text_split) != 2:
                raise ValueError ("Markdown Syntax error, link never closed!")
            
            if text_split[0] != "":
                
                new_nodes.append(TextNode(text_split[0],TextType.TEXT))

            
            new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))

            node_text = text_split[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text,TextType.TEXT))

    return new_nodes




def split_nodes_link(old_nodes):

    new_nodes = []
    for node in old_nodes:
        if node.TextType != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        links = extract_markdown_links(node_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            text_split= node_text.split(f"[{link[0]}]({link[1]})",1)


            if len(text_split) != 2:
                raise ValueError ("Markdown Syntax error, link never closed!")
            
            if text_split[0] != "":
                new_nodes.append(TextNode(text_split[0],TextType.TEXT))

            new_nodes.append(TextNode(link[0],TextType.LINK,link[1]))

            node_text = text_split[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text,TextType.TEXT))
        

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,"**",TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
