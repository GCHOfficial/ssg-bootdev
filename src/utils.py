import os
import re
import shutil

from blocks import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, ParentNode
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
                    if len(lines) == 1:
                        listitems.append(ParentNode("p", text_to_children(currentitem)))
                    else:
                        for j in range(i + 1, len(lines)):
                            nextitem = re.findall(r"^>(.*)$", lines[j], re.MULTILINE)[
                                0
                            ].lstrip()
                            if currentitem != "" and nextitem != "":
                                currentitem += " " + nextitem
                            elif currentitem != "" and nextitem == "":
                                listitems.append(
                                    ParentNode("p", text_to_children(currentitem))
                                )
                                break
                            if j == len(lines) - 1:
                                (
                                    listitems.append(
                                        ParentNode("p", text_to_children(currentitem))
                                    )
                                    if currentitem != ""
                                    else (
                                        listitems.append(
                                            ParentNode("p", text_to_children(nextitem))
                                        )
                                        if nextitem != ""
                                        else ()
                                    )
                                )
                children.append(ParentNode("blockquote", listitems))
            case BlockType.ULIST:
                listitems = []
                for listitem in block.split("\n"):
                    listitems.append(
                        ParentNode(
                            "li",
                            text_to_children(
                                re.findall(r"^-(.*)$", listitem, re.MULTILINE)[
                                    0
                                ].lstrip()
                            ),
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
                        ParentNode(
                            "li",
                            text_to_children(
                                re.findall(r"^\d+.(.+)$", listitem, re.MULTILINE)[
                                    0
                                ].lstrip()
                            ),
                        )
                    )
                children.append(
                    ParentNode(
                        "ol",
                        listitems,
                    )
                )
    return ParentNode("div", children)


def copy_static(static_path, docs_path) -> None:
    if os.path.exists(docs_path):
        for item in os.listdir(docs_path):
            item_path = os.path.join(docs_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    else:
        os.mkdir(docs_path)
    recursive_copy(static_path, docs_path)


def recursive_copy(folder, destination) -> None:
    if not os.path.exists(folder):
        print("Folder to copy doesn't exist")
        return
    if not os.path.exists(destination):
        os.mkdir(destination)
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isdir(item_path):
            recursive_copy(item_path, os.path.join(destination, item))
        else:
            shutil.copy(item_path, os.path.join(destination, item))


def extract_title(markdown) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.replace("#", "").lstrip()
    raise Exception("Title not found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            os.mkdir(os.path.join(dest_dir_path, item))
            generate_pages_recursive(
                item_path, template_path, os.path.join(dest_dir_path, item), basepath
            )
        else:
            generate_page(
                item_path,
                template_path,
                os.path.join(dest_dir_path, item.replace(".md", ".html")),
                basepath,
            )
