import pytest
from general import leer_archivo_txt, prim, tsp_ruta_mas_corta, flujo_maximo

def test_leer_archivo_txt(tmp_path):
    archivo = tmp_path / "grafo.txt"
    contenido = """3
0 1 2
1 0 3
2 3 0
0 1 0
1 0 1
0 1 0"""
    archivo.write_text(contenido)

    n, matriz1, matriz2 = leer_archivo_txt(str(archivo))

    assert n == 3
    assert matriz1 == [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
    assert matriz2 == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]

def test_prim():
    matriz = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ]
    resultado = prim(matriz)
    assert resultado == [(0, 1), (0, 2)]

def test_tsp_ruta_mas_corta():
    matriz = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ]
    ruta, distancia = tsp_ruta_mas_corta(matriz)
    assert ruta == [0, 1, 2] or ruta == [0, 2, 1]
    assert distancia == 6

def test_flujo_maximo():
    capacidad = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]
    ]
    assert flujo_maximo(capacidad) == 23

if __name__ == "__main__":
    pytest.main()
