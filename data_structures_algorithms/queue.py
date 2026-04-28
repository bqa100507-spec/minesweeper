"""
Queue data structure implementation.
"""

class Queue:
    """
    A simple Queue data structure using a Python list.
    """
    def __init__(self):
        """
        Initialize an empty queue.
        """
        self.items = []
        
    def enqueue(self, item):
        """
        Add an item to the end of the queue.
        """
        self.items.append(item)
        
    def dequeue(self):
        """
        Remove and return the item at the front of the queue.
        Returns None if the queue is empty.
        """
        if not self.is_empty():
            return self.items.pop(0)
        return None
        
    def is_empty(self):
        """
        Check if the queue is empty.
        Returns True if empty, False otherwise.
        """
        return len(self.items) == 0
