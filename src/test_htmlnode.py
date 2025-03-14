import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_repr_empty(self):
        node = HTMLNode()
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(None, None, children: None, None)"
        )
        
    def test_prop_dict(self):
        prop_dict = {"test1": 'var_test', "test2": "var_test2"}
        node = HTMLNode("<a>", "Hello Testing", ["child1", "child2"], prop_dict)
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(<a>, Hello Testing, children: ['child1', 'child2'], {'test1': 'var_test', 'test2': 'var_test2'})"
        )

    def test_repr_sub(self):
        node = HTMLNode(value = "Just the value")
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(None, Just the value, children: None, None)"
        )
    
    def test_to_html_props(self):
        node = HTMLNode("div", "Hello World!", None, {"test1": 15, "test2": "var_test"})
        self.assertEqual(
            node.props_to_html(),
            ' test1="15" test2="var_test"'
        )
    
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click da link!", {"href": "www.xxx.com"})
        self.assertEqual(
            node.to_html(), 
            '<a href="www.xxx.com">Click da link!</a>'
            )
         
    def test_leaf_to_html_notag(self):
        node = LeafNode(None, "Testing 1 2 3")
        self.assertEqual(node.to_html(), "Testing 1 2 3")
        
if __name__ == "__main__":
    unittest.main()