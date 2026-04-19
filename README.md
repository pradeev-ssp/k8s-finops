# Kubernetes FinOps & Right-Sizing Engine 🚀

An automated auditing tool to identify underutilized resources in a Kubernetes cluster and generate cost-saving recommendations.

##  Tech Stack
- **Orchestration:** Kubernetes (Minikube)
- **Monitoring:** Prometheus & Grafana (kube-prometheus-stack)
- **Logic:** Python 3.12 (Requests, OS)
- **Automation:** Kubernetes CronJobs
- **Containerization:** Docker

## 📊 How it Works
1. **Metrics:** Prometheus collects real-time CPU `rate` usage vs. `kube_pod_container_resource_requests`.
2. **Analysis:** A containerized Python engine runs as a weekly **CronJob**.
3. **Reporting:** It calculates the "Waste Gap" and generates an HTML report flagging deployments with >50% waste.
4. **Action:** Provides exact YAML values for developers to right-size their manifests.

## 🚀 Impact
Identified over 99% CPU waste in test deployments, providing a clear path to significant cloud cost reduction.
