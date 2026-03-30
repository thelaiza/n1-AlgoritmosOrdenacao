"""
Bubble Sort — O(n²)

Ideia: percorre o vetor repetidamente, comparando pares adjacentes
e trocando-os se estiverem na ordem errada. A cada passagem, o maior
elemento "borbulha" para o final. Para quando não há mais trocas.

Complexidade:
  - Melhor caso:  O(n)   — vetor já ordenado (flag de troca)
  - Caso médio:   O(n²)
  - Pior caso:    O(n²)  — vetor invertido
  - Espaço:       O(1)   — in-place
"""

MAX_SAFE_SIZE = 10_000  # BubbleSort é inviável acima disso


def bubble_sort(data: list[int]) -> list[int]:
    if len(data) > MAX_SAFE_SIZE:
        raise ValueError(
            f"BubbleSort abortado: n={len(data)} excede o limite seguro de {MAX_SAFE_SIZE}. "
            f"Algoritmo O(n²) inviável para entradas grandes."
        )

    arr = data[:]          # cópia para não modificar o original
    n = len(arr)

    for i in range(n):
        swapped = False    # otimização: para cedo se já estiver ordenado

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:    # nenhuma troca = vetor já ordenado
            break

    return arr