L = -1
R = 1
S = 0


class TuringMachine:
    def __init__(self, alphabet: set, input_symbols: set, states: set, initial_state: str,
                 accepting_states: set, transition_function: dict, blank_symbol: str = "_"):
        """
        if blank_symbol not in alphabet:
            raise ValueError("Blank symbol must be in alphabet")
        if not input_symbols.issubset(alphabet):
            raise ValueError("Input symbols must be a subset of alphabet")
        if initial_state not in states:
            raise ValueError("Initial state must be in states")
        if not accepting_states.issubset(states):
            raise ValueError("Accepting states must be a subset of states")
        """

        self.alphabet = alphabet
        self.blank_symbol = blank_symbol
        self.input_symbols = input_symbols
        self.states = states
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transition_function = transition_function

        self.tape = None  # Tape is set in run method
        self.cache = self.blank_symbol
        self.current_state = initial_state

    def run(self, input_string: str):
        self.tape = Tape(input_string, self.blank_symbol)
        while self.current_state not in self.accepting_states:
            self.print_instant_description()

            curr_char = self.tape.get_current()
            new_state, new_cache, tape_output, head_direction = self.get_transition(self.current_state, curr_char,
                                                                                    self.cache)
            self.current_state = new_state
            self.cache = new_cache
            self.tape.write(tape_output)

            if head_direction == "R":
                self.tape.go_right()
            elif head_direction == "L":
                self.tape.go_left()
        print("cadena :" + input_string + " aceptada")

    def get_transition(self, state, tape_value, cache_value):
        if ((state, cache_value), tape_value) in self.transition_function:
            transition = self.transition_function[((state, cache_value), tape_value)]
            try:
                new_state = transition[0][0]
                new_cache = transition[0][1]
                tape_output = transition[1]
                head_direction = transition[2]
            except IndexError:
                exit("Transition function is not in the correct format")

            return new_state, new_cache, tape_output, head_direction
        else:
            print("No transition found for state: " + state + " tape_value: " + tape_value + " cache_value: "
                  + cache_value)
            exit()

    def print_instant_description(self):
        left_side = self.tape.get_left_side()
        right_side = self.tape.get_right_side()
        current_char = self.tape.get_current()
        state_tuple = self.current_state
        cache_value = self.cache

        print("꜔  " + left_side + " [" + state_tuple + ", " + cache_value + "] " + current_char + "," + right_side)


class Node:
    def __init__(self, value):
        self.char = value
        self.next = None
        self.prev = None


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
