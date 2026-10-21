# NeMo fraud detection: getting-started notebooks

A hands-on path through the NVIDIA NeMo stack: generate synthetic phone-call transcripts, curate them, fine-tune a model to flag fraud, evaluate it, and watch the GPUs while you do it. Transcripts and training data are German; the notebooks and this README are English.

## Prerequisites

- An NVIDIA GPU with at least 24 GB VRAM (some configs need less, see the table below; Megatron fine-tuning needs more)
- Docker with the NVIDIA Container Toolkit
- An NGC API key ([ngc.nvidia.com](https://ngc.nvidia.com) -> Setup -> Generate API Key)
- A Hugging Face token, only if you use gated weights such as Llama (request access on the model page first)

## Quickstart

```bash
cp .env.example .env    # fill in NGC_API_KEY, and HF_TOKEN if you need it
```

Run `00_Setup_Environment.ipynb` from the host, in a plain Jupyter install or VS Code, to check your drivers and Docker setup, then start the stack:

```bash
docker compose up -d
```

Open a notebook server inside a container:

```bash
docker exec -it nemo-24.09 bash
jupyter notebook --ip=0.0.0.0 --port=8889 --no-browser --allow-root
# or, for the Automodel container:
docker exec -it nemo-fraud-detection-nemo-automodel-1 bash
jupyter notebook --ip=0.0.0.0 --port=8887 --no-browser --allow-root
```

Then run `notebooks/00_setup_and_verification.ipynb` inside the `nemo` container to confirm the GPU, the Docker network, and `.env` are all visible from there.

## Notebook order

| Step | Notebook | Container | Rough time |
|---|---|---|---|
| 0 | `00_Setup_Environment.ipynb` | host | a few minutes |
| 0 | `notebooks/00_setup_and_verification.ipynb` | `nemo` | a few minutes |
| 1 | `notebooks/01_Data_Generation/01_data_generation.ipynb` | `nemo` | hours, for 5000 samples against a local NIM |
| 1 | `notebooks/01_Data_Generation/02_Data_Judgement.ipynb` | `nemo` | minutes |
| 2 | `notebooks/02_Data_Curation/01_data_curation.ipynb` | `nemo` (GPU/Dask) | minutes |
| 3 | one of `notebooks/04_FineTuning/01_Megatron_Finetuning.ipynb`, `02_Automodel_Finetuning.ipynb`, `03_Huggingface_Finetuning.ipynb` | `nemo` or `nemo-automodel` (see each notebook) | 30+ minutes, GPU-bound |
| 4 | the `notebooks/03_Evaluation/*.ipynb` notebooks | matches the fine-tuning notebook used | minutes each |
| 5 | `notebooks/05_Monitoring/01_Prometheus_Grafana.ipynb` | `nemo` | minutes |

Data flows through fixed paths under `$PROJECT_ROOT` (default `/data/nemo-fraud-detection-notebooks`, set in `.env`): generation writes to `notebooks/01_Data_Generation/data/`, curation reads that and writes to `notebooks/02_Data_Curation/data/sft/`, and fine-tuning/evaluation read from there.

## Monitoring

Grafana (`http://<host>:3000`, default login `admin`/`admin`) ships with six dashboards in `Grafana/`. Import one via Dashboards -> New -> Import, uploading the matching JSON:

| File | Covers |
|---|---|
| `00_GPU Health` | DCGM GPU utilization, VRAM, temperature |
| `00_NIM Monitoring` | NIM request rate and latency |
| `01_Data Generation` | Generation throughput and judge scores |
| `02_Data_Curation` | Curator pipeline stage counts |
| `03_Evaluation` | Accuracy/F1 across evaluation runs |
| `04_Finetuning` | Training loss and GPU usage during fine-tuning |

## Ports

| Port | Service |
|---|---|
| 8889 | NeMo container Jupyter |
| 8887 | NeMo Automodel container Jupyter |
| 8800 | NIM (Llama-3.1-8B-Instruct) |
| 9090 | Prometheus |
| 3000 | Grafana |
| 9400 | DCGM exporter (GPU metrics) |
| 8080 | cAdvisor (container metrics) |
| 9100 | node-exporter (host metrics) |

## Repository layout

```text
nemo-fraud-detection-notebooks/
├── Grafana/                 Dashboard exports, imported by hand (see Monitoring above)
├── notebooks/
│   ├── 00_setup_and_verification.ipynb
│   ├── 01_Data_Generation/  Synthetic transcript generation + variance analysis
│   ├── 02_Data_Curation/    Noise injection, cleaning, PII masking, train/val/test split
│   ├── 03_Evaluation/       Baseline, judge, LoRA, MLflow and vLLM evaluation
│   ├── 04_FineTuning/       Megatron, Automodel and Hugging Face fine-tuning
│   └── 05_Monitoring/       Prometheus/Grafana health checks
├── 00_Setup_Environment.ipynb   Host-side hardware/Docker checks, starts the stack
├── Dockerfile                   Extends nvcr.io/nvidia/nemo:24.09
├── docker-compose.yml            NeMo, Automodel, NIM, Prometheus, Grafana, exporters
├── requirements.txt
├── prometheus.yml
└── .env.example
```

Notebook outputs are cleared before every commit, so diffs stay readable; re-run a notebook to see its results again.
