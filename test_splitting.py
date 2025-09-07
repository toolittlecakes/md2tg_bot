#!/usr/bin/env python3
"""Test script to verify message splitting functionality."""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from handlers.message import _split_message

def test_split_message():
    """Test the _split_message function with various scenarios."""
    
    # Test 1: Short message (should not be split)
    short_text = "This is a short message."
    result = _split_message(short_text, max_length=100)
    assert len(result) == 1
    assert result[0] == short_text
    print("✓ Test 1 passed: Short message not split")
    
    # Test 2: Long message that needs splitting
    long_text = "This is a very long message that needs to be split into multiple parts because it exceeds the maximum length limit. " * 50
    result = _split_message(long_text, max_length=100)
    assert len(result) > 1
    for chunk in result:
        assert len(chunk) <= 100
    print(f"✓ Test 2 passed: Long message split into {len(result)} chunks")
    
    # Test 3: Message with line breaks
    multiline_text = "\n".join([f"Line {i}: This is line {i} with some content." for i in range(50)])
    result = _split_message(multiline_text, max_length=200)
    assert len(result) > 1
    for chunk in result:
        assert len(chunk) <= 200
    print(f"✓ Test 3 passed: Multiline message split into {len(result)} chunks")
    
    # Test 4: Very long single word (edge case)
    long_word = "a" * 150
    result = _split_message(long_word, max_length=100)
    assert len(result) >= 2
    print(f"✓ Test 4 passed: Very long word split into {len(result)} chunks")
    
    print("\nAll tests passed! Message splitting functionality works correctly.")

if __name__ == "__main__":
    test_split_message()
