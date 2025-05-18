import unittest

import utils
from textnode import TextNode, TextType


class TestNodeUtils(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("Text with a **bold** word", TextType.TEXT)
        new_nodes = utils.split_nodes_delimiter([node], "**", TextType.BOLD)
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
        new_nodes = utils.split_nodes_delimiter([node], "**", TextType.BOLD)
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
        new_nodes = utils.split_nodes_delimiter([node], "_", TextType.ITALIC)
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
        new_nodes = utils.split_nodes_delimiter([node], "_", TextType.ITALIC)
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
        new_nodes = utils.split_nodes_delimiter([node], "`", TextType.CODE)
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
        new_nodes = utils.split_nodes_delimiter([node], "`", TextType.CODE)
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
        new_nodes = utils.split_nodes_delimiter(nodes, "**", TextType.BOLD)
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
        with self.assertRaises(Exception):
            utils.split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = utils.extract_markdown_images(
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
        matches = utils.extract_markdown_images("Text without images.")
        self.assertListEqual(matches, [])

    def test_extract_markdown_images_except_links(self):
        matches = utils.extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(matches, [])

    def test_extract_markdown_links(self):
        matches = utils.extract_markdown_links(
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
        matches = utils.extract_markdown_links("Text without links.")
        self.assertListEqual(matches, [])

    def test_extract_markdown_links_except_images(self):
        matches = utils.extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(matches, [])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = utils.split_nodes_image([node])
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
        new_nodes = utils.split_nodes_image([node])
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
        new_nodes = utils.split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
        )

    def test_split_images_text_only(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = utils.split_nodes_image([node])
        self.assertListEqual(new_nodes, [TextNode("This is plain text", TextType.TEXT)])

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = utils.split_nodes_link([node])
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
        new_nodes = utils.split_nodes_link([node])
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
        new_nodes = utils.split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("link", TextType.LINK, "https://www.google.com")],
        )

    def test_split_links_text_only(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = utils.split_nodes_link([node])
        self.assertListEqual(new_nodes, [TextNode("This is plain text", TextType.TEXT)])

    def test_text_to_textnodes(self):
        new_nodes = utils.text_to_textnodes(
            "This is **text** with an _italic_ word, `code` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
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
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )
