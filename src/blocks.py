from enum import Enum


class Blocktype(Enum):

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return Blocktype.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return Blocktype.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return Blocktype.PARAGRAPH
        return Blocktype.QUOTE
    if block.startswith(("- ","* ","+ ")):
        for line in lines:
            if not line.startswith(("- ","* ","+ ")):
                return Blocktype.PARAGRAPH
        return Blocktype.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return Blocktype.PARAGRAPH
            i += 1
        return Blocktype.ORDERED_LIST
    return Blocktype.PARAGRAPH
