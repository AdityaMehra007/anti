import time
import unittest
from byox.regex.nfa import match, search

class TestRegex(unittest.TestCase):
    def test_literal_and_wildcard(self):
        self.assertTrue(match("hello", "hello"))
        self.assertFalse(match("hello", "world"))
        self.assertTrue(match("h.llo", "hello"))
        self.assertTrue(match("h.llo", "hallo"))
        self.assertFalse(match("h.llo", "hllo"))

    def test_concatenation_and_alternation(self):
        self.assertTrue(match("cat|dog", "cat"))
        self.assertTrue(match("cat|dog", "dog"))
        self.assertFalse(match("cat|dog", "bird"))
        self.assertTrue(match("a(b|c)d", "abd"))
        self.assertTrue(match("a(b|c)d", "acd"))
        self.assertFalse(match("a(b|c)d", "aed"))

    def test_quantifiers_star_plus_opt(self):
        # Star *
        self.assertTrue(match("ab*c", "ac"))
        self.assertTrue(match("ab*c", "abc"))
        self.assertTrue(match("ab*c", "abbbbbc"))
        self.assertFalse(match("ab*c", "abx"))

        # Plus +
        self.assertFalse(match("ab+c", "ac"))
        self.assertTrue(match("ab+c", "abc"))
        self.assertTrue(match("ab+c", "abbbc"))

        # Optional ?
        self.assertTrue(match("colou?r", "color"))
        self.assertTrue(match("colou?r", "colour"))
        self.assertFalse(match("colou?r", "colouur"))

    def test_character_classes(self):
        self.assertTrue(match("[a-z]+", "hello"))
        self.assertFalse(match("[a-z]+", "HELLO"))
        self.assertTrue(match("[0-9]+", "12345"))
        self.assertTrue(match("[a-zA-Z0-9_]+", "User_123"))
        
        # Negated class
        self.assertTrue(match("[^0-9]+", "abcXYZ"))
        self.assertFalse(match("[^0-9]+", "abc1XYZ"))

    def test_anchors_and_search(self):
        # Match matches full string unless search is used
        self.assertTrue(search("cat", "a big cat in the hat"))
        self.assertFalse(search("dog", "a big cat in the hat"))
        
        # Anchors
        self.assertTrue(match("^cat", "cat"))
        self.assertTrue(match("cat$", "cat"))
        self.assertTrue(search("^cat", "cat and mouse"))
        self.assertFalse(search("^cat", "the cat and mouse"))

    def test_no_catastrophic_backtracking(self):
        # Pathological pattern for backtracking engines: (a?)^n a^n
        # Thompson NFA evaluates in linear time
        pattern = "a?" * 25 + "a" * 25
        text = "a" * 25
        t0 = time.perf_counter()
        res = match(pattern, text)
        duration = time.perf_counter() - t0
        self.assertTrue(res)
        self.assertLess(duration, 0.5)  # Should finish in milliseconds, not exponential

if __name__ == "__main__":
    unittest.main()
