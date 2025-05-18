from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


def main() -> None:
    testnode = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    testnode2 = HTMLNode(
        "<a>", "test", ["test"], {"test": "testvalue", "test2": "testvalue2"}
    )
    testnode3 = LeafNode("a", "This is a link!", {"href": "http://www.google.com"})
    testnode4 = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(testnode)
    print(testnode2)
    print(testnode2.props_to_html())
    print(testnode3.to_html())
    print(testnode4.to_html())


if __name__ == "__main__":
    main()
