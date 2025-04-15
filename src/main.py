from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from funcs import *
import os
import shutil



cwd = os.getcwd()

source = os.path.join(cwd,"static")

dest = os.path.join(cwd,"public")

content_path = os.path.join(cwd,"content")

template_path = os.path.join(cwd,"template.html")

dest_file_path = os.path.join(dest,"index.html")

def main():
    print("Deleting public directory")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    copy_contents(source,dest)

    generate_pages_recursive(content_path,template_path,dest)

main()