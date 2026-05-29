# Your Starting Point (Honest Assessment)

You have AWS Solutions Architect certification, real IaC/Terraform/EKS/ECS project experience, Docker & K8s training, and some Python (ML work + Lambda). The gap isn't starting from zero — it's **depth in Python scripting for DevOps/cloud automation** and  **containerization internals beyond "it works"** . That's very closeable.

---

## Python Scripting for Cloud/DevOps — Your Priority #1

Your Python is ML-flavored (scikit-learn, UI). DevOps Python is a different style — it's about  **talking to APIs, parsing files, automating system tasks, and gluing cloud services together** .

### Core Concepts You Need

**1. Working with files and the OS**

```python
import os, pathlib, shutil, subprocess

# Run shell commands from Python (replaces bash scripts)
result = subprocess.run(["kubectl", "get", "pods", "-n", "production"], 
                        capture_output=True, text=True)
print(result.stdout)

# Walk directories, read configs
for path in pathlib.Path(".").rglob("*.yaml"):
    print(path)
```

**2. Parsing YAML and JSON** — critical for K8s manifests and AWS responses

```python
import yaml, json

# Read a K8s manifest
with open("deployment.yaml") as f:
    manifest = yaml.safe_load(f)

print(manifest["spec"]["replicas"])   # navigate the dict

# AWS CLI returns JSON — parse it
import subprocess, json
out = subprocess.run(["aws", "ec2", "describe-instances"], capture_output=True, text=True)
data = json.loads(out.stdout)
instances = data["Reservations"]
```

**3. boto3 — the AWS SDK for Python** (this will be your most used tool)

```python
import boto3

# List all S3 buckets
s3 = boto3.client("s3")
buckets = s3.list_buckets()["Buckets"]
for b in buckets:
    print(b["Name"])

# Start an EC2 instance
ec2 = boto3.client("ec2", region_name="us-east-1")
ec2.start_instances(InstanceIds=["i-0abc123"])

# Invoke a Lambda function
lam = boto3.client("lambda")
response = lam.invoke(FunctionName="my-function", Payload=b'{"key": "value"}')
```

**4. Error handling and retries** — scripts in production must not crash silently

```python
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name):
    client = boto3.client("secretsmanager")
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response["SecretString"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print(f"Secret {secret_name} not found")
        else:
            raise  # re-raise unexpected errors

```

**5. argparse — making scripts usable by teammates**

```python
import argparse

parser = argparse.ArgumentParser(description="Deploy app to EKS")
parser.add_argument("--env", choices=["dev", "staging", "prod"], required=True)
parser.add_argument("--image-tag", required=True)
args = parser.parse_args()

print(f"Deploying to {args.env} with tag {args.image_tag}")
```

### Python Practice Exercises (do these in order)

1. **Write a script** that uses boto3 to list all EC2 instances in your AWS account, filter by a tag (e.g. `Environment=dev`), and print their IDs and states.
2. **Write a script** that reads a `deployment.yaml` K8s manifest, changes the image tag, and writes a new file — simulating a CD pipeline step.
3. **Write a script** that polls an ECS task or EKS pod until it reaches `RUNNING`/`Running` state, with a timeout — you'll do this constantly in pipelines.
4. **Write a Lambda function** in Python that receives an S3 event, logs the bucket/key, and copies the file to another bucket. Deploy it with boto3 from your local machine.
5. **Build a small CLI tool** with argparse that wraps `kubectl` commands — accepts `--namespace` and `--action` (get-pods, describe, logs) and runs them, capturing and pretty-printing output.

---

## Containers — Your Priority #2

You have Docker training and ECS/EKS project experience, but "training only" on Docker suggests you may not be solid on the *why* behind things. Here's what matters.

### The Mental Model That Changes Everything

A container is **not** a VM. It's a process with three Linux kernel features wrapping it:

* **Namespaces** — isolate what the process *sees* (its own filesystem, network, PID list)
* **Cgroups** — limit what the process *uses* (CPU, RAM)
* **Union filesystem (OverlayFS)** — layers that make images efficient

When you write a Dockerfile, you're building those layers.

### Dockerfile — Write These Well

```dockerfile
# BAD — one fat layer, rebuilds everything on any change
FROM python:3.11-slim
COPY . /app
RUN pip install -r /app/requirements.txt
CMD ["python", "/app/main.py"]

# GOOD — dependencies cached separately from code
FROM python:3.11-slim

WORKDIR /app

# Copy ONLY requirements first — Docker caches this layer
# until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy code — only this layer rebuilds on code changes
COPY . .

# Run as non-root (security)
RUN useradd -m appuser
USER appuser

CMD ["python", "main.py"]
```

### Multi-stage builds — critical for AWS deployments

```dockerfile
# Stage 1: build
FROM python:3.11 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: runtime — much smaller image
FROM python:3.11-slim
COPY --from=builder /install /usr/local
COPY app/ /app/
CMD ["python", "/app/main.py"]
```

### Docker Networking and Volumes (you'll debug these constantly)

```bash
# Containers talk to each other by SERVICE NAME in docker-compose
# Not by localhost, not by IP

# Inspect a container's network
docker inspect my-container | grep -A 20 '"Networks"'

# Mount a local directory (for development)
docker run -v $(pwd)/config:/app/config my-image

# Named volume (for databases — survives container restarts)
docker run -v postgres-data:/var/lib/postgresql/data postgres:15
```

### Container Practice Exercises

1. **Containerize a real Python app** : write a FastAPI app with two endpoints, package it in Docker with a proper multi-stage build, run it locally, hit the endpoints.
2. **Docker Compose multi-container** : build a `docker-compose.yml` with your FastAPI app + a PostgreSQL DB + a Redis cache. Make the app connect to both by service name.
3. **Debug a broken container** : deliberately introduce a bug (wrong CMD, missing env var, wrong port). Practice: `docker logs`, `docker exec -it <id> /bin/bash`, `docker inspect`.
4. **Push to ECR** : tag and push your image to Amazon ECR (you have AWS access). Pull it from a different terminal to verify.
5. **Deploy to EKS with your image** : write a `Deployment` and `Service` manifest that pulls your ECR image, set resource `requests` and `limits`, and expose it via a LoadBalancer service.

---

## Quick Reference: How Everything Connects on Your Project

```
Your Python script
    │
    ├─► boto3 → AWS APIs (create infra, trigger pipelines)
    ├─► subprocess → kubectl (manage K8s workloads)
    └─► yaml/json → parse K8s manifests, Terraform outputs

Terraform (IaC)
    └─► provisions EKS cluster, VPC, ECR, IAM roles

Docker
    └─► packages your app → pushed to ECR

Kubernetes (on EKS)
    └─► pulls from ECR, runs containers, manages scaling/health
```
