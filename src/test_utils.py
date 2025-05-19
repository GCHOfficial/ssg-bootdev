import unittest

from textnode import TextNode, TextType
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestNodeUtils(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("Text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_bold_multiple(self):
        node = TextNode("Bold word **here** and **here**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Bold word ", TextType.TEXT),
                TextNode("here", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("here", TextType.BOLD),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("Text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_italic_multiple(self):
        node = TextNode("Italic word _here_ and _here_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Italic word ", TextType.TEXT),
                TextNode("here", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("here", TextType.ITALIC),
            ],
        )

    def test_split_nodes_delimiter_code(self):
        node = TextNode("Text with `code` inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" inside", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_code_multiple(self):
        node = TextNode("Code `here` and `here`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Code ", TextType.TEXT),
                TextNode("here", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("here", TextType.CODE),
            ],
        )

    def test_split_nodes_delimiter_non_text_type(self):
        nodes = [
            TextNode("This is already bolded", TextType.BOLD),
            TextNode(", but this **needs** to be.", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is already bolded", TextType.BOLD),
                TextNode(", but this ", TextType.TEXT),
                TextNode("needs", TextType.BOLD),
                TextNode(" to be.", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_invalid_markdown(self):
        node = TextNode("Text with invalid** markdown`", TextType.TEXT)
        with self.assertRaises(SyntaxError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_images_no_image(self):
        matches = extract_markdown_images("Text without images.")
        self.assertListEqual(matches, [])

    def test_extract_markdown_images_except_links(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(matches, [])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            matches,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_markdown_links_no_link(self):
        matches = extract_markdown_links("Text without links.")
        self.assertListEqual(matches, [])

    def test_extract_markdown_links_except_images(self):
        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(matches, [])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_split_images_except_links(self):
        node = TextNode(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://www.google.com)", TextType.TEXT),
            ],
        )

    def test_split_images_image_only(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
        )

    def test_split_images_text_only(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [TextNode("This is plain text", TextType.TEXT)])

    def test_split_images_empty_text(self):
        node = TextNode(
            "This is an image without text ![](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is an image without text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_split_images_empty_url(self):
        node = TextNode("This is an image without URL ![image]()", TextType.TEXT)
        with self.assertRaises(SyntaxError):
            split_nodes_image([node])

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.boot.dev"),
            ],
        )

    def test_split_links_except_images(self):
        node = TextNode(
            "This is a text with a [link](https://www.google.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is a text with a ",
                    TextType.TEXT,
                ),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(
                    " and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT
                ),
            ],
        )

    def test_split_links_link_only(self):
        node = TextNode("[link](https://www.google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("link", TextType.LINK, "https://www.google.com")],
        )

    def test_split_links_text_only(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [TextNode("This is plain text", TextType.TEXT)])

    def test_split_links_empty_text(self):
        node = TextNode(
            "This is a link without text [](https://www.google.com)", TextType.TEXT
        )
        with self.assertRaises(SyntaxError):
            split_nodes_link([node])

    def test_split_links_empty_url(self):
        node = TextNode("This is a link without URL [link]()", TextType.TEXT)
        with self.assertRaises(SyntaxError):
            split_nodes_link([node])

    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes(
            "This is **text** with an _italic_ word, `code`, an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word, ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(", an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_textnodes_invalid_markdown(self):
        with self.assertRaises(SyntaxError):
            text_to_textnodes("This is invalid ** markdown __ with ![]()")

    def test_text_to_textnodes_text_only(self):
        new_nodes = text_to_textnodes(
            "This is just plain text, with nothing to be processed."
        )
        self.assertListEqual(
            new_nodes,
            [
                TextNode(
                    "This is just plain text, with nothing to be processed.",
                    TextType.TEXT,
                )
            ],
        )

    def test_markdown_to_html_node_paragraphs(self):
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

    def test_markdown_to_html_node_headings(self):
        md = """
# This is a headings test

## With multiple headings

###Improper syntax

####### And a non heading
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a headings test</h1><h2>With multiple headings</h2><p>###Improper syntax</p><p>####### And a non heading</p></div>",
        )

    def test_markdown_to_html_node_headings_no_space(self):
        md = """
# This is a headings test
# With stacked headings
        """

        with self.assertRaises(SyntaxError):
            node = markdown_to_html_node(md)
            node.to_html()

    def test_markdown_to_html_node_codeblock(self):
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

    def test_markdown_to_html_node_quote(self):
        md = """
> This is a list
> of Markdown quotes

>
> This should have
>
> multiple paragraphs
> to check

> and another one
with quotes misused
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a list of Markdown quotes</p></blockquote><blockquote><p>This should have</p><p>multiple paragraphs to check</p></blockquote><p>> and another one with quotes misused</p></div>",
        )

    def test_markdown_to_html_node_ul(self):
        md = """
- This is
- an unordered
- list

- with multiple lines
-

-and improper code
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is</li><li>an unordered</li><li>list</li></ul><p>- with multiple lines -</p><p>-and improper code</p></div>",
        )

    def test_markdown_to_html_node_ol(self):
        md = """
1. This is
2. an ordered
3. list

1. with multiple lines
2.

3. and improper

1.code
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is</li><li>an ordered</li><li>list</li></ol><p>1. with multiple lines 2.</p><p>3. and improper</p><p>1.code</p></div>",
        )
