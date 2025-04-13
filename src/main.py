from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from funcs import *

block = """>This is a quote
>That spans
>Many lines
>I sure hope it works
"""
print(block.split("\n"))