import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode("", "", None, {"test": "testvalue", "test2": "testvalue2"})
        self.assertEqual(node.props_to_html(), ' test="testvalue" test2="testvalue2"')

    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_not_dict(self):
        node = HTMLNode("", "", None, "test")
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_raw_text(self):
        node = LeafNode(None, "Testing!")
        self.assertEqual(node.to_html(), "Testing!")

    def test_to_html_a(self):
        node = LeafNode("a", "Test Link", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Test Link</a>'
        )

    def test_to_html_no_value(self):
        node = LeafNode()
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):
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

    def test_to_html_with_multiple_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("i", "grandchild2")
        grandchild_node3 = LeafNode("a", "grandchild3", {"href": "grandchild3.com"})
        grandchild_node4 = LeafNode(None, "grandchild4")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        child_node2 = ParentNode("span", [grandchild_node3, grandchild_node4])
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b>grandchild</b><i>grandchild2</i></span><span><a href="grandchild3.com">grandchild3</a>grandchild4</span></div>',
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_tag(self):
        child_node = LeafNode("b", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()
