import matplotlib.pyplot as plt
import cProfile
import pstats
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
from Parser import get_turing_machine_attr
from TuringMachine import TuringMachine

# Formatea las entradas a strings YAML-Friendly
def format_number(n):
    return f"- {'1' * n}|__1"

# Refresca los strings de simulacion del yaml
def refresh_yaml_file(file_path):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        cut_off_index = None
        for i, line in enumerate(lines):
            if "simulation_strings:" in line:
                cut_off_index = i + 1 
                break
        if cut_off_index is not None:
            file.seek(0)
            file.writelines(lines[:cut_off_index] + ['\n'])
            file.truncate()

# Mide el tiempo de ejecucion de la maquina de turing en ms
def profile_function(func, *args, **kwargs):
    pr = cProfile.Profile()
    pr.enable()
    func(*args, **kwargs)
    pr.disable()
    return pstats.Stats(pr).total_tt * 1000

# Agrega los strings al archivo yaml
def append_to_yaml(file_path, data):
    try:
        with open(file_path, 'a') as file:
            file.write("\n".join(data) + "\n")
    except IOError as e:
        print(f"Error, no se pudo escribir en {file_path}: {e}")

# Ejecutar la simulacion de la maquina de turing
def run_simulation(yaml_file_path):
    try:
        attrs = get_turing_machine_attr(yaml_file_path)
        exec_times = []
        for string in attrs[-1]:
            tm = TuringMachine(*attrs[:-1], "B")
            exec_time = profile_function(tm.run, string)
            exec_times.append(exec_time)
        return exec_times
    except Exception as e:
        print(f"Error No se pudo cargar la MT: {e}")
        return []

# Encuentra el mejor grado polinomial con el metodo del codo
def find_best_polynomial_degree(X, y):
    mse_values = []
    degrees = range(1, 10)
    for degree in degrees:
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        model.fit(X, y)
        y_pred = model.predict(X)
        mse = mean_squared_error(y, y_pred)
        mse_values.append(mse)
    best_degree = np.argmin(mse_values) + 1
    return best_degree, mse_values

# Grafica la regresion polinomial
def plot_polynomial_fit(X, y, degree):
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(X)
    model = LinearRegression().fit(X_poly, y)
    coef = model.coef_[0]
    intercept = model.intercept_[0]

    # Consrtuye el string de la ecuacion
    equation = f'y = {intercept:.2f}'
    for i, c in enumerate(coef[1:], start=1):
        if c >= 0:
            equation += f' + {c:.2f}x^{i}'
        else:
            equation += f' - {-c:.2f}x^{i}'

    print(f'Ecuación Polinomial: {equation}')

    X_plot = np.linspace(min(X), max(X), 100).reshape(-1, 1)
    X_plot_poly = poly_features.transform(X_plot)
    y_plot = model.predict(X_plot_poly)
    
    plt.scatter(X, y, color='blue', label='Datos reales')
    plt.plot(X_plot, y_plot, color='red', label=f'Grado del Polinomio {degree}')
    plt.xlabel('Tamaño Entrada')
    plt.ylabel('Tiempo de ejecución (ms)')
    plt.title(f'Regresión Polinomial')
    plt.legend()
    plt.show()

# Grafica la dispersion de puntos de los datos
def plot_dispersion(X, y):
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue')
    plt.xlabel('Tamaño Entrada')
    plt.ylabel('Tiempo de ejecución (ms)')
    plt.title('Dispersión de tiempos de ejecución')
    plt.grid(True)
    plt.show()


def main():
    numbers = list(range(1, 11))
    formatted_numbers = [format_number(n) for n in numbers]
    yaml_file_path = 'MT_fibonacci.yaml'
    refresh_yaml_file(yaml_file_path)
    append_to_yaml(yaml_file_path, formatted_numbers)
    exec_times = run_simulation(yaml_file_path)
    if exec_times:
        numbers_np = np.array(numbers).reshape(-1, 1)
        exec_times_np = np.array(exec_times).reshape(-1, 1)
        best_degree, mse_values = find_best_polynomial_degree(numbers_np, exec_times_np)
        plot_dispersion(numbers_np, exec_times_np)
        plot_polynomial_fit(numbers_np, exec_times_np, best_degree)

if __name__ == "__main__":
    main()
