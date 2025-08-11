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

def tabla_verdad(expr):
    pass

# Función: tautologia
# Esta función determina si la expresión es una tautología, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión.
# Salida: booleano.

def tautologia(expr):
    var = len(extract_variables(expr))

    for i in range(2**var):
        val = {}
        for j, vars in enumerate(extract_variables(expr)):
            val[vars] = bool((i >> (var - j - 1)) & 1)
        
        if not eval(expr, {}, val):
            return False
        
    return True

# Función: equivalentes
# Esta función determina si expr1 es equivalente a expr2, devuelve True;
# en caso contrario, devuelve False.
# Entrada: expresión 1 y expresión 2.
# Salida: booleano.
def equivalentes(expr1, expr2):
    pass

# Función: inferencia
# Esta función determina los valores de verdad para una valuación de una proposición dada.
# Entrada: expresión.
# Salida: lista de listas.

def inferencia(expr):
    pass

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
            mensg = "¿La expresión " + expr + " es una tautología? \n" + tautologia(expr)

        case 3: #Equivalentes
            print("Ingrese la primera expresión a comparar:")
            exprA = input()
            print("Ingrese la segunda expresión a comparar:")
            exprB = input()
            mensg = "¿La expresión " + exprA + " es equivalente a " + exprB + "? \n" + equivalentes(exprA, exprB)

        case 4: #Inferencia
            print("Ingrese la expresión de la cual quiere hacer una inferencia:")
            expr = input()
            mensg = "La inferencia de la expresión " + expr + " es: \n" + inferencia(expr)

        case 5: #Salir
            mensg = "Ha seleccionado salir..."

        case _: #Default
            mensg = "Ingrese una opción correcta..."

    print(mensg)