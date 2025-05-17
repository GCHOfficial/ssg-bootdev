from enum import Enum

from htmlnode import HTMLNode, LeafNode

TextType = Enum("TextType", ["TEXT", "BOLD", "ITALIC", "CODE", "LINK", "IMAGE"])


class TextNode:
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node) -> bool:
        if (
            self.text == other_node.text
            and self.text_type == other_node.text_type
            and self.url == other_node.url
        ):
            return True
        return False

    def __repr__(self) -> str:
        return (
            f"TextNode(text: {self.text}, text_type: {self.text_type}, url: {self.url})"
        )

    def to_html_node(self) -> HTMLNode:
        match (self.text_type):
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise TypeError("Invalid text type")
