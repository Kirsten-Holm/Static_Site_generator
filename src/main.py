from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from funcs import *


md = """
This is **bolded** paragraph
text in a p
tag here

```
code node
more code in the code node
```

> This is a simple blockquote

> This is a blockquote
> that spans multiple lines
> in the markdown file

> You can also have **formatted text** within blockquotes
> 
> And even separate paragraphs if you include a blank
> line with just a ">" character.

This is another paragraph with _italic_ text and `code` here

- First item
- Second item
- Third item

+ Apple
+ Banana
+ Cherry

* Item 1
* Item 2
* Item 3


1. First item
2. Second item
3. Third item
4. Fourth item

"""

htmlnodes = markdown_to_html_node(md)

print(htmlnodes.to_html())

print("\n\n\n")

print("""<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><pre><code>code node
more code in the code node
</code></pre><blockquote><p>This is a simple blockquote</p></blockquote><blockquote><p>This is a blockquote that spans multiple lines in the markdown file</p></blockquote><blockquote><p>You can also have <b>formatted text</b> within blockquotes</p><p>And even separate paragraphs if you include a blank line with just a ">" character.</p></blockquote><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><ul><li>First item</li><li>Second item</li><li>Third item</li></ul><ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><ol><li>First item</li><li>Second item</li><li>Third item</li><li>Fourth item</li></ol></div>"""
)


