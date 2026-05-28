import unittest                                                                                                        
                                                                                                                       
from aider.mdstream import MarkdownStream                                                                              
                                                                                                                       
                                                                                                                       
class TestMarkdownStreamIncremental(unittest.TestCase):                                                                
    def _full_render(self, text):                                                                                      
        pm = MarkdownStream()                                                                                          
        return pm._render_text(text)                                                                                   
                                                                                                                       
    def _incremental_render(self, text):                                                                               
        pm = MarkdownStream()                                                                                          
        lines = pm._render_markdown_to_lines(text)                                                                     
        return "".join(lines)                                                                                          
                                                                                                                       
    def assert_matches_full(self, text):                                                                               
        full = self._full_render(text).splitlines(keepends=True)                                                       
        incremental = self._incremental_render(text).splitlines(keepends=True)                                         
        self.assertEqual(incremental, full)                                                                            
                                                                                                                       
    def test_plain_paragraphs(self):                                                                                   
        text = "Hello world.\n\nThis is a second paragraph.\n\nAnd a third.\n"                                         
        self.assert_matches_full(text)                                                                                 
                                                                                                                       
    def test_with_headers_and_lists(self):                                                                             
        text = (                                                                                                       
            "# Header\n\n"                                                                                             
            "Some intro text.\n\n"                                                                                     
            "- item one\n"                                                                                             
            "- item two\n\n"                                                                                           
            "## Sub header\n\n"                                                                                        
            "Closing words.\n"                                                                                         
        )                                                                                                              
        self.assert_matches_full(text)                                                                                 
                                                                                                                       
    def test_with_code_block(self):                                                                                    
        text = (                                                                                                       
            "Here is some code:\n\n"                                                                                   
            "```python\n"                                                                                              
            "def foo():\n"                                                                                             
            "\n"                                                                                                       
            "    return 42\n"                                                                                          
            "```\n\n"                                                                                                  
            "Done.\n"                                                                                                  
        )                                                                                                              
        self.assert_matches_full(text)                                                                                 
                                                                                                                       
    def test_open_code_fence_not_split(self):                                                                          
        # A blank line inside an unclosed fence must not become a stable split.                                        
        text = "intro\n\n```python\ndef foo():\n\n    return 1\n"                                                      
        pm = MarkdownStream()                                                                                          
        prefix_len, suffix = pm.find_minimal_suffix(text)                                                              
        # The split must occur before the opening fence, leaving the fence in                                          
        # the unstable suffix.                                                                                         
        self.assertIn("```python", suffix)                                                                             
                                                                                                                       
    def test_incremental_matches_full_when_streamed(self):                                                             
        text = (                                                                                                       
            "# Title\n\n"                                                                                              
            "Paragraph one.\n\n"                                                                                       
            "```python\n"                                                                                              
            "x = 1\n"                                                                                                  
            "y = 2\n"                                                                                                  
            "```\n\n"                                                                                                  
            "Paragraph two.\n"                                                                                         
        )                                                                                                              
        pm = MarkdownStream()                                                                                          
        # Simulate streaming by feeding progressively longer prefixes.                                                 
        for i in range(1, len(text) + 1):                                                                             
            pm._render_markdown_to_lines(text[:i])                                                                     
                                                                                                                       
        incremental = "".join(pm._render_markdown_to_lines(text)).splitlines(keepends=True)                            
        full = self._full_render(text).splitlines(keepends=True)                                                       
        self.assertEqual(incremental, full)                                                                            
                                                                                                                       
                                                                                                                       
if __name__ == "__main__":                                                                                             
    unittest.main()                                                                                                    
=======                                                                                                                
import unittest                                                                                                        
                                                                                                                       
