import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_content(self):
        node = TextNode("This is a test node", TextType.TEXT)
        node2 = TextNode("This is anotha node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://test.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://test.com")
        self.assertEqual(node, node2)
        
    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
if __name__ == "__main__":
    unittest.main()
