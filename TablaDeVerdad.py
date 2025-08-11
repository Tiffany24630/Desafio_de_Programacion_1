# ================== DEPENDENCIAS BÁSICAS ==================
from functools import partial
import re

# ================== OPERADORES INFIX (implies, iff) ==================
class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)

@Infix
def implies(p, q):
    return not p or q

@Infix
def iff(p, q):
    return (p |implies| q) and (q |implies| p)

# ================== UTILIDAD: EXTRAER VARIABLES ==================
def extract_variables(expression):
    # letras minúsculas de una sola letra: a, b, c, ...
    sorted_variable_set = sorted(set(re.findall(r'\b[a-z]\b', expression)))
    return sorted_variable_set

# ================== GENERAR COMBINACIONES ==================
def _generar_combinaciones(n):
    if n == 0:
        return [()]
    combinaciones = []
    for i in range(2**n):
        binario = format(i, f'0{n}b')
        combo = tuple(bit == '1' for bit in binario)
        combinaciones.append(combo)
    return combinaciones

# ================== EVALUAR EXPRESIÓN CON CONTEXTO ==================
def _evaluar_expresion(expr, variables, valores):
    contexto = dict(zip(variables, valores))
    contexto['implies'] = implies
    contexto['iff'] = iff
    try:
        return eval(expr, {"__builtins__": {}}, contexto)
    except:
        raise ValueError(f"Error al evaluar la expresión: {expr}")

# ================== TABLA DE VERDAD (OPCIÓN 1) ==================
def tabla_verdad(expr):
    try:
        variables = extract_variables(expr)
        combinaciones = _generar_combinaciones(len(variables))
        tabla = []
        for combo in combinaciones:
            resultado = _evaluar_expresion(expr, variables, combo)
            fila = list(combo) + [resultado]
            tabla.append(fila)
        return variables, tabla
    except Exception as e:
        raise ValueError(f"Error en tabla_verdad: {str(e)}")

# ================== MENÚ (SOLO TABLA DE VERDAD Y SALIR) ==================
def mostrar_menu():
    print("\n" + "="*50)
    print("MM2015 - Lógica Proposicional")
    print("="*50)
    print("1. Tabla de verdad")
    print("2. Finalizar")
    print("="*50)

def main():
    while True:
        mostrar_menu()
        try:
            opcion = input("Seleccione una opción (1-2): ").strip()

            if opcion == '1':
                expr = input("Ingrese la expresión: ").strip()
                variables, resultado = tabla_verdad(expr)

                print(f"\nTabla de verdad para '{expr}':")
                print(resultado)
                
            elif opcion == '2':
                print("¡Hasta luego!")
                break

            else:
                print("Opción no válida. Por favor, seleccione 1 o 2.")

        except Exception as e:
            print(f"Error: {e}")
            print("Por favor, verifique la sintaxis de su expresión.")

if __name__ == "__main__":
    main()