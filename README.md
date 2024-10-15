# Enable RBAC in Minikube

```bash
minikube start --extra-config=apiserver.Authorization.Mode=RBAC
```

# Ingress Controller - Enable Ingress Addon

```bash
minikube addons enable ingress
```

# Network Policies - Deny Service A from Accessing Service B
