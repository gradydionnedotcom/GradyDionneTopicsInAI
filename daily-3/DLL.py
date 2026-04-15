import random
from time import time

class Node:
    def __init__(self, v, p, n):
        self.value = v
        self.prev = p
        self.next = n
    def __str__(self):
        return str(self.value)

class DLLIterator:
    def __init__(self, header):
        self.current = header.next

    def __next__(self):
        if self.current.next is not None:
            v = self.current.value
            self.current = self.current.next
            return v
        else:
            raise StopIteration("no more values")

    def __iter__(self):
        return self

class DoublyLinkedList:
    def __init__(self):
        self.header = Node(None, None, None)
        self.trailer = Node(None, self.header, None)
        self.header.next = self.trailer
        self.size = 0

    def __iter__(self):
        return DLLIterator(self.header)

    def get_size(self):
        '''
        Returns the list size
        '''
        return self.size
    
    def is_empty(self):
        '''
        Returns true if the list is empty, false otherwise
        '''
        if self.size == 0:
            return True
        return False
    
    def get(self, index):
        '''
        Returns the value at the specified index
        '''
        node = self.header.next
        for i in range (index):
            node = node.next
        return node.value
    
    def first(self):
        '''
        Returns the first element in the list
        '''
        return self.header.next.value

    def last(self):
        '''
        Returns the last element in the list 
        '''
        return self.trailer.prev.value

    def __add_between(self, v, n1, n2):
        """add value between n1 and n2. n1 and n2 cannot be None
        n1 and n2 must be consecutive

        :param v: value
        :type v: anything
        :param n1: node before value to insert
        :type n1: Node
        :param n2: node after value to insert
        :type n2: Node
        """
        if n1 is None or n2 is None or n1.next is not n2 or n1 is n2:
            raise ValueError("n1 or n2 is not valid")
        
        #step1 : create a new node
        new_node = Node(v, n1, n2)

        #step 2: adjust next and prev of n1 and n2
        n1.next = new_node
        n2.prev = new_node

        #step 3: increase size
        self.size += 1

    def add_first(self, v):
        """
            parameters:
                v: type is the generic type E of the list
            return:
                None
            adds a the value v at the head of the list
        """
        self.__add_between(v, self.header, self.header.next)

    def add_last(self, v):
        """
            parameters:
                v: type is the generic type E of the list
            return value:
                None
            adds a the value v at the tail of the list
        """
        self.__add_between(v, self.trailer.prev, self.trailer)

    def __str__(self):
        result = ""
        ref = self.header
        for i in range(self.size):
            ref = ref.next
            result += str(ref.value) + ', '
        return result
    
    def remove_between(self, node1, node2):
        # check if either node1 or node2 is None. Raise a ValueError if so.
        if node1 == None or node2 == None:
            raise ValueError("No such node exists")

        # Check that node1 and node 2 has exactly 1 node between them, raise a ValueError if not
        if node1.next.next != node2:
            raise ValueError("You are deleting either none or more than one nodes")

        # Everything is in order, so delete the node between node1 and node2, 
        # returning the value that was stored in it
        value_to_return = node1.next.value
        node1.next = node1.next.next
        node2.prev = node2.prev.prev
        self.size -= 1
        return value_to_return
    
    def remove_first(self):
        return self.remove_between(self.header, self.header.next.next)

    def remove_last(self):
        return self.remove_between(self.trailer.prev.prev, self.trailer)
    
    def remove_at_index(self, index: int):
        '''
        removes an element from the linked list at a given index
        '''
        
        if index < 0 or index >= self.size:
            raise IndexError("Index Error")

        if index == 0:
            return self.remove_first()

        current = self.header.next
        for i in range(index - 1):
            current = current.next

        value_to_return = current.next.value
        current.next = current.next.next
        self.size -= 1
        return value_to_return

    def search(self, value):
        
        ref = self.header
        for i in range(self.size + 1):
            if ref.value == value:
                return i - 1
            else:
                ref = ref.next
        return - 1

''' 
def creat_double_linked_list(n):
    new_list = DoublyLinkedList()
    for i in range(n):
            new_list.add_first(i)
    return new_list

def main():
    
    l = DoublyLinkedList()
    for i in range(20):
        l.add_first(i)

    for num in l:
        print (num)

if __name__=="__main__":
    main()
'''