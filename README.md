# N1 — Algoritmos de Ordenação

Trabalho da disciplina de Algoritmos e Estruturas de Dados.
Implementação, instrumentação e análise experimental de algoritmos de ordenação.

**Estudante:** Laíza Carolina da Silva  
**Professor:** Diogo Winck

---

## O que o projeto faz

Implementa três algoritmos de ordenação em Python, executa todos sobre os mesmos dados, mede o tempo de execução com OpenTelemetry e envia as métricas para o Prometheus, que são visualizadas no Grafana.

---

## Algoritmos implementados

| Algoritmo | Complexidade | Arquivo |
|---|---|---|
| Bubble Sort | O(n²) | `algorithms/bubble_sort.py` |
| Merge Sort | O(n log n) | `algorithms/merge_sort.py` |
| Quick Sort | O(n log n) | `algorithms/quick_sort.py` |

---

## Estrutura do projeto

```
sorting_project/
├── generate_data.py        # Gera os dados e salva em JSON
├── run_all.py              # Executa os algoritmos com instrumentação
├── docker-compose.yml      # Sobe Prometheus e Grafana
├── prometheus.yml          # Configuração do Prometheus
├── data/
│   └── datasets.json       # Dados gerados (1k, 5k, 10k, 50k elementos)
└── algorithms/
    ├── __init__.py
    ├── bubble_sort.py
    ├── merge_sort.py
    └── quick_sort.py
```

---

## Pré-requisitos

- Python 3.10 ou superior
- Docker Desktop

---

## Como rodar

**1. Instalar as dependências Python:**

```bash
pip install opentelemetry-sdk opentelemetry-exporter-prometheus prometheus-client
```

**2. Gerar os dados (apenas na primeira vez):**

```bash
cd sorting_project
python generate_data.py
```

**3. Subir o Prometheus e o Grafana (com o Docker Desktop aberto):**

```bash
docker-compose up
```

**4. Em outro terminal, rodar os algoritmos:**

```bash
python run_all.py
```

O script executa todos os algoritmos, exibe os tempos no terminal e mantém o servidor de métricas ativo em `http://localhost:8000/metrics`.

---

## Observabilidade

Com tudo rodando, acesse:

- **Prometheus:** `http://localhost:9090` — para consultar as métricas coletadas
- **Grafana:** `http://localhost:3000` — para visualizar o dashboard (login: admin / admin)

No Grafana, a query usada no dashboard foi:

```
sorting_duration_seconds_sum * 1000
```

---

## Resultados obtidos

Tempos de execução medidos (em ms):

| Algoritmo | n=1.000 | n=5.000 | n=10.000 | n=50.000 |
|---|---|---|---|---|
| Bubble Sort | 59,6 ms | 1.286,6 ms | 4.974,1 ms | ignorado |
| Merge Sort | 2,1 ms | 15,8 ms | 28,7 ms | 167,3 ms |
| Quick Sort | 2,1 ms | 6,0 ms | 15,2 ms | 83,0 ms |

O Bubble Sort foi bloqueado para n=50.000 por ser inviável — o tempo projetado ultrapassaria horas de execução.

---

## Decisões de projeto

**Por que os dados são gerados uma única vez e salvos em arquivo?**  
Para garantir que todos os algoritmos ordenem exatamente os mesmos números. Se cada algoritmo gerasse seus próprios dados, ou recebesse dados já parcialmente ordenados por outro, a comparação seria inválida.

**Por que Grafana + Prometheus?**  
É a stack de observabilidade mais usada na indústria e tem integração nativa com OpenTelemetry. A configuração via Docker Compose torna o ambiente reproduzível.

**Por que o Quick Sort foi mais rápido que o Merge Sort, sendo ambos O(n log n)?**  
O Quick Sort opera in-place, sem alocar memória auxiliar, o que reduz o número de acessos à memória e aproveita melhor o cache da CPU. O Big-O não captura essas constantes ocultas.
