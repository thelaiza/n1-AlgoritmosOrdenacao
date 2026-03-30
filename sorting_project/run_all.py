"""
run_all.py — Parte 4: Instrumentação com OpenTelemetry.

Executa todos os algoritmos de ordenação e registra:

MÉTRICAS (enviadas ao Prometheus via endpoint /metrics na porta 8000):
  - sorting_duration_seconds  → tempo total de execução por algoritmo/tamanho
  - sorting_input_size        → tamanho da entrada (n)

LOGS (stdout estruturado):
  - Início e fim de cada execução
  - Algoritmo selecionado
  - Erros ou comportamentos anômalos

Uso:
    pip install opentelemetry-sdk opentelemetry-exporter-prometheus prometheus-client
    python run_all.py
"""

import time
import logging
import os

# --- OpenTelemetry ---
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

# --- Projeto ---
from generate_data import load_datasets, OUTPUT_FILE, generate_datasets, save_datasets, SIZES
from algorithms import ALGORITHMS

# ─────────────────────────────────────────
# Logging estruturado
# ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("sorting")

# ─────────────────────────────────────────
# OpenTelemetry — configuração do MeterProvider
# ─────────────────────────────────────────
prometheus_reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[prometheus_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("sorting.algorithms")

# Instrumentos
duration_histogram = meter.create_histogram(
    name="sorting_duration_seconds",
    description="Tempo de execução de cada algoritmo de ordenação",
    unit="s",
)

input_size_gauge = meter.create_gauge(
    name="sorting_input_size",
    description="Tamanho da entrada (n) usada na execução",
)


def run_experiments(datasets: dict) -> list[dict]:
    results = []

    for algo_name, algo_fn in ALGORITHMS.items():
        print(f"\n{'─' * 45}")
        print(f"  Algoritmo: {algo_name}")
        print(f"{'─' * 45}")

        for size_str, original_data in datasets.items():
            n = int(size_str)
            labels = {"algorithm": algo_name, "input_size": str(n)}

            # LOG: início da execução
            log.info(f"INÍCIO | algoritmo={algo_name} | n={n}")

            # Cópia limpa — garante que nenhum algoritmo recebe dados já ordenados
            data = original_data[:]

            # Registra o tamanho da entrada como métrica
            input_size_gauge.set(n, labels)

            try:
                start = time.perf_counter()
                sorted_data = algo_fn(data)
                elapsed = time.perf_counter() - start

                # Registra duração no histograma do OpenTelemetry
                duration_histogram.record(elapsed, labels)

                # Validação de corretude
                is_sorted = all(
                    sorted_data[i] <= sorted_data[i + 1]
                    for i in range(len(sorted_data) - 1)
                )

                if not is_sorted:
                    log.error(f"ERRO DE ORDENAÇÃO | algoritmo={algo_name} | n={n}")

                result = {
                    "algorithm": algo_name,
                    "n": n,
                    "time_seconds": round(elapsed, 6),
                    "time_ms": round(elapsed * 1000, 3),
                    "sorted_correctly": is_sorted,
                }
                results.append(result)

                status = "✓" if is_sorted else "✗ ERRO"
                print(f"  n={n:>6} | {elapsed * 1000:>10.3f} ms | {status}")

                # LOG: fim da execução
                log.info(f"FIM    | algoritmo={algo_name} | n={n} | tempo={elapsed*1000:.3f}ms | correto={is_sorted}")

            except ValueError as e:
                log.warning(f"IGNORADO | algoritmo={algo_name} | n={n} | motivo={e}")
                print(f"  n={n:>6} |   IGNORADO (n muito grande para O(n²))")

            except Exception as e:
                log.error(f"EXCEÇÃO | algoritmo={algo_name} | n={n} | erro={e}")
                raise

    return results


def print_summary(results: list[dict]) -> None:
    sizes = sorted(set(r["n"] for r in results))
    algos = list(ALGORITHMS.keys())

    print(f"\n\n{'═' * 60}")
    print("  RESUMO — Tempo de execução (ms)")
    print(f"{'═' * 60}")

    header = f"{'Algoritmo':<15}" + "".join(f"{n:>12}" for n in sizes)
    print(header)
    print("─" * len(header))

    for algo in algos:
        row = f"{algo:<15}"
        for n in sizes:
            match = next((r for r in results if r["algorithm"] == algo and r["n"] == n), None)
            if match:
                row += f"{match['time_ms']:>10.1f}ms"
            else:
                row += f"{'—':>12}"
        print(row)

    print(f"{'═' * 60}\n")


if __name__ == "__main__":
    # Sobe o servidor HTTP para o Prometheus coletar as métricas
    start_http_server(8000)
    log.info("Servidor de métricas iniciado em http://localhost:8000/metrics")

    # Garante que os dados existem
    if not os.path.exists(OUTPUT_FILE):
        log.info("Arquivo de dados não encontrado. Gerando agora...")
        save_datasets(generate_datasets(SIZES), OUTPUT_FILE)

    log.info("Carregando datasets...")
    datasets = load_datasets(OUTPUT_FILE)
    log.info(f"Datasets carregados: {list(datasets.keys())}")

    results = run_experiments(datasets)
    print_summary(results)

    # Mantém o processo vivo para o Prometheus continuar coletando
    print("✓ Métricas disponíveis em http://localhost:8000/metrics")
    print("  Pressione Ctrl+C para encerrar.\n")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        log.info("Encerrado pelo usuário.")