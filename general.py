import itertools
from collections import deque
from typing import List, Tuple, Deque

"""
Diego Roque de Rosas A01657709
Jesús Jionary Gutiérrez Moreno A01664857
Bruno Contreras Silva A01657766
"""

def leer_archivo_txt(ruta_archivo: str) -> Tuple[int, List[List[int]], List[List[int]]]:
    """
    Lee un archivo de texto con formato específico para obtener dos matrices de adyacencia.

    Args:
        ruta_archivo (str): Ruta al archivo de texto.

    Returns:
        Tuple[int, List[List[int]], List[List[int]]]: Tamaño de las matrices y las dos matrices de adyacencia.

    Raises:
        FileNotFoundError: Si el archivo no se encuentra.
        ValueError: Si el archivo tiene errores en el formato o en los datos.
    """
    try:
        with open(ruta_archivo, 'r') as archivo:
            lineas = [linea.strip() for linea in archivo.readlines() if linea.strip()]
            if not lineas:
                raise ValueError("El archivo está vacío.")

            n = int(lineas[0])
            if n <= 0:
                raise ValueError("El tamaño de la matriz debe ser mayor que 0.")

            esperado = 1 + 2 * n
            if len(lineas) != esperado:
                raise ValueError(f"El archivo tiene un número incorrecto de líneas. Esperado: {esperado}, encontrado: {len(lineas)}")

            matriz1 = []
            for i in range(n):
                fila = lineas[i + 1].split()
                if len(fila) != n:
                    raise ValueError(f"La fila {i + 1} de la matriz 1 no tiene {n} elementos.")
                matriz1.append(list(map(int, fila)))

            matriz2 = []
            for i in range(n):
                fila = lineas[i + n + 1].split()
                if len(fila) != n:
                    raise ValueError(f"La fila {i + 1} de la matriz 2 no tiene {n} elementos.")
                matriz2.append(list(map(int, fila)))

        return n, matriz1, matriz2
    except FileNotFoundError:
        raise FileNotFoundError(f"No se pudo encontrar el archivo en la ruta: {ruta_archivo}")
    except ValueError as e:
        raise ValueError(f"Error en el formato del archivo: {e}")

