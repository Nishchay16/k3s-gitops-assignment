# K3s Distributed Infrastructure & GitOps Challenge

This repository contains a production-grade, GitOps-managed Kubernetes stack deployed on K3s. It demonstrates automated infrastructure provisioning, policy-driven security (OPA), asynchronous messaging (NATS), and persistent storage (Minio CSI).

## High-Level Architecture

The architecture follows a modular "App-of-Apps" pattern managed by Argo CD.

- **Ingress Controller**: Traefik (K3s Default) handles external traffic.
- **GitOps**: Argo CD automates the deployment of all infrastructure and application components.
- **Messaging**: NATS serves as the asynchronous broker.
- **Policy**: OPA Gatekeeper enforces resource limits on all non-system namespaces.
- **Storage**: Minio CSI driver simulates block storage for persistent volumes.

## Quick Start (Bootstrap)

To spin up the cluster and the entire stack, run the bootstrap script:

```bash
chmod +x init.sh
./init.sh
```

The script installs Argo CD and applies the `root-app.yaml`, which recursively triggers the deployment of:

1. `infra/nats` (Messaging)
2. `infra/minio` (Storage)
3. `infra/opa` (Policy)
4. `infra/app-stack` (3-Tier Microservices)

## Communication Matrix

The application stack demonstrates three distinct networking patterns required by the challenge:

| Source | Destination | Protocol | Pattern | Description |
|--------|-------------|----------|---------|-------------|
| UI Service | HTTP Service | NATS (4222) | Asynchronous | Background tasks triggered via NATS broker. |
| UI Service | HTTP Service | ClusterIP (80) | Synchronous | Real-time REST API calls via K8s internal DNS. |
| External User | WS Service | Traefik (80/ws) | External | Persistent WebSocket connections via Ingress. |

## Security & Policy Enforcement

### 1. OPA Gatekeeper

We enforce Resource Limits (CPU/Memory) on all pods.

- **Verification**: Try deploying a pod without limits in a new namespace; Gatekeeper will reject the request.
- **Exemptions**: System namespaces (`kube-system`, `argocd`, `my-app`) are whitelisted to ensure core stability.

### 2. RBAC Restriction

A `developer-role` is defined in `infra/rbac/` which grants `GET/LIST/WATCH` permissions ONLY within the `my-app` namespace, preventing unauthorized access to infrastructure components in `minio-system` or `nats-system`.

## Minio CSI Integration

The cluster uses the Minio Direct-CSI pattern.

- **Implementation**: A standard Minio deployment acts as the storage backend.
- **Driver**: The Minio CSI driver (running as a controller) interfaces with the Kubernetes API to provision volumes dynamically.
- **StorageClass**: `minio-csi-storage` is used by the `sanity-test-pvc` to demonstrate volume binding and persistence.

## Automated Sanity Check (Argo Workflows)

Post-deployment, an Argo Workflow is triggered to verify the integrity of the cluster.

- **Test 1**: Connectivity check to the NATS broker.
- **Test 2**: DNS resolution check for the HTTP Internal Service.
- **Test 3**: (Optional) Volume mount validation.

To manually trigger the workflow:

```bash
argo submit -n argo-workflows infra/workflows/sanity-check.yaml
```

## Repository Structure

```
.
├── init.sh                     # Bootstrap script
├── infra/
│   ├── apps/                   # Argo CD Application manifests (App-of-Apps)
│   ├── nats/                   # NATS Broker manifests
│   ├── minio/                  # Minio Server & CSI Driver manifests
│   ├── opa/                    # Rego policies and Gatekeeper Constraints
│   ├── rbac/                   # Developer Roles & RoleBindings
│   ├── app-stack/              # UI, HTTP, and WS deployments
│   └── workflows/              # Argo Workflow Sanity Checks
└── README.md
```

## Final Steps

1. Create the `init.sh` file with the bootstrap script code.
2. Ensure your `infra/workflows/sanity-check.yaml` is saved.
3. Commit and Push to your repository:

```bash
git add .
git commit -m "Initial K3s GitOps infrastructure setup"
git push origin main
```

---

## Prerequisites

- K3s cluster installed and running
- `kubectl` configured to access your cluster
- `git` for version control
- Argo CD CLI (optional, for manual workflow submissions)
- Argo Workflows CLI (optional, for manual workflow submissions)

## Additional Resources

- [K3s Documentation](https://k3s.io/)
- [Argo CD Documentation](https://argo-cd.readthedocs.io/)
- [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)
- [OPA Gatekeeper Documentation](https://open-policy-agent.org/docs/latest/gatekeeper/)
- [NATS Documentation](https://docs.nats.io/)
- [Minio CSI Documentation](https://min.io/docs/minio/kubernetes/upstream/)

---

**Happy GitOps-ing!**
