# Base image for per-paper sandbox containers.
# Built once; orchestrator pulls it by name (SANDBOX_BASE_IMAGE env var).
#
# Isolation contract:
#   - --network none applied AFTER pip install phase (orchestrator enforces this)
#   - --cap-drop=ALL --security-opt=no-new-privileges
#   - cgroups: 4 CPU, 8 GB RAM, 10 GB disk
#   - 30-minute wall-clock timeout enforced by orchestrator

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        build-essential \
        curl \
        wget \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Pre-install common ML dependencies to speed up sandbox setup
# (repos that need unusual deps will still install them from their requirements.txt)
RUN pip install --no-cache-dir \
    numpy \
    scipy \
    pandas \
    scikit-learn \
    matplotlib \
    tqdm \
    pyyaml \
    requests

WORKDIR /work
# Paper repo will be cloned/bind-mounted here by the orchestrator

CMD ["bash"]
