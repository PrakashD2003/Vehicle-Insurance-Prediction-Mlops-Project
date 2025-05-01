# from_root.py
import os

def from_root(*paths):
    """
    Returns an absolute path under the project root.
    """
    root = os.path.dirname(__file__)
    return os.path.join(root, *paths)
