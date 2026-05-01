import random

class Node:
    def __init__(self, v, n):
        self.value = v
        self.next = n
    
    def __str__(self):
        return str(self.value)
    
class SLLIterator:
    def __init__(self, head):
        self.current = head

    def __next__(self):
        if self.current is not None:
            v = self.current.value
            self.current = self.current.next
            return v
        else:
            raise StopIteration("no more values")

    def __iter__(self):
        return self

class SinglyLinkedList:

    def __init__(self):
        self.head = None
        self.size = 0

    def __str__(self):
        result = ""
        ref = self.head
        for i in range(self.size):
            if i == self.size - 1:
                result += str(ref)
            else:
                result += str(ref) + " "
            ref = ref.next
        return f"[{result}]"
    
    def __iter__(self):
        return SLLIterator(self.head)

    def get_size(self):
        return self.size
    
    def get(self, index):
        '''
        Returns the value at the specified index
        '''
        node = self.head
        for i in range (index):
            node = node.next
        return node.value

    def is_empty(self):
        '''
        Returns true if the list is empty, false otherwise
        '''
        if self.size == 0:
            return True
        return False

    def remove_first(self):
        '''
        removes and return the value of the first node
        '''
        #case 1: list is empty
        if self.size == 0:
            raise ValueError("list is empty")
        #case 2: list is not empty
        value_to_return = self.head.value
        self.head = self.head.next
        self.size -= 1
        return value_to_return

    def add_first(self, v):
        '''
        Adding a value at the head of the list
        returns nothing
        '''
        #step 1: create a new node
        new_node = Node(v, self.head)

        #step 2: change the head reference to point
        # to new node
        self.head = new_node

        #step 3: increment size
        self.size += 1

    def remove_last(self):
        '''
        Removes the element at the end of the list
        '''

        node = self.head
        for i in range(self.size - 2):
            node = node.next
        node.next = None
        self.size -= 1
    
    def add_last(self, v):
        '''
        Adds an element at the end of the list
        '''

        new_node = Node(v, None)
        if self.head is None:
            self.head = new_node
        else:
            node = self.head
            while node.next is not None:
                node = node.next
            node.next = new_node
        self.size += 1
    
    def min(self):
        '''
        returns the minimum value, or value error if the list is empty
        '''
        if self.size == 0:
            raise ValueError('The list is empty')
        
        min = self.head.value
        ref = self.head
        for i in range(self.size):
            if ref.value < min:
                min = ref.value
            ref = ref.next
        
        return min
    
    def remove_at_index(self, index: int):
        '''
        removes an element from the linked list at a given index
        '''
        
        if index < 0 or index >= self.size:
            raise IndexError("Index Error")

        if index == 0:
            return self.remove_first()

        current = self.head
        for i in range(index - 1):
            current = current.next

        value_to_return = current.next.value
        current.next = current.next.next
        self.size -= 1
        return value_to_return

    def rotate(self, n: int):

        if n < 0 or n > self.size:
            raise IndexError ("number out of list boundaries")
        rotate_list = []

        for i in range(n):
            rotate_list.append(self.head.value)
            self.head = self.head.next
            self.size -= 1
        
        for element in rotate_list:
            self.add_last(element)

def main():
    l = SinglyLinkedList()

    for i in range(10, 16):
        l.add_first(i)
    print(l)
    print(l)
    print(l.min())

    test=SinglyLinkedList()

    for i in range(20):
        num = random.randint(10, 99)
        test.add_last(num)

    for num in test:
        print(num)


if __name__ == "__main__":
    main()
