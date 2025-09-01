import pandas as pd
from itertools import combinations

def tabla_combinada(matriz_aportes, requerimientos_potencia, avi_coma_vasc):     
    # Generar todas las combinaciones posibles de los IDs en la matriz de aportes  
    ids = matriz_aportes['Id'].unique()  # 'Id' es el nombre de la columna con los IDs
    combinaciones = []
    # Generar todas las combinaciones no repetitivas, de tamaño variable (n a m)
    for i in range(1, len(matriz_aportes) + 1):  
        comb = list(combinations(ids, i))  # Combinaciones de tamaño 'i'
        combinaciones.extend(comb)
    # Convertir las combinaciones a una lista de listas
    combinaciones = [list(comb) for comb in combinaciones]
    # Crear un DataFrame para la tabla combinada
    combinacion_df = pd.DataFrame({
        'ID': [i for i in range(len(combinaciones))],  # Asignar un ID para cada combinación
        'Combinacion': combinaciones
    })
    # Calcular el costo total de cada combinación, VASC Y VASCMAX
    costos = []
    costostotal = []
    for comb in combinaciones:
        costo_total = 0
        costo_maximototal = 0  # 🔹 Inicializa esta variable dentro del bucle
        for id in comb:
            costo_total += matriz_aportes[matriz_aportes['Id'] == id]['Costo'].values[0]
            costo_maximototal += matriz_aportes[matriz_aportes['Id'] == id]['CostoMaximoPorBarra'].values[0]             
        costos.append(costo_total)
        costostotal.append(costo_maximototal) 
    # Asignar los resultados a combinacion_df
    combinacion_df['CostoMaximo'] = costostotal
    combinacion_df['Costo'] = costos
    #Calcular la potencia de cada combinación
    # Identificar las columnas de potencia (desde la columna 7 en adelante)
    columnas_potencia = matriz_aportes.columns[6:]
    # Inicializar un diccionario para almacenar las sumas por columna
    potencias_por_barra = {col: [] for col in columnas_potencia}
    # Iterar sobre las combinaciones y calcular la suma de cada barra por combinación
    for comb in combinaciones:
        for col in columnas_potencia:
            potencia_total = 0
            for id in comb:
                fila = matriz_aportes[matriz_aportes['Id'] == id]
                potencia_total += fila[col].values[0]  # Sumar la columna específica
            potencias_por_barra[col].append(potencia_total)
    # Asignar cada columna de potencia al DataFrame de combinaciones
    for col, valores in potencias_por_barra.items():
        combinacion_df[col] = valores
    # Calcular el cumplimiento
    barras = requerimientos_potencia.iloc[:, 0].tolist()
    potencias = requerimientos_potencia.iloc[:, 1:].values
    barra_potencia_dict = {barras[i]: potencias[i][0] for i in range(len(barras))}
    cumplimiento = []
    # Comparamos la suma de potencias de cada barra con la suma de potencias de cada combinación
    for i in range(len(combinacion_df)):
        potencias_combinadas = combinacion_df.iloc[i, 4:].to_dict() 
        cumplimiento_total = 0
        # Comparamos si la columna de potencia de la combinación es mayor o igual a la potencia requerida
        for barra, potencia in potencias_combinadas.items():
            if potencia >= barra_potencia_dict[barra]:
                cumplimiento_total += 100  # Cumplimiento total para esta barra
            else:
                # Se calcula cuánto porcentaje cubre la potencia de la combinación con respecto a la potencia requerida
                cumplimiento_total += (potencia / barra_potencia_dict[barra]) * 100
        # Promediar el cumplimiento total entre todas las barras
        cumplimiento_total = cumplimiento_total / len(potencias_combinadas)
        cumplimiento.append(cumplimiento_total)
    combinacion_df['Cumplimiento'] = cumplimiento
    # agregar fila vasc y vasmax
    #agregar las columnas de vasc
    matriz_aportes['VASC'] = avi_coma_vasc['VASC']
    vasc = []
    for comb in combinaciones:
        vasc_total = 0
        for id in comb:
            vasc_total += matriz_aportes[matriz_aportes['Id'] == id]['VASC'].values[0]      
        vasc.append(vasc_total)
    # Asignar los resultados a combinacion_df
    combinacion_df['VASC'] = vasc
    # Calcular el VALOR MEDIO del proyecto
    # VASC/La suma de potencia de cada barra de la combinación 
    # Agregar fila Valor Medio a la tabla matriz_aportes
    valor_medio = []
    for i in range(len(combinacion_df)):
        # Sumar la potencia de cada barra de la combinación desde la columna 4 a la 8
        suma_potencia = combinacion_df.iloc[i, 4:9].sum()
        if suma_potencia != 0:
            valor_medio_total = combinacion_df.iloc[i]['VASC'] / suma_potencia
        else:
            valor_medio_total = 0  # Evitar división por cero
        valor_medio.append(valor_medio_total)
    # Asignar los resultados a combinacion_df
    combinacion_df['Valor Medio'] = valor_medio

    return combinacion_df