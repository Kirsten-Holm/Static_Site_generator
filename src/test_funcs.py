import unittest

from parentnode import ParentNode
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode,TextType
import re
from funcs import *

class TestTextToHtml(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK,"link.to.site")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), f"<a href=\"{html_node.props["href"]}\">This is a text node</a>")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE,"url/of/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), f"<img src=\"{html_node.props["src"]}\" alt=\"{html_node.props["alt"]}\" />") 
    


class TestSplitTextNode(unittest.TestCase):

    def test_codeblock(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        true_node = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes,true_node)

    def test_boldblock(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        true_node = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bold block", TextType.BOLD),
        TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes,true_node)


    
    def test_italicblock(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        true_node = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("italic block", TextType.ITALIC),
        TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes,true_node)


    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )





class TestExtractMarkdownImages(unittest.TestCase):

    def test_bootdev_example(self):
        func_result = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(func_result,[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])



class TestExtractMarkdownLinks(unittest.TestCase):
    
    def test_extract_link(self):
        func_result = extract_markdown_links( "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(func_result,[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])



class TestSplitNodesImagesAndLinks(unittest.TestCase):


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes
        )

    def test_split_images_more_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png) and here is a third ![third image](https://i.imgur.com/clunk.png)"
            "![foruth image](https://i.imgur.com/punnk.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and here is a third ", TextType.TEXT),
                TextNode("third image", TextType.IMAGE, "https://i.imgur.com/clunk.png"),
                TextNode("foruth image", TextType.IMAGE,"https://i.imgur.com/punnk.png")
            ],
            new_nodes
        )



    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
                        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ,],new_nodes
            )

class TestTextToTextNode(unittest.TestCase):

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            nodes, [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        )


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_dos(self):
        md = """
This might be **bolded** i hope anyway
this is stuck to the **bolded** text























this is a paragraph split wayyyyyyyyy away from the previous one, i hope it works...pls

-this is a list\n-with\n-a\n-new\n-word\n-on\n-every\n-line

-this is a fairly
-normal list
-just testin stuff out


            """
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This might be **bolded** i hope anyway\nthis is stuck to the **bolded** text",
                "this is a paragraph split wayyyyyyyyy away from the previous one, i hope it works...pls",
                "-this is a list\n-with\n-a\n-new\n-word\n-on\n-every\n-line","-this is a fairly\n-normal list\n-just testin stuff out"
            ],
        )






class TestMarkdownToHTMLNode(unittest.TestCase):


    def test_markdown_to_html_nodes_big_text(self):
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
        markdown_html = """<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><pre><code>code node
more code in the code node
</code></pre><blockquote>This is a simple blockquote</blockquote><blockquote>This is a blockquote that spans multiple lines in the markdown file</blockquote><blockquote>You can also have <b>formatted text</b> within blockquotes And even separate paragraphs if you include a blank line with just a ">" character.</blockquote><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><ul><li>First item</li><li>Second item</li><li>Third item</li></ul><ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><ol><li>First item</li><li>Second item</li><li>Third item</li><li>Fourth item</li></ol></div>"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, markdown_html)



    def test_heading(self):

        md = """
# this is heading one

this is a paragraph
lala
lala

## heading two here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><h1>this is heading one</h1><p>this is a paragraph lala lala</p><h2>heading two here</h2></div>")
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )




class TestExtractTitle(unittest.TestCase):

    def test_simple_heading(self):

        heading = "# simple heading"

        self.assertEqual(extract_title(heading),"simple heading")

    def test_multiple_heading(self):
        
        heading = """# real heading
bunch of fucking garbo
this also is trash
## heading 2 because haha
this is a scam"""

        self.assertEqual(extract_title(heading),"real heading")

if __name__ == "__main__":
    unittest.main()