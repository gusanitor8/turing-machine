class Tape:
    def __init__(self, string, blank_symbol):
        self.blank_symbol = blank_symbol
        self.current = None
        self.head = None
        self.tail = None
        self.origin = None

        self._set_initial_node(string[0])
        for char in string[1:]:
            self._set_next(char)
        self._return_to_origin()

    def go_right(self):
        if self.current.next is None:
            self._set_next(self.blank_symbol)
            # self.current = self.current.next
        else:
            self.current = self.current.next

    def go_left(self):
        if self.current.prev is None:
            self._set_prev(self.blank_symbol)
            # self.current = self.current.prev
        else:
            self.current = self.current.prev

    def write(self, value):
        self.current.char = value

    def get_current(self):
        return self.current.char

    def get_left_side(self):
        left = ""
        current = self.current

        while current.prev is not None:
            left = current.prev.char + ", " + left
            current = current.prev

        return left

    def get_right_side(self):
        right = ""
        current = self.current

        while current.next is not None:
            right += current.next.char + ", "
            current = current.next

        return right

    def _set_initial_node(self, value):
        self.origin = Node(value)
        self.current = self.origin

    def _set_next(self, value):
        new_node = Node(value)
        self.current.next = new_node
        new_node.prev = self.current
        self.current = new_node
        self.head = self.current

    def _set_prev(self, value):
        new_node = Node(value)
        self.current.prev = new_node
        new_node.next = self.current
        self.current = new_node
        self.tail = self.current

    def _return_to_origin(self):
        self.current = self.origin

    def __str__(self):
        right = self.get_right_side()
        left = self.get_left_side()

        return "[" + left + " >" + self.current.char + "," + right + "]"


class Node:
    def __init__(self, value):
        self.char = value
        self.next = None
        self.prev = None
