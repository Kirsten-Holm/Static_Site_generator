from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode,TextType
from blocks import Blocktype, block_to_block
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


#function for splitting raw markdown representing a full document into a list of "block" strings
def markdown_to_blocks(markdown):
    #splitting on double newline as markdown blocks are separated by 1 blank line
    markdown_blocks = markdown.split("\n\n")

    markdown_blocks = [block.strip() for block in markdown_blocks]

    markdown_blocks = [block for block in markdown_blocks if block.strip()]

    return markdown_blocks
#here i will define some functions to help me make the markdown to html node function

def code_node_handler(block):
    raw_code_text = block.strip("```")
    if raw_code_text.startswith("\n"):
        raw_code_text = raw_code_text[1::]
    code_text_node = TextNode(raw_code_text,"code")

    code_node = text_node_to_html_node(code_text_node)

    return code_node



def remove_blockquote_markers(block):
    lines = block.split("\n")

    lines_clean = []

    for line in lines:
        if line.startswith(">"):
            cleaned_line = line[1:].strip(" ")
            lines_clean.append(cleaned_line)
        else:
            lines_clean.append(line)

    return "\n".join(lines_clean)

def quote_handler(block):
    paragraphs = remove_blockquote_markers(block).split("\n\n")

    formatted_paragraphs =[]

    for paragraph in paragraphs:
        lines = " ".join(paragraph.splitlines())

        children_text = text_to_textnodes(lines)
        children = [text_node_to_html_node(child) for child in children_text]
        p_node = HTMLNode("p",None,children)
        formatted_paragraphs.append(p_node)

    return formatted_paragraphs



    return quote_leafnodes

def list_handler(block):
    list_items = block.splitlines()

    if list_items[0].startswith(("* ","- ","+ ")):
        list_items_trimmed = [list_item[2::] for list_item in list_items ]

    if list_items[0].startswith("1. "):
        list_items_trimmed = [list_item[3::] for list_item in list_items]

    list_children = []
    for item in list_items_trimmed:
        list_children.append(LeafNode("li",item,None))

    return list_children
    

def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)

    Children_to_add = []

    for block in blocks:
        block_type = block_to_block(block)
        
        match block_type:
            case Blocktype.PARAGRAPH:
                block_split_joined = " ".join(block.splitlines())
                child_paragraph_textnodes = text_to_textnodes(block_split_joined)
                

                child_paragraph_leafnodes = [text_node_to_html_node(child) for child in child_paragraph_textnodes]
                Children_to_add.append(HTMLNode("p",None,child_paragraph_leafnodes,None))
            case Blocktype.HEADING:
                heading_num = block[:5].count('#')
                Children_to_add.append(HTMLNode(f"h{heading_num}",block,None,None))
            case Blocktype.CODE:
                children_code = code_node_handler(block)
                Children_to_add.append(HTMLNode("pre", None,[children_code],None))
            case Blocktype.QUOTE:
                quote_nodes = quote_handler(block)
                Children_to_add.append(HTMLNode("blockquote",None,quote_nodes,None))
            case Blocktype.UNORDERED_LIST:
                list_items = list_handler(block)
                Children_to_add.append(HTMLNode("ul",None,list_items,None))
            case Blocktype.ORDERED_LIST:
                list_items = list_handler(block)
                Children_to_add.append(HTMLNode("ol",None,list_items,None))
    
    return HTMLNode("div",None ,Children_to_add, None)
