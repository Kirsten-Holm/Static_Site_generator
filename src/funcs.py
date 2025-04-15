from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode,TextType
from blocks import Blocktype, block_to_block
import os
import shutil
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

def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        html = block_to_html_node(block)
        children.append(html)

    return ParentNode("div",children)



def block_to_html_node(block):
    block_type = block_to_block(block)
    match block_type:

        case Blocktype.PARAGRAPH:
            return paragraph_to_html_node(block)
        case Blocktype.HEADING:
            return heading_to_html_node(block)
        case Blocktype.CODE:
            return code_to_html_node(block)
        case Blocktype.QUOTE:
            return quote_to_html_node(block)
        case Blocktype.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case Blocktype.ORDERED_LIST:
            return olist_to_html_node(block)
        case _:
            raise ValueError ("Invalid Blocktype")

def text_to_children(text):
    textnodes = text_to_textnodes(text)

    children = []

    for node in textnodes:
        child = text_node_to_html_node(node)
        children.append(child)

    return children

def paragraph_to_html_node(block):
    block_text = " ".join(block.splitlines())

    children = text_to_children(block_text)

    return ParentNode("p",children)

def heading_to_html_node(block):
    heading_number = 0

    for char in block:
        if char == "#":
            heading_number += 1
        else:
            break
    if heading_number + 1 >= len(block):
        raise ValueError (f"Invalid heading level: {heading_number}")
    text = block[heading_number + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{heading_number}",children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    
    code_text = block[4:-3]
    code_text_node = TextNode(code_text,TextType.TEXT)
    child_node = text_node_to_html_node(code_text_node)
    code = ParentNode("code",[child_node])
    return ParentNode("pre",[code])

def quote_to_html_node(block):
    lines = block.split("\n")
    newlines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote")
        newlines.append(line.lstrip(">").strip())

    content = " ".join([line for line in newlines if line.strip()])
    children = text_to_children(content)
    return ParentNode("blockquote",children)


def ulist_to_html_node(block):

    lines = block.split("\n")

    html_nodes = []

    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        
        html_nodes.append(ParentNode("li",children))
    return ParentNode("ul",html_nodes)


def olist_to_html_node(block):

    lines = block.split("\n")

    html_nodes = []

    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        
        html_nodes.append(ParentNode("li",children))
    return ParentNode("ol",html_nodes)



def copy_contents(sourcedir,destdir):
    if not os.path.exists(sourcedir):
        raise Exception ("Invalid Path")
    if not os.path.exists(destdir):
        os.mkdir(destdir)

    for element in os.listdir(sourcedir):

        new_dest = os.path.join(destdir,element)
        new_source = os.path.join(sourcedir,element)

        if os.path.isfile(new_source):
            shutil.copy(new_source,new_dest)

        else:
             copy_contents(new_source,new_dest)




def extract_title(markdown):
    lines = markdown.splitlines()
    heading_line = ""
    for line in lines:
        if line.startswith("#"):
            if line.startswith("##"):
                raise Exception("h1 not found")
            else:
                if line[1] == " ":

                    return line[2::]
                return line[1::]
    raise Exception ("h1 not found")

def generate_page(from_path, template_path, dest_path,basepath="/"):

    print(f"Cooking up a page from {from_path} to {dest_path} using {template_path} as a basis, yum!")

    from_file = open(from_path, 'r')
    markdown_from_path = from_file.read()
    from_file.close()

    template_file = open(template_path, 'r')
    template = template_file.read()
    template_file.close()

    html_node = markdown_to_html_node(markdown_from_path)
    html_string = html_node.to_html()

    title = extract_title(markdown_from_path)
    template = template.replace("{{ Title }}",title)
    template = template.replace("{{ Content }}",html_string)
    template = template.replace("href=\"/\"",f"href=\"{basepath}")
    template = template.replace("src=\"/\"",f"src=\"{basepath}")


    dirname = os.path.dirname(dest_path)
    if dirname != "":
        os.makedirs(dirname, exist_ok=True)

    template_filled = open(dest_path, 'w')
    template_filled.write(template)
    



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath="/"):

    for dir in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content,dir)):
            generate_page(os.path.join(dir_path_content,"index.md"),template_path,os.path.join(dest_dir_path,"index.html"),basepath)
        else:
            generate_pages_recursive(os.path.join(dir_path_content,dir),template_path,os.path.join(dest_dir_path,dir),basepath)
     