def prim(matriz_adyacencia: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Calcula el Árbol de Expansión Mínima (MST) utilizando el algoritmo de Prim.

    Args:
        matriz_adyacencia (List[List[int]]): Matriz de adyacencia del grafo.

    Returns:
        List[Tuple[int, int]]: Lista de aristas en el MST.

    Raises:
        ValueError: Si el grafo no es conexo.
    """
    num_nodos = len(matriz_adyacencia)
    visitado = [False] * num_nodos
    infinit = float('inf')
    weight = [infinit] * num_nodos
    origen = [-1] * num_nodos
    weight[0] = 0
    mst = []

    for _ in range(num_nodos):
        nodo_actual = -1
        menor_peso = infinit
        for nodo in range(num_nodos):
            if not visitado[nodo] and weight[nodo] < menor_peso:
                menor_peso = weight[nodo]
                nodo_actual = nodo

        if nodo_actual == -1:
            raise ValueError("El grafo no es conexo.")

        visitado[nodo_actual] = True
        if origen[nodo_actual] != -1:
            mst.append((origen[nodo_actual], nodo_actual))

        for nodo_destino in range(num_nodos):
            peso_actual = matriz_adyacencia[nodo_actual][nodo_destino]
            if peso_actual != 0 and not visitado[nodo_destino] and peso_actual < weight[nodo_destino]:
                weight[nodo_destino] = peso_actual
                origen[nodo_destino] = nodo_actual

    return mst

def tsp_ruta_mas_corta(matriz_adyacencia: List[List[int]]) -> Tuple[List[int], int]:
    """
    Resuelve el Problema del Viajante (TSP) para encontrar la ruta más corta.

    Args:
        matriz_adyacencia (List[List[int]]): Matriz de adyacencia del grafo.

    Returns:
        Tuple[List[int], int]: La mejor ruta y su distancia total.
    """
    n = len(matriz_adyacencia)
    ciudades = range(n)
    mejor_distancia = float('inf')
    mejor_ruta = []

    for permutacion in itertools.permutations(ciudades):
        distancia_actual = 0
        for i in range(n):
            origen = permutacion[i]
            destino = permutacion[(i + 1) % n]
            distancia_actual += matriz_adyacencia[origen][destino]
            if distancia_actual >= mejor_distancia:
                break
        else:
            mejor_distancia = distancia_actual
            mejor_ruta = list(permutacion)

    return mejor_ruta, mejor_distancia

def busqueda_camino(origen: int, destino: int, ruta_previa: List[int], matriz_capacidad: List[List[int]], lista_vecinos: List[List[int]]) -> int:
    """
    Realiza una búsqueda en amplitud (BFS) para encontrar un camino aumentante en un grafo de flujo.

    Args:
        origen (int): Nodo de origen.
        destino (int): Nodo de destino.
        ruta_previa (List[int]): Lista para almacenar el camino encontrado.
        matriz_capacidad (List[List[int]]): Matriz de capacidades del grafo.
        lista_vecinos (List[List[int]]): Lista de adyacencias del grafo.

    Returns:
        int: Capacidad del flujo encontrado en el camino. Retorna 0 si no hay camino.
    """
    num_nodos = len(ruta_previa)
    ruta_previa[:] = [-1] * num_nodos
    ruta_previa[origen] = -2
    cola_nodos: Deque[Tuple[int, int]] = deque([(origen, float('inf'))])

    while cola_nodos:
        nodo_actual, flujo_disponible = cola_nodos.popleft()

        for vecino in lista_vecinos[nodo_actual]:
            if ruta_previa[vecino] == -1 and matriz_capacidad[nodo_actual][vecino] > 0:
                ruta_previa[vecino] = nodo_actual
                capacidad_usable = min(flujo_disponible, matriz_capacidad[nodo_actual][vecino])

                if vecino == destino:
                    return capacidad_usable

                cola_nodos.append((vecino, capacidad_usable))

    return 0

def flujo_maximo(capacidad: List[List[int]]) -> int:
    """
    Calcula el flujo máximo en un grafo usando el algoritmo de Edmonds-Karp.

    Args:
        capacidad (List[List[int]]): Matriz de capacidades del grafo.

    Returns:
        int: El flujo máximo del grafo.
    """
    n = len(capacidad)
    origen = 0
    destino = n - 1
    flujo_total = 0
    padre = [-1] * n

    def construir_adyacencia(capacidad: List[List[int]]) -> List[List[int]]:
        return [
            [j for j in range(len(capacidad)) if capacidad[i][j] > 0]
            for i in range(len(capacidad))
        ]

    adyacencia = construir_adyacencia(capacidad)

    while True:
        flujo = busqueda_camino(origen, destino, padre, capacidad, adyacencia)
        if flujo == 0:
            break

        flujo_total += flujo
        actual = destino
        while actual != origen:
            anterior = padre[actual]
            capacidad[anterior][actual] -= flujo
            capacidad[actual][anterior] += flujo
            actual = anterior

    return flujo_total

if __name__ == "__main__":
    try:
        n, matriz_distancias, matriz_capacidades = leer_archivo_txt("grafo.txt")

        # Ejecutar Prim para encontrar el MST
        try:
            mst = prim(matriz_distancias)
            print("Forma óptima de cablear con fibra óptica:")
            print(", ".join(f"({a}, {b})" for a, b in mst))
        except ValueError as e:
            print(f"Error en el algoritmo de Prim: {e}")

        # Resolver el TSP
        ruta, distancia_total = tsp_ruta_mas_corta(matriz_distancias)
        print("\nRuta más corta para el repartidor:")
        print(", ".join(f"({ruta[i]}, {ruta[(i + 1) % n]})" for i in range(n)))

        # Calcular el flujo máximo
        flujo = flujo_maximo(matriz_capacidades)
        print("\nFlujo máximo de información:")
        print(flujo)

    except FileNotFoundError:
        print("Error: No se encontró el archivo 'grafo.txt'. Por favor, verifica la ruta y vuelve a intentarlo.")
    except ValueError as e:
        print(f"Error en el formato del archivo: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
