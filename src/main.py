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


copy_contents(source,dest)