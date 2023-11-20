import yaml


# Función para cargar la configuración desde un archivo YAML
def load_config(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config


# Función para parsear la configuración de la Máquina de Turing desde el archivo YAML
def parse_config(config):
    # Obtener información relevante del archivo YAML
    q_states = config['q_states']
    delta = config['delta']

    # Función para reemplazar valores vacíos con '_'
    def replace_empty_with_underscore(value):
        return '_' if value == 'None' or value is None else str(value)

    # Diccionario para almacenar la configuración parseada
    parsed_config = {}

    # Iterar sobre las transiciones definidas en el archivo YAML
    for t in delta:
        # Obtener información específica de la transición
        initial_state = replace_empty_with_underscore(str(t['params']['initial_state']))

        # Manejar mem_cache_value y new_cache_value
        cache_value = replace_empty_with_underscore(str(t['params'].get('mem_cache_value', '_')))
        new_cache_value = replace_empty_with_underscore(str(t['output'].get('mem_cache_value', '_')))

        tape_input = replace_empty_with_underscore(t['params']['tape_input'])

        # Crear una clave única para identificar el estado y el valor de la caché
        state_cache_key = ((initial_state, cache_value), tape_input)

        # Obtener información sobre la cinta después de aplicar la transición
        new_state = replace_empty_with_underscore(str(t['output']['final_state']))
        tape_output = replace_empty_with_underscore(t['output']['tape_output'])
        tape_displacement = replace_empty_with_underscore(t['output']['tape_displacement'])

        # Ajustar el formato de la salida según lo requerido
        tape_values = ((new_state, new_cache_value), tape_output, tape_displacement)

        # Almacenar la información en el diccionario parseado
        parsed_config[state_cache_key] = tape_values

    return parsed_config


def get_turing_machine_attr(filename):
    config = load_config(filename)
    parsed_config = parse_config(config)

    input_symbols = set(config['alphabet'])
    alphabet = set(config['tape_alphabet'])
    states = set(config['q_states']['q_list'])
    initial_state = config['q_states']['initial']
    accepting_states = {config['q_states']['final']}
    transition_function = parsed_config
    simulation_strings = config['simulation_strings']

    return alphabet, input_symbols, states, initial_state, accepting_states, transition_function, simulation_strings