from aider.mdstream import MarkdownStream                                                                              
                                                                                                                       
                                                                                                                       
class TestMarkdownStreamIncremental(unittest.TestCase):                                                                
    def _full_render(self, text):                                                                                      
        pm = MarkdownStream()                                                                                          
        return pm._render_text(text)                                                                                   
                                                                                                                       
    def _incremental_render(self, text):                                                                               
        pm = MarkdownStream()                                                                                          
        lines = pm._render_markdown_to_lines(text)                                                                     
        return "".join(lines)                                                                                          
                                                                                                                       
    def assert_matches_full(self, text):                                                                               
        full = self._full_render(text).splitlines(keepends=True)                                                       
        incremental = self._incremental_render(text).splitlines(keepends=True)                                         
        self.assertEqual(incremental, full)                                                                            
                                                                                                                       
    def test_plain_paragraphs(self):                                                                                   
        text = "Hello world.\n\nThis is a second paragraph.\n\nAnd a third.\n"                                         
        self.assert_matches_full(text)                                                                                 
                                                                                                                       
    def test_with_headers_and_lists(self):                                                                             
        text = (                                                                                                       
            "# Header\n\n"                                                                                             
            "Some intro text.\n\n"                                                                                     
            "- item one\n"                                                                                             
            "- item two\n\n"                                                                                           
            "## Sub header\n\n"                                                                                        
            "Closing words.\n"                                                                                         
        )                                                                                                              
        self.assert_matches_full(text)                                                                                 
                                                                                                                       
    def test_with_code_block(self):                                                                                    
        text = (                                                                                                       
            "Here is some code:\n\n"                                                                                   
            "```python\n"                                                                                              
            "def foo():\n"                                                                                             
            "\n"                                                                                                       
            "    return 42\n"                                                                                          
            "```\n\n"                                                                                                  
            "Done.\n"                                                                                                  
        )                                                                                                              
        self.assert_matches_full(text)                                                                                 
                                                                                                                       
    def test_open_code_fence_not_split(self):                                                                          
        # A blank line inside an unclosed fence must not become a stable split.                                        
        text = "intro\n\n```python\ndef foo():\n\n    return 1\n"                                                      
        pm = MarkdownStream()                                                                                          
        prefix_len, suffix = pm.find_minimal_suffix(text)                                                              
        # The split must occur before the opening fence, leaving the fence in                                          
        # the unstable suffix.                                                                                         
        self.assertIn("```python", suffix)                                                                             
                                                                                                                       
    def test_incremental_matches_full_when_streamed(self):                                                             
        text = (                                                                                                       
            "# Title\n\n"                                                                                              
            "Paragraph one.\n\n"                                                                                       
            "```python\n"                                                                                              
            "x = 1\n"                                                                                                  
            "y = 2\n"                                                                                                  
            "```\n\n"                                                                                                  
            "Paragraph two.\n"                                                                                         
        )                                                                                                              
        pm = MarkdownStream()                                                                                          
        # Simulate streaming by feeding progressively longer prefixes.                                                 
        for i in range(1, len(text) + 1):                                                                              
            pm._render_markdown_to_lines(text[:i])                                                                     
                                                                                                                       
        incremental = "".join(pm._render_markdown_to_lines(text)).splitlines(keepends=True)                            
        full = self._full_render(text).splitlines(keepends=True)                                                       
        self.assertEqual(incremental, full)                                                                            
                                                                                                                       
                                                                                                                       
if __name__ == "__main__":                                                                                             
    unittest.main()                                                                                                    
>>>>>>> REPLACE                                                                                                        
                                                                                                                       


Environment / How to run (IMPORTANT)                                                                                   

 • System has no python on PATH; use uv.                                                                               
 • The project's [browser] extra forces numpy==2.4.3 (Python ≥3.11), causing uv dependency resolution to FAIL across   
   the project's >=3.10 range. Do NOT try to run via the project env. Do not modify dependency/project files (not in   
   scope).                                                                                                             
 • Use an isolated throwaway env. Once the test file is created, run:                                                  

                                                                                                                       
uv run --no-project --python 3.13 --with pytest --with rich --with packaging python -m pytest                          
tests/basic/test_mdstream.py -v                                                                                        
                                                                                                                       

                                                                                                                       
uv run --no-project --python 3.13 --with rich --with packaging python -m aider.mdstream                                
                                                                                                                       


Files currently in the chat (editable)                                                                                 

aider/io.py, aider/mdstream.py, aider/__init__.py, aider/coders/base_coder.py, aider/coders/search_replace.py,         
aider/history.py, aider/models.py, aider/coders/editblock_coder.py, aider/coders/editblock_prompts.py                  


Next steps for the new chat                                                                                            

 1 Create tests/basic/test_mdstream.py (block above).                                                                  
 2 Run the pytest command above; confirm all tests pass.                                                               
 3 Optionally run the aider.mdstream demo to eyeball streaming output.                                                 
 4 Commit the new test file. 
