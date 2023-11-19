from TuringMachine import TuringMachine, L, R, S

transition_function = {
    # ((current_state, cache),tape_value_input): ((new_state, new_cache), tape_output, head_directionRSL )
    (("0", "_"), "a"): (("1", "a"), "_", R),
    (("0", "_"), "b"): (("1", "b"), "_", R),
}
