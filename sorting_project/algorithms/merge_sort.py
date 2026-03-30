"""
Merge Sort — O(n log n)

Ideia: divide o vetor ao meio recursivamente até chegar em sublistas
de 1 elemento (já ordenadas por definição), depois as mescla de volta
em ordem. Estratégia clássica de divisão e conquista.

Complexidade:
  - Melhor caso:  O(n log n)
  - Caso médio:   O(n log n)
  - Pior caso:    O(n log n)  — sempre divide igualmente
  - Espaço:       O(n)        — cria sublistas auxiliares
"""


def merge_sort(data: list[int]) -> list[int]:
    arr = data[:]          # cópia para não modificar o original
    _merge_sort(arr, 0, len(arr) - 1)
    return arr


def _merge_sort(arr: list[int], left: int, right: int) -> None:
    if left >= right:
        return

    mid = (left + right) // 2
    _merge_sort(arr, left, mid)
    _merge_sort(arr, mid + 1, right)
    _merge(arr, left, mid, right)


def _merge(arr: list[int], left: int, mid: int, right: int) -> None:
    left_part = arr[left : mid + 1]
    right_part = arr[mid + 1 : right + 1]

    i = j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1

    # copia os elementos restantes
    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1