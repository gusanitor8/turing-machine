L = -1
R = 1

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

        # TODO the machine must read blank if: tape is empty, tape is not empty and head is at the end of the tape
        self.tape = ""  # Tape is set in run method
        self.cache = ""

    def run(self, input_string: str):
        self.tape = self.blank_symbol + input_string + self.blank_symbol
