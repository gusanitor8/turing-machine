from Tape import Tape


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
        self.print_current_string(input_string)

        while self.current_state not in self.accepting_states:
            self.print_instant_description()

            curr_char = self.tape.get_current()
            new_state, new_cache, tape_output, head_direction = self.get_transition(self.current_state, curr_char,
                                                                                    self.cache)
            if new_state is None:
                break

            self.current_state = new_state
            self.cache = new_cache
            self.tape.write(tape_output)

            if head_direction == "R":
                self.tape.go_right()
            elif head_direction == "L":
                self.tape.go_left()

        if self.current_state in self.accepting_states:
            self.print_is_accepted(input_string)
        else:
            self.print_is_rejected(input_string)

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
            return None, None, None, None

    def print_instant_description(self):
        left_side = self.tape.get_left_side()
        right_side = self.tape.get_right_side()
        current_char = self.tape.get_current()
        state_tuple = self.current_state
        cache_value = self.cache

        print("\t꜔  " + left_side + " [" + state_tuple + ", " + cache_value + "] " + current_char + "," + right_side)

    @staticmethod
    def print_is_accepted(string: str):
        print("The String: " + string + " is ACCCEPTED by the TM \n\n")

    @staticmethod
    def print_is_rejected(string: str):
        print("The String: " + string + " is REJECTED by the TM \n\n")

    @staticmethod
    def print_current_string(string: str):
        print("Current String: " + string)

