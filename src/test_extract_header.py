import unittest

from extract_header import extract_title

class TestTitleExtractor:
    def test_title_one(self):
        md = "# Simple Test"
        title = extract_title(md)
        
        self.assertEqual(title, "Simple Test")
        
    def test_title_two(self):
        md = """
        This is a longer
        text string
        with a 
        # Header in it
        """
        title = extract_title(md)
        
        self.assertEqual(title, "Header in it")
        
if __name__ == "__main__":
    unittest.main()