FROM nvcr.io/nvidia/nemo:24.09

# Installation von zusätzlichen Paketen für Guardrails, Tracking, Evaluierung, Visualisierung und Training
RUN pip install --no-cache-dir \
    nemoguardrails \
    wandb \
    protobuf \
    requests \
    mlflow \
    scikit-learn \
    seaborn \
    matplotlib \
    sentence-transformers
    
# Upgrade der übrigen Pakete
RUN pip install --upgrade wandb protobuf mlflow scikit-learn seaborn matplotlib sentence-transformers

# Arbeitsverzeichnis setzen
WORKDIR /data