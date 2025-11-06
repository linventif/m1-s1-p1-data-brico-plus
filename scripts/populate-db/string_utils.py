# -*- coding: utf-8 -*-
"""
String utility functions for database field size constraints
"""

def truncate_to_bytes(text, max_bytes):
    """
    Truncate a string to fit within max_bytes when encoded as UTF-8.
    This is necessary because Oracle VARCHAR2 measures byte length, not character length.
    
    Args:
        text: The string to truncate
        max_bytes: Maximum number of bytes allowed
        
    Returns:
        The truncated string that fits within max_bytes
    """
    if not text:
        return text
    
    # Fast path: if already under limit, return as-is
    encoded = text.encode('utf-8')
    if len(encoded) <= max_bytes:
        return text
    
    # Slow path: truncate character by character
    result = text
    while len(result.encode('utf-8')) > max_bytes and len(result) > 0:
        result = result[:-1]
    
    return result
