import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
        
    def test_parent_to_html_base(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold Text"),
                LeafNode(None, "Normal Text"),
                LeafNode("i", "Italics Text"),
                LeafNode(None, "Normal Text")
            ]
        )
        self.assertEqual(node.to_html(), 
                         "<p><b>Bold Text</b>Normal Text<i>Italics Text</i>Normal Text</p>")
        
    def test_parent_to_html_grandfather(self):
        grandchild = LeafNode("p", "grandchild")
        child = ParentNode("span", [grandchild])
        child2 = LeafNode("b", "second child")
        parent = ParentNode("div", [child, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><span><p>grandchild</p></span><b>second child</b></div>",
            )
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
    

if __name__ == "__main__":
    unittest.main()