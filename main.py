from Parser import get_turing_machine_attr
from TuringMachine import TuringMachine
BLANC = "B"

def main():
    # Turing machine 1
    print("Fibonacci Turing Machine")
    alphabet, input_symbols, states, initial_state, accepting_states, transition_function, simulation_strings = (
        get_turing_machine_attr('MT_fibonacci.yaml'))

    for string in simulation_strings:
        tm = TuringMachine(alphabet, input_symbols, states, initial_state, accepting_states, transition_function, BLANC)

        tm.run(string)

    # # Turing machine 2
    # print("Second Turing Machine: Alteradora")
    # alphabet, input_symbols, states, initial_state, accepting_states, transition_function, simulation_strings = (
    #     get_turing_machine_attr('MT_alteradora.yaml'))
    #
    # for string in simulation_strings:
    #     tm = TuringMachine(alphabet, input_symbols, states, initial_state, accepting_states, transition_function)
    #     tm.run(string)


if __name__ == "__main__":
    main()
