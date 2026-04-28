"""
Stack data structure implementation.
"""

class Stack:
    """
    A simple Stack data structure using a Python list.
    """
    def __init__(self):
        """
        Initialize an empty stack.
        """
        self.items = []
        
    def push(self, item):
        """
        Push an item onto the top of the stack.
        """
        self.items.append(item)
        
    def pop(self):
        """
        Pop and return the item at the top of the stack.
        Returns None if the stack is empty.
        """
        if not self.is_empty():
            return self.items.pop()
        return None
        
    def is_empty(self):
        """
        Check if the stack is empty.
        Returns True if empty, False otherwise.
        """
        return len(self.items) == 0
