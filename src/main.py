import pandas as pd
import numpy as np
import time
from algoritmointerpolacion import crear_matriz_aportes 
from algoritmosinfiltrados import tabla_combinada
from algoritmosfiltros import filtrar_tabla

start_time = time.time()  # Guardar el tiempo de inicio

# Cargar datos
ofertas = pd.read_csv(r"C:\Users\lucas\OneDrive\Escritorio\Proyectos\algoritmo_adjudicación\data\ofertas.csv", sep=';', decimal=',')
print("📄 Ofertas:")
print(ofertas, "\n")
factores_participacion = pd.read_csv(r"C:\Users\lucas\OneDrive\Escritorio\Proyectos\algoritmo_adjudicación\data\factores_de_participacion.csv", sep=';', decimal=',')
print("📄 Factores de Participación:")
print(factores_participacion, "\n")
posiciones_libres = pd.read_csv(r"C:\Users\lucas\OneDrive\Escritorio\Proyectos\algoritmo_adjudicación\data\pocisiones_libres_por_barra.csv", sep=';', decimal=',')
print("📄 Posiciones Libres por Barra:")
print(posiciones_libres, "\n")
requerimientos_potencia = pd.read_csv(r"data\requerimientos_de_potencia_de_cc.csv", sep=';', decimal=',')
print("📄 Requerimientos de Potencia:")
print(requerimientos_potencia, "\n")
avi_coma_vasc = pd.read_csv(r"C:\Users\lucas\OneDrive\Escritorio\Proyectos\algoritmo_adjudicación\data\AVI_COMA_VASC.csv", sep=';', decimal=',')
print("📄 AVI_COMA_VASC:")
print(avi_coma_vasc, "\n")
# Variable de costo máximo en CLP
def calcular_vasc(pcc):
    if pcc < 450:
        return 11197
    elif 450 <= pcc < 650:
        return 9979
    elif 650 <= pcc < 850:
        return 8316
    else:
        return 7886

# Agregar la columna 'CostoMaximoPorBarra' correctamente
ofertas['CostoMaximoPorBarra'] = ofertas['Skss'].apply(calcular_vasc)
# Eliminar columnas que su costo supere al costo maximo
ofertas = ofertas[ofertas['Costo'] <= ofertas['CostoMaximoPorBarra']]
# Llamar al algoritmo para crear la matriz de aportes
matriz_aportes = crear_matriz_aportes(ofertas, factores_participacion, requerimientos_potencia)
# Mostrar la matriz de aportes
print("\n📊 Matriz de Aportes:")
print(matriz_aportes)

#Llamar al algoritmo para crear la tabla final
tabla_ganadora = tabla_combinada(matriz_aportes, requerimientos_potencia, avi_coma_vasc)
print("\nTabla Sin filtrar:")
print(tabla_ganadora)
#llamar funcion para filtrar la tabla
tabla_ganadora = filtrar_tabla(tabla_ganadora, requerimientos_potencia, posiciones_libres, matriz_aportes)
#Mostrar la tabla
print("\n🏆 Tabla Ganadora:")
print(tabla_ganadora)

# Guardar la tabla ganadora filtrada en un archivo CSV
output_path = r"C:\Users\lucas\OneDrive\Escritorio\Proyectos\algoritmo_adjudicación\data\tabla_ganadora.csv"
tabla_ganadora.to_csv(output_path, index=False, sep=';', decimal=',') 
#Mostrar la matriz de aportes pero solo con las ids que se encuentran en la primera fila de la tabla ganadora
# Obtener la primera fila de la tabla ganadora
primera_fila = tabla_ganadora.iloc[0]
# Obtener la lista de IDs de la primera fila
ids_primera_fila = primera_fila['Combinacion']
# Filtrar la matriz de aportes para mostrar solo las filas con los IDs de la primera fila
matriz_aportes_filtrada = matriz_aportes[matriz_aportes['Id'].isin(ids_primera_fila)]
matriz_aportes_filtrada = matriz_aportes_filtrada[['Id', 'Nombre', 'Skss','Costo', 'CostoMaximoPorBarra']]
# Mostrar la matriz de aportes filtrada
print("\nCOMBINACIÓN ÓPTIMA:")
print(matriz_aportes_filtrada)


# Medir el tiempo de ejecución final
end_time = time.time()  # Guardar el tiempo de finalización
execution_time = end_time - start_time  # Calcular el tiempo total de ejecución

# Mostrar el tiempo de ejecución
print(f"\n🕒 Tiempo de ejecución: {execution_time:.4f} segundos")
#sonido cuando termine
import winsound
frequency = 1500  #Hertz
duration = 100  # ms
#winsound.Beep(frequency, duration)