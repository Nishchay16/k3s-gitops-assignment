#!/bin/bash
# 1. Install k3s (Single node for local, or mention multi-node config)
curl -sfL https://get.k3s.io | sh -

# 2. Install Argo CD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 3. Apply the Root Application (App-of-Apps)
kubectl apply -f infra/apps/root-app.yaml

echo "Infrastructure is bootstrapping via GitOps..."
