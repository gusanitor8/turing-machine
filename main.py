from Parser import get_turing_machine_attr
from TuringMachine import TuringMachine


def main():
    alphabet, input_symbols, states, initial_state, accepting_states, transition_function, simulation_strings = (
        get_turing_machine_attr('MT_reconocedora.yaml'))

    for string in simulation_strings:
        tm = TuringMachine(alphabet, input_symbols, states, initial_state, accepting_states, transition_function)

        tm.run(string)

    """
    alphabet, input_symbols, states, initial_state, accepting_states, transition_function, simulation_strings = (
        get_turing_machine_attr('MT_alteradora.yaml'))

    tm = TuringMachine(alphabet, input_symbols, states, initial_state, accepting_states, transition_function)
    for string in simulation_strings:
        tm.run(string)
    """


if __name__ == "__main__":
    main()
