import re
from enum import Enum

BlockType = Enum(
    "BlockType", ["PARAGRAPH", "HEADING", "CODE", "QUOTE", "ULIST", "OLIST"]
)


def markdown_to_blocks(markdown) -> list:
    blocks = []
    for block in markdown.split("\n\n"):
        if block.strip() != "":
            blocks.append(block.strip())
    return blocks


def block_to_block_type(markdown) -> BlockType:
    mdlines = markdown.split("\n")
    if len(re.findall(r"^#{1,6}\s+.+$", markdown, flags=re.MULTILINE)) > 0:
        return BlockType.HEADING
    elif len(re.findall(r"`{3}.+`{3}", markdown, flags=re.S)) > 0:
        return BlockType.CODE
    elif len(re.findall(r"^>.*$", markdown, flags=re.MULTILINE)) > 0:
        quoteblock = True
        for line in markdown.split("\n"):
            if not line.startswith(">"):
                quoteblock = False
        if quoteblock:
            return BlockType.QUOTE
        else:
            return BlockType.PARAGRAPH
    elif len(re.findall(r"^-.*$", markdown, flags=re.MULTILINE)) > 0:
        ulistblock = True
        for line in mdlines:
            if not line.startswith("- "):
                ulistblock = False
        if ulistblock:
            return BlockType.ULIST
        else:
            return BlockType.PARAGRAPH
    elif len(re.findall(r"^(\d+).+$", markdown, flags=re.MULTILINE)) > 0:
        olistblock = True
        for i in range(0, len(mdlines)):
            if not mdlines[i].startswith(f"{i + 1}. "):
                olistblock = False
        if olistblock:
            return BlockType.OLIST
        else:
            return BlockType.PARAGRAPH
    return BlockType.PARAGRAPH
