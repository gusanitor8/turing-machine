from Parser import get_turing_machine_attr
from TuringMachine import TuringMachine


def main():
    """
    alphabet, input_symbols, states, initial_state, accepting_states, transition_function, simulation_strings = (
        get_turing_machine_attr('Entrada.yaml'))

    tm = TuringMachine(alphabet, input_symbols, states, initial_state, accepting_states, transition_function)
    for string in simulation_strings:
        tm.run(string)
    """

    alphabet, input_symbols, states, initial_state, accepting_states, transition_function, simulation_strings = (
        get_turing_machine_attr('MT_alterador.yml'))

    tm = TuringMachine(alphabet, input_symbols, states, initial_state, accepting_states, transition_function)
    for string in simulation_strings:
        tm.run(string)


if __name__ == "__main__":
    main()

