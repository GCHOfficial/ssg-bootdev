import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_different_text_types(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_to_html_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.to_html(), "<b>This is a bold text</b>")

    def test_text_to_html_italic(self):
        node = TextNode("This is an italic text", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.to_html(), "<i>This is an italic text</i>")

    def test_text_to_html_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.to_html(), "<code>This is code</code>")

    def test_text_to_html_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        html_node = node.to_html_node()
        self.assertEqual(
            html_node.to_html(), '<a href="https://www.google.com">This is a link</a>'
        )

    def test_text_to_html_image(self):
        node = TextNode(
            "This is an image",
            TextType.IMAGE,
            "https://www.boot.dev/img/bootdev-logo-full-small.webp",
        )
        html_node = node.to_html_node()
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://www.boot.dev/img/bootdev-logo-full-small.webp" alt="This is an image"></img>',
        )

    def test_text_to_html_unknown_type(self):
        node = TextNode("Test", None)
        with self.assertRaises(TypeError):
            node.to_html_node()


if __name__ == "__main__":
    unittest.main()
