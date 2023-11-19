L = -1
R = 1
S = 0


class TuringMachine:
    def __init__(self, alphabet: set, blank_symbol: str, input_symbols: set, states: set, initial_state: str,
                 accepting_states: set, transition_function: dict):

        if blank_symbol not in alphabet:
            raise ValueError("Blank symbol must be in alphabet")
        if not input_symbols.issubset(alphabet):
            raise ValueError("Input symbols must be a subset of alphabet")
        if initial_state not in states:
            raise ValueError("Initial state must be in states")
        if not accepting_states.issubset(states):
            raise ValueError("Accepting states must be a subset of states")

        self.alphabet = alphabet
        self.blank_symbol = blank_symbol
        self.input_symbols = input_symbols
        self.states = states
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transition_function = transition_function

        self.tape = None  # Tape is set in run method
        self.cache = ""
        self.current_state = initial_state

    def run(self, input_string: str):
        self.tape = Tape(input_string, self.blank_symbol)

        while self.current_state not in self.accepting_states:
            curr_char = self.tape.get_current()
            new_state, new_cache, tape_output, head_direction = self.get_transition(self.current_state, curr_char,
                                                                                    self.cache)
            self.current_state = new_state
            self.cache = new_cache
            self.tape.write(tape_output)

            if head_direction == R:
                self.tape.go_right()
            elif head_direction == L:
                self.tape.go_left()

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
            exit("No transition found for state: " + state + " tape_value: " + tape_value + " cache_value: "
                 + cache_value)


class Node:
    def __init__(self, value):
        self.char = ""
        self.next = None
        self.prev = None


class Tape:
    def __init__(self, string, blank_symbol):
        self.blank_symbol = blank_symbol
        self.current = None

        self._set_initial_node(string[0])
        for char in string[1:]:
            self._set_next(char)

    def go_right(self):
        if self.current.next is None:
            self._set_next(self.blank_symbol)
            self.current = self.current.next
        else:
            self.current = self.current.next

    def go_left(self):
        if self.current.prev is None:
            self._set_prev(self.blank_symbol)
            self.current = self.current.prev
        else:
            self.current = self.current.prev

    def write(self, value):
        self.current.char = value

    def get_current(self):
        return self.current.char

    def _set_initial_node(self, value):
        self.current = Node(value)

    def _set_next(self, value):
        self.current.next = Node(value)

    def _set_prev(self, value):
        self.current.prev = Node(value)
