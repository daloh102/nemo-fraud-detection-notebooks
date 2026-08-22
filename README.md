# 📓 Notebooks & Execution Pipeline

Dieser Ordner bündelt alle interaktiven Jupyter-Notebooks für die vollständige End-to-End-Pipeline des Fraud-Detection-Projekts. Für einen reibungslosen Ablauf wird empfohlen, die Notebooks in der chronologischen Reihenfolge auszuführen.

---

## 🧭 Pipeline-Struktur & Ablauf

| Schritt | Notebook | Beschreibung & Kernaufgaben |
| :--- | :--- | :--- |
| **01** | `01_Data_Curation.ipynb` | Bereinigung, Vorverarbeitung und Formatierung der Rohdaten in das benötigte SFT-Format. |
| **02** | `02_FineTuning.ipynb` | Durchführung des PEFT/LoRA-Trainings über das Megatron/NeMo-Framework auf den GPUs. |
| **03** | `03_Evaluation_and_Wandb.ipynb` | Checkpoint-Handling, echte Modell-Inferenz auf Validierungsdaten sowie W&B-Logging. |
| **04** | `04_Monitoring_Dashboard.ipynb` | Infrastruktur-Management zur Prüfung von Prometheus, Grafana & DCGM-GPU-Exporter. |

---

> **💡 Wichtiger Hinweis für die Ausführung:** 
> Stelle vor dem Start der Inferenz- und Monitoring-Notebooks sicher, dass sich deine Container im selben Docker-Netzwerk befinden und die entsprechenden Ports erreichbar sind.