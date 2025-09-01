import pandas as pd

def filtrar_tabla(tabla_ganadora, requerimientos_potencia, posiciones_libres, matriz_aportes):
    #a la tabla ganadora se le agregan 3 columnas de filtro
    #agregar columna f_costo
    tabla_ganadora['f_costo'] = None
    #comparamos la columna costo con el costo maximo
    tabla_ganadora['f_costo'] = tabla_ganadora['Costo'] <= tabla_ganadora['CostoMaximo'] #si el costo es menor o igual al costo maximo, se agrega True
    #agregar columna f_req
    tabla_ganadora['f_req'] = None 
    #Si la columna cumplimiento es mayor o igual a 100, se agrega True
    tabla_ganadora['f_req'] = tabla_ganadora['Cumplimiento'] >= 100
    #agregar columna f_pos
    tabla_ganadora['f_pos'] = None 
    # Crear un diccionario con las posiciones libres
    dic_posiciones = dict(zip(posiciones_libres['Barra'], posiciones_libres['Nbmax']))
    # Iterar sobre cada fila de la tabla ganadora
    for idx, row in tabla_ganadora.iterrows():
        combinacion_str = row['Combinacion']
        if isinstance(combinacion_str, list):
            combinacion = list(combinacion_str)  # Si es una lista, la usamos directamente
        else:
            # Si no es una lista, se supone que es una cadena de texto representando una lista
            combinacion = list(map(int, combinacion_str.strip('[]').split(',')))
        # Copiar el diccionario de posiciones libres para no modificar el original
        posiciones_temp = dic_posiciones.copy()
        # Obtener los nombres de las barras de la matriz de aportes según las IDs
        barras = matriz_aportes[matriz_aportes['Id'].isin(combinacion)]['Barra'].tolist()
        # Restar 1 por cada barra encontrada
        for barra in barras:
            if barra in posiciones_temp:
                posiciones_temp[barra] -= 1
        # Evaluar si todas las posiciones disponibles son ≥ 0
        tabla_ganadora.at[idx, 'f_pos'] = all(pos >= 0 for pos in posiciones_temp.values())
    #filtro 1: ordena en las primeras posiciones las combinaciones con las 3 condiciones True y eliminando las que no cumplen
    tabla_final = tabla_ganadora[tabla_ganadora['f_costo'] & tabla_ganadora['f_pos'] & tabla_ganadora['f_req'] &(tabla_ganadora['VASC'] <= 47230000)].copy() 
    # Extraemos sumamos la cantidad de combinaciones de ids en cada una de las filas y la guardamos en una nueva columna
    #tabla_final.loc[:, 'Cantidad de IDs'] = tabla_final['Combinacion'].apply(lambda x: len(x))
    # Dejamos solo las filas con más cantidad de IDs y la siguiente con más cantidad de IDs
    #tabla_final = tabla_final[tabla_final['Cantidad de IDs'] == tabla_final['Cantidad de IDs'].max()]
    # dejamos solo las columnas necesarias
    tabla_final = tabla_final[['Combinacion', 'CostoMaximo', 'Costo','Cumplimiento','VASC', 'Valor Medio']]
    #filtro 2: ordena las combinaciones restantes por costo
    tabla_final = tabla_final.sort_values(by='Valor Medio', ascending=True)
    return tabla_final