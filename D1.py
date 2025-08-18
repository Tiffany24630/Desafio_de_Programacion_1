"""
# MM2015 - Desafío de programación 1: Lógica proposicional
# autor: macastillo

# NOTA:
# Debe utilizar letras minúsculas para los nombres de las variables, por ejemplo, a, b, c.
# Puede utilizar paréntesis para agrupar expresiones, como «a and (b or c)».

# Implemente las cuatro funciones siguientes:
# tabla_verdad, tautologia, equivalentes e inferencia

# Entrega:
# Deberá subir este archivo a la página del curso en Canvas.
"""


######## No modifique el siguiente bloque de código ########
# ********************** COMIENZO *******************************

from functools import partial
import re


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
def implies(p, q) :
    return not p or q

@Infix
def iff(p, q) :
    return (p |implies| q) and (q |implies| p)

# Debe utilizar esta función para extraer variables.
# Esta función toma una expresión como entrada y devuelve una lista ordenada de variables.
# NO modifique esta función.

def extract_variables(expression):
    sorted_variable_set = sorted(set(re.findall(r'\b[a-z]\b', expression)))
    return sorted_variable_set


# ********************** FIN *******************************



############## IMPLEMENTAR LAS SIGUIENTES FUNCIONES  ##############
############## No modificar las definiciones de las funciones ##############

# Función: tabla_verdad
# Esta función calcula una tabla de verdad para una expresión dada.
# Entrada: expresión.
# Salida: tabla de verdad como una lista de listas.

# ================== GENERAR COMBINACIONES ================== (Tabla de verdad)
def _generar_combinaciones(n):
    if n == 0:
        return [()]
    combinaciones = []
    for i in range(2**n):
        binario = format(i, f'0{n}b')
        combo = tuple(bit == '1' for bit in binario)
        combinaciones.append(combo)
    return combinaciones

# ================== EVALUAR EXPRESIÓN CON CONTEXTO ================== (Tabla de verdad)
def _evaluar_expresion(expr, variables, valores):
    contexto = dict(zip(variables, valores))
    contexto['implies'] = implies
    contexto['iff'] = iff
    try:
        return eval(expr, {"__builtins__": {}}, contexto)
    except:
        raise ValueError(f"Error al evaluar la expresión: {expr}")

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
    

# Función: tautologia
# Esta función determina si la expresión es una tautología, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión.
# Salida: booleano.

def tautologia(expr):
    expresion = extract_variables(expr)
    var = len(expresion)

    for i in range(2**var): 
        val = {}
        for j, vars in enumerate(expresion):
            val[vars] = bool((i >> (var - j - 1)) & 1)
        
        if not eval(expr, {}, val): 
            return False #Si hay alguna expresión que no sea verdadera
        
    return True #Si todas las expresiones son verdaderas

# Función: equivalentes
# Esta función determina si expr1 es equivalente a expr2, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión 1 y expresión 2.
# Salida: booleano.
def equivalentes(expr1, expr2):
    # Extraer variables de ambas expresiones
    vars1 = extract_variables(expr1)
    vars2 = extract_variables(expr2)
    
    # Si las variables no son las mismas, no son equivalentes
    if vars1 != vars2:
        return False
    
    variables = vars1
    n = len(variables)
    
    # Si no hay variables, comparamos directamente las expresiones constantes
    if n == 0:
        try:
            # Evaluamos las expresiones sin variables
            val1 = eval(expr1)
            val2 = eval(expr2)
            return val1 == val2
        except:
            # Si hay error en la evaluación, asumimos que no son equivalentes
            return False
    
    # Generar todas las combinaciones de valores de verdad
    for i in range(2**n):
        # Crear el contexto de evaluación con los valores de verdad
        context = {}
        for j in range(n):
            # Asignar True o False según el bit correspondiente
            context[variables[j]] = bool((i >> (n - 1 - j)) & 1)
        
        try:
            # Evaluar ambas expresiones con el mismo contexto
            val1 = eval(expr1, {}, context)
            val2 = eval(expr2, {}, context)
            
            # Si los valores difieren en alguna combinación, no son equivalentes
            if val1 != val2:
                return False
        except:
            # Si hay error en la evaluación, asumimos que no son equivalentes
            return False

    return True

# Función: inferencia
# Esta función determina los valores de verdad para una valuación de una proposición dada.
# Entrada: expresión.
# Salida: lista de listas.

def inferencia(expr):
    # Separar la expresión en la parte lógica y el valor esperado
    if expr.count('=') != 1:
        raise ValueError("La expresión debe contener exactamente un '='")
    
    expr_logica, valor_str = expr.split('=', 1)
    expr_logica = expr_logica.strip()
    valor_str = valor_str.strip()
    
    # Validar el valor esperado (0 o 1)
    if valor_str not in ['0', '1']:
        raise ValueError("Valor esperado debe ser 0 o 1")
    
    valor_esperado = (valor_str == '1')
    
    # Extraer variables de la expresión lógica
    variables = extract_variables(expr_logica)
    n = len(variables)
    soluciones = []
    
    # Generar todas las combinaciones de valores de verdad (2^n)
    for i in range(2**n):
        # Crear representación binaria de n bits
        bin_str = bin(i)[2:].zfill(n)
        # Convertir cada bit a booleano (True/False)
        valores = [bit == '1' for bit in bin_str]
        # Crear contexto: mapear variables a sus valores
        contexto = dict(zip(variables, valores))
        
        try:
            # Evaluar la expresión lógica en el contexto actual
            resultado = eval(expr_logica, globals(), contexto)
        except Exception as e:
            raise ValueError(f"Error al evaluar: {expr_logica}") from e
        
        # Si coincide con el valor esperado, guardar la asignación
        if resultado == valor_esperado:
            soluciones.append(valores)
            
    return soluciones

op = 0
mensg = ""

while (op != 5):
    print("Ingrese la opción que desea realizar: \n1. Tabla de verdad. \n2. Tautología. \n3. Euivalentes. \n4. Inferencia. \n5. Salir.")
    op = input()

    match op:
        case 1: #Tabla de verdad
            print("Ingrese la expresión de la que desea hacer una tabla de verdad:")
            expr = input()
            mensg = "La tabla de verdad de la expresión " + expr + " es: \n" + tabla_verdad(expr)
        
        case 2: #Tautología
            print("Ingrese la expresión de la que desea comprobar si es una tautología:")
            expr = input()
            mensg = "¿La expresión " + expr + " es una tautología? \n" + str(tautologia(expr))

        case 3: #Equivalentes
            print("Ingrese la primera expresión a comparar:")
            exprA = input()
            print("Ingrese la segunda expresión a comparar:")
            exprB = input()
            mensg = "¿La expresión " + exprA + " es equivalente a " + exprB + "? \n" + str(equivalentes(exprA, exprB))

        case 4: #Inferencia
            print("Ingrese la expresión de la cual quiere hacer una inferencia:")
            expr = input()
            mensg = "La inferencia de la expresión " + expr + " es: \n" + inferencia(expr)

        case 5: #Salir
            mensg = "Ha seleccionado salir..."

        case _: #Default
            mensg = "Ingrese una opción correcta..."

    print(mensg)
