import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    new_nodes = []
    for node in old_nodes:
        split_nodes = node.text.split(delimiter, 2)
        if node.text_type is not TextType.TEXT or len(split_nodes) < 3:
            if len(split_nodes) % 2 == 0:
                raise Exception("Invalid Markdown syntax")
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
    return re.findall(r"!\[(.*?)\]\((.+?)\)", text)


def extract_markdown_links(text) -> list:
    return re.findall(r"(?<!!)\[(.*?)\]\((.+?)\)", text)


def split_nodes_image(old_nodes) -> list:
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        split_nodes = re.split(r"!\[.*?\]\(.+?\)", node.text, maxsplit=1)
        if len(split_nodes) == 0 or len(images) == 0:
            new_nodes.append(node)
            continue
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
        split_nodes = re.split(r"(?<!!)\[.*?\]\(.+?\)", node.text, maxsplit=1)
        if len(split_nodes) == 0 or len(links) == 0:
            new_nodes.append(node)
            continue
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
