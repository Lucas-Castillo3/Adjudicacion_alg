import pandas as pd

def crear_matriz_aportes(ofertas, factores_participacion, requerimientos_potencia):
#CREAR MATRIZ DE APORTES
    #Extraemos los nombres de las columnas barra de la tabla factores_participacion, exepto la primera columna y segunda columna
    nombres_requerimientos = factores_participacion.columns[2:].tolist()  # Nombres de las columnas
    # Extraemos los nombres de las filas de la tabla requerimientos_potencia
    #nombres_requerimientos = requerimientos_potencia.iloc[:, 0].tolist()  # Nombres de las filas, columna 0
    # Crear la nueva tabla 'matriz_aportes' basada en la tabla 'ofertas' y agregar columnas con los nombres de 'requerimientos_potencia'
    matriz_aportes = ofertas.copy()  # Copiamos la tabla 'ofertas' para crear 'matriz_aportes'
    # Agregar nuevas columnas con los nombres de los requerimientos
    matriz_aportes = matriz_aportes[matriz_aportes['Barra'].notnull()]
    for nombre_requerimiento in nombres_requerimientos:
        matriz_aportes[nombre_requerimiento] = None  # Se agregan nuevas columnas con el nombre correspondiente
    # CALCULOS PARA MATRIZ DE APORTES
    # Iteramos sobre las filas de la tabla ofertas
    for i in range(len(matriz_aportes)):
        # Extraemos el valor de la tercera columna, primera fila de la tabla ofertas
        valor_oferta = matriz_aportes.iloc[i, 2]  # fila, columna (es el X)
        # Extraemos el nombre de la fila 1, columna 4 de la tabla ofertas
        nombre_requerimiento = matriz_aportes.iloc[i, 4]
        # Filtramos la tabla factores_participacion para que solo contenga las filas que coincidan con el nombre requerido
        factores_filtrados = factores_participacion[factores_participacion['Barra Candidata'] == nombre_requerimiento]
        # Iteramos sobre las columnas de la tabla factores_participacion (excluyendo la primera columna)
        for j in range(1, factores_filtrados.shape[1]-1):  # Comienza en 1 para omitir la primera columna
            # Extraemos la columna específica
            columna_factores = factores_filtrados.iloc[:, 1]  # Columna de la tabla filtrada
            if valor_oferta in columna_factores.values:
                # Si valor_oferta se encuentra en la columna_factores, asignamos el valor de la columna siguiente directamente
                indice = columna_factores[columna_factores == valor_oferta].index[0]  # Obtenemos el índice donde se encuentra el valor_oferta
                factor = factores_filtrados.at[indice, factores_filtrados.columns[j+1]]# Asignamos el valor de la columna siguiente
                resultado = (factor / 100) * valor_oferta  # Calculamos el resultado
            else:
                # Calculamos las diferencias absolutas entre valor_oferta y cada valor en la columna filtrada
                diferencias = columna_factores.apply(lambda x: abs(x - valor_oferta))
                # Obtenemos los índices de los dos valores más cercanos
                indices_cercanos = diferencias.nsmallest(2).index  # Retorna los índices de los 2 valores más pequeños               
                # Si los índices son válidos, extraemos los dos valores más cercanos
                dos_valores_cercanos = factores_filtrados.loc[indices_cercanos, 'Skss (Mva)'].tolist()
                # Asignamos los dos valores a variables diferentes
                valor_cercano_1 = dos_valores_cercanos[1]  # Este sería como el X1 del algoritmo
                valor_cercano_2 = dos_valores_cercanos[0]  # X2
                # Extraemos los valores de la columna siguiente (columna 2) para los mismos índices
                columna_siguiente = factores_filtrados.loc[indices_cercanos, factores_filtrados.columns[j + 1]].tolist()
                # Asignamos esos valores a nuevas variables
                valor_siguiente_1 = columna_siguiente[1]  # Este sería como el Y1 del algoritmo
                valor_siguiente_2 = columna_siguiente[0]  # Y2
                # Hacemos la interpolación
                a = ((valor_oferta - valor_cercano_1) / (valor_cercano_2 - valor_cercano_1))
                y = valor_siguiente_1 + (a * (valor_siguiente_2 - valor_siguiente_1))
                # Calculamos el resultado
                resultado = (y / 100) * valor_oferta
                # Almacenamos el resultado en la matriz_aportes bajo la columna con el mismo nombre de la barra candidata
            matriz_aportes.iloc[i, len(ofertas.columns) + j - 1] = resultado
    return matriz_aportes