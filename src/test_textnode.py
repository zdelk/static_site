import unittest

from textnode import TextNode, TextType, text_node_to_html_node

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
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_url(self):
        node = TextNode("This is a link node", TextType.LINK, "www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, 'This is a link node')
        self.assertEqual(
            html_node.to_html(),
            '<a href="www.boot.dev">This is a link node</a>',
        )
        
    def test_img(self):
        node = TextNode("image title", TextType.IMAGE, "www.image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="www.image.com" alt="image title"></img>'
        )
        

if __name__ == "__main__":
    unittest.main()
