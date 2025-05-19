import re

from blocks import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    new_nodes = []
    for node in old_nodes:
        split_nodes = node.text.split(delimiter, 2)
        if node.text_type is not TextType.TEXT or len(split_nodes) < 3:
            if len(split_nodes) % 2 == 0:
                raise SyntaxError(
                    "Invalid Markdown syntax: Improper use of inline markdown"
                )
            new_nodes.append(node)
            continue
        else:
            (
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
                if split_nodes[0] != ""
                else ()
            )
            (
                new_nodes.append(TextNode(split_nodes[1], text_type))
                if split_nodes[1] != ""
                else ()
            )
            (
                new_nodes.append(TextNode(split_nodes[2], TextType.TEXT))
                if split_nodes[2] != ""
                else ()
            )
    if old_nodes != new_nodes:
        return split_nodes_delimiter(new_nodes, delimiter, text_type)
    else:
        return new_nodes


def extract_markdown_images(text) -> list:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text) -> list:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes) -> list:
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        split_nodes = re.split(r"!\[.*?\]\(.*?\)", node.text, maxsplit=1)
        if len(split_nodes) == 0 or len(images) == 0:
            new_nodes.append(node)
            continue
        elif images[0][1] == "":
            raise SyntaxError("Invalid Markdown syntax: Images must have an URL")
        else:
            (
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
                if split_nodes[0] != ""
                else ()
            )
            (
                new_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
                if images[0] != ()
                else ()
            )
            (
                new_nodes.append(TextNode(split_nodes[1], TextType.TEXT))
                if split_nodes[1] != ""
                else ()
            )
    if old_nodes != new_nodes:
        return split_nodes_image(new_nodes)
    else:
        return new_nodes


def split_nodes_link(old_nodes) -> list:
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        split_nodes = re.split(r"(?<!!)\[.*?\]\(.*?\)", node.text, maxsplit=1)
        if len(split_nodes) == 0 or len(links) == 0:
            new_nodes.append(node)
            continue
        elif links[0][0] == "" or links[0][1] == "":
            raise SyntaxError("Invalid Markdown syntax: Links must have text and URL")
        else:
            (
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
                if split_nodes[0] != ""
                else ()
            )
            (
                new_nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
                if links[0] != ()
                else ()
            )
            (
                new_nodes.append(TextNode(split_nodes[1], TextType.TEXT))
                if split_nodes[1] != ""
                else ()
            )
    if (old_nodes) != new_nodes:
        return split_nodes_link(new_nodes)
    else:
        return new_nodes


def text_to_textnodes(text) -> list:
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD
                    ),
                    "_",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )


def text_to_children(text) -> list:
    children = []
    for node in text_to_textnodes(text):
        children.append(node.to_html_node())
    return children


def markdown_to_html_node(markdown) -> HTMLNode:
    children = []
    for block in markdown_to_blocks(markdown):
        blocktext = block.replace("\n", " ")
        match (block_to_block_type(block)):
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", text_to_children(blocktext)))
            case BlockType.HEADING:
                if len(block.split("\n")) > 1:
                    raise SyntaxError(
                        "Invalid Markdown syntax: headings should have new lines before and after them"
                    )
                children.append(
                    ParentNode(
                        f"h{blocktext.count('#', 0, 5)}",
                        text_to_children(blocktext.replace("#", "").lstrip()),
                    )
                )
            case BlockType.CODE:
                children.append(
                    ParentNode(
                        "pre",
                        [
                            TextNode(
                                block.replace("```", "").lstrip(), TextType.CODE
                            ).to_html_node()
                        ],
                    )
                )
            case BlockType.QUOTE:
                listitems = []
                lines = block.split("\n")
                for i in range(0, len(lines)):
                    currentitem = re.findall(r"^>(.*)$", lines[i], re.MULTILINE)[
                        0
                    ].lstrip()
                    for j in range(i + 1, len(lines)):
                        nextitem = re.findall(r"^>(.*)$", lines[j], re.MULTILINE)[
                            0
                        ].lstrip()
                        if currentitem != "" and nextitem != "":
                            currentitem += " " + nextitem
                        elif currentitem != "" and nextitem == "":
                            listitems.append(LeafNode("p", currentitem))
                            break
                        if j == len(lines) - 1:
                            (
                                listitems.append(LeafNode("p", currentitem))
                                if currentitem != ""
                                else ()
                            )
                children.append(ParentNode("blockquote", listitems))
            case BlockType.ULIST:
                listitems = []
                for listitem in block.split("\n"):
                    listitems.append(
                        LeafNode(
                            "li",
                            re.findall(r"^-(.*)$", listitem, re.MULTILINE)[0].lstrip(),
                        )
                    )
                children.append(
                    ParentNode(
                        "ul",
                        listitems,
                    )
                )
            case BlockType.OLIST:
                listitems = []
                for listitem in block.split("\n"):
                    listitems.append(
                        LeafNode(
                            "li",
                            re.findall(r"^\d+.(.+)$", listitem, re.MULTILINE)[
                                0
                            ].lstrip(),
                        )
                    )
                children.append(
                    ParentNode(
                        "ol",
                        listitems,
                    )
                )
    return ParentNode("div", children)
