"""
Quick Sort — O(n log n) médio / O(n²) pior caso

Ideia: escolhe um pivô, particiona o vetor em elementos menores e maiores
que o pivô, depois aplica recursivamente nas duas partes. O pivô é escolhido
como a mediana entre primeiro, meio e último elemento — estratégia que evita
o pior caso em dados já ordenados ou quase ordenados.

Complexidade:
  - Melhor caso:  O(n log n)
  - Caso médio:   O(n log n)
  - Pior caso:    O(n²)       — pivô sempre o menor/maior (mitigado pelo median-of-3)
  - Espaço:       O(log n)    — pilha de recursão
"""


def quick_sort(data: list[int]) -> list[int]:
    arr = data[:]          # cópia para não modificar o original
    _quick_sort(arr, 0, len(arr) - 1)
    return arr


def _quick_sort(arr: list[int], low: int, high: int) -> None:
    if low >= high:
        return

    pivot_idx = _partition(arr, low, high)
    _quick_sort(arr, low, pivot_idx - 1)
    _quick_sort(arr, pivot_idx + 1, high)


def _median_of_three(arr: list[int], low: int, high: int) -> int:
    """Retorna o índice da mediana entre primeiro, meio e último elemento."""
    mid = (low + high) // 2
    # ordena os três e usa o do meio como pivô
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    # coloca o pivô na posição high-1 para o particionamento
    arr[mid], arr[high] = arr[high], arr[mid]
    return high


def _partition(arr: list[int], low: int, high: int) -> int:
    pivot_idx = _median_of_three(arr, low, high)
    pivot = arr[pivot_idx]

    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1