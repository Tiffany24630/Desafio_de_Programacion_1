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