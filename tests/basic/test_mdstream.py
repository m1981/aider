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


    def test_empty_string(self):
        text = ""
        pm = MarkdownStream()
        lines = pm._render_markdown_to_lines(text)
        full = pm._render_text(text).splitlines(keepends=True)
        self.assertEqual(lines, full)

    def test_single_paragraph_no_trailing_newline(self):
        text = "Hello world."
        self.assert_matches_full(text)

    def test_very_long_single_paragraph(self):
        text = ("word " * 200).strip() + "\n"
        self.assert_matches_full(text)

    def test_find_minimal_suffix_no_boundaries(self):
        # No blank lines at all — split at 0, entire text is suffix.
        text = "one\ntwo\nthree\n"
        pm = MarkdownStream()
        prefix_len, suffix = pm.find_minimal_suffix(text)
        self.assertEqual(prefix_len, 0)
        self.assertEqual(suffix, text)

    def test_find_minimal_suffix_closed_fence(self):
        # Blank line after a closed fence IS a valid split point.
        text = "intro\n\n```python\nx = 1\n```\n\nafter\n"
        pm = MarkdownStream()
        prefix_len, suffix = pm.find_minimal_suffix(text)
        self.assertNotIn("```python", text[:prefix_len])
        self.assertGreater(prefix_len, 0)


if __name__ == "__main__":
    unittest.main()
