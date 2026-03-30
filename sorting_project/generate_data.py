"""
Parte 3 — Geração e padronização dos dados.

Gera os vetores uma única vez e salva em arquivo JSON.
Todos os algoritmos usarão exatamente esses mesmos dados,
garantindo validade experimental na comparação.
"""

import random
import json
import os

# Tamanhos definidos conforme enunciado
SIZES = [1_000, 5_000, 10_000, 50_000]
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "data", "datasets.json")

def generate_datasets(sizes: list[int], seed: int = 42) -> dict:
    """
    Gera um dicionário com vetores de inteiros aleatórios para cada tamanho.

    O seed é fixado para que os dados sejam reproduzíveis:
    se o arquivo for perdido, a mesma chamada recria exatamente os mesmos dados.
    """
    random.seed(seed)
    datasets = {}
    for size in sizes:
        datasets[str(size)] = [random.randint(0, 10 * size) for _ in range(size)]
        print(f"  Gerado: n={size:>6} | min={min(datasets[str(size)])} | max={max(datasets[str(size)])}")
    return datasets


def save_datasets(datasets: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datasets, f)
    size_kb = os.path.getsize(path) / 1024
    print(f"\n  Dados salvos em: {path} ({size_kb:.1f} KB)")


def load_datasets(path: str) -> dict[str, list[int]]:
    """
    Carrega os datasets do arquivo JSON.
    Retorna um dicionário { "1000": [...], "5000": [...], ... }

    IMPORTANTE: sempre use esta função antes de ordenar.
    Nunca passe para um algoritmo dados que já foram ordenados por outro.
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    # Garante que os valores são listas de inteiros (JSON salva tudo como número, mas valida)
    return {k: list(map(int, v)) for k, v in raw.items()}


if __name__ == "__main__":
    print("=== Gerando datasets ===\n")
    datasets = generate_datasets(SIZES)
    save_datasets(datasets, OUTPUT_FILE)
    print("\nVerificando carregamento...")
    loaded = load_datasets(OUTPUT_FILE)
    for size, data in loaded.items():
        print(f"  n={size:>6} | {len(data)} elementos carregados corretamente")
    print("\nPronto. Execute os algoritmos com run_all.py")