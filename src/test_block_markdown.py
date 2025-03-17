import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_extra_lines(self):
        md = """
This is **bolded** paragraph then some extra lines



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph then some extra lines",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_lead_trail_lines(self):
        md = """
        
        
        
This is **bolded** paragraph then some extra lines



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items



        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph then some extra lines",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        

    def test_block_to_block_type_heading(self):
        md = """# Heading block test"""
        btype = block_to_block_type(md)
        self.assertEqual(
            btype, BlockType.HEADING
        )
        
    def test_block_to_block_type_heading_not_extra(self):
        md = """######### Heading block test"""
        btype = block_to_block_type(md)
        self.assertEqual(
            btype, BlockType.PARAGRAPH
        )
        
    def test_block_to_block_type_heading_not_NS(self):
        md = """#Heading block test"""
        btype = block_to_block_type(md)
        self.assertEqual(
            btype, BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code(self):
        md = """```this is some code```"""
        btype = block_to_block_type(md)
        self.assertEqual(btype, BlockType.CODE)
        
    def test_block_to_block_type_quote(self):
        md = """>This is a test quote
>with and extra line
> and another"""
        btype = block_to_block_type(md)
        self.assertEqual(btype, BlockType.QUOTE)
        
    def test_block_to_block_type_unordered_list(self):
        md = """- this is a unordered list
- with some
- extra lines"""
        btype = block_to_block_type(md)
        self.assertEqual(btype, BlockType.ULIST)
    
    def test_block_to_block_type_ordered_list(self):
        md = """1. testing
2. ordered
3. list"""
        btype = block_to_block_type(md)
        self.assertEqual(btype, BlockType.OLIST)
        

    def test_block_to_block_types_new(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
if __name__ == "__main__":
    unittest.main()
    
    