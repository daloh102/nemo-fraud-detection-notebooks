FROM nvcr.io/nvidia/nemo:24.09

# Extra packages for guardrails, experiment tracking, evaluation and visualization.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /data
