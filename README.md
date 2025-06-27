
# Terraform Copilot Agent – Full Setup (Frontend + Backend + HTTPS + IAP + Terraform)

This project provides a full deployment stack for an LLM-powered Terraform Copilot Agent on GKE with secure HTTPS access protected by Google IAP and Google-managed SSL certificates.

---

## 🧪 Local Development (Optional)

### Start Backend (FastAPI)
```bash
uvicorn copilot_backend.main:app --reload
```

### Start Frontend (Streamlit)
```bash
streamlit run copilot_frontend/app.py
```

---

## 🚀 Docker Build & Push

### Backend
```bash
docker build -f Dockerfile -t gcr.io/your-project/copilot-backend:latest .
docker push gcr.io/your-project/copilot-backend:latest
```

### Frontend
```bash
docker build -f Dockerfile.frontend -t gcr.io/your-project/copilot-frontend:latest .
docker push gcr.io/your-project/copilot-frontend:latest
```

---

## ☸️ Kubernetes Deployment (GKE)

### Step 1: Deploy Backend
```bash
kubectl apply -f k8s/copilot-deployment.yaml
kubectl apply -f k8s/copilot-backend-service.yaml
```

### Step 2: Deploy Frontend
```bash
kubectl apply -f k8s/copilot-frontend.yaml
kubectl apply -f k8s/copilot-frontend-service.yaml
```

---

## 🔐 HTTPS Load Balancer + IAP Setup with Google-managed Cert

### Step 1: Reserve Static IP
```bash
gcloud compute addresses create copilot-static-ip --global
```

### Step 2: Configure Google-managed SSL Certificate
- Edit `iap-https-lb/managed-cert.yaml` and replace `your-domain.com` with your real domain.
- Make sure your domain points to the static IP created above.

### Step 3: Create OAuth Client ID for IAP
- Go to GCP → APIs & Services → Credentials
- Create OAuth Client ID (Web App)
- Copy the Client ID and Secret

### Step 4: Create Secret for OAuth in GKE
```bash
kubectl create secret generic iap-oauth-secret \
  --from-literal=client_id=YOUR_CLIENT_ID \
  --from-literal=client_secret=YOUR_CLIENT_SECRET
```

### Step 5: Apply IAP and HTTPS Resources
```bash
kubectl apply -f iap-https-lb/frontend-neg.yaml
kubectl apply -f iap-https-lb/frontend-service-neg.yaml
kubectl apply -f iap-https-lb/frontendconfig.yaml
kubectl apply -f iap-https-lb/managed-cert.yaml
kubectl apply -f iap-https-lb/ingress.yaml
```

---

## ☁️ Optional: Provision Infra with Terraform

Terraform provisions:
- Global static IP
- IAP OAuth credentials
- GKE secret for IAP access

### Step 1: Set Variables
Update values or pass via CLI:
- `project_id`
- `region` (default: us-central1)
- `domain`
- `brand` (OAuth consent screen brand)

### Step 2: Deploy
```bash
cd terraform
terraform init
terraform apply -var='project_id=your-project' -var='domain=your-domain.com' -var='brand=your-iap-brand'
```

---

## ✅ Final Access

Once deployed and DNS is set:
```
https://your-domain.com/ai-tf
```

Access is protected by Google IAP — only authorized users will be able to log in.

---

## 📁 Structure

```
/copilot_backend/         # FastAPI backend
/copilot_frontend/        # Streamlit frontend
/k8s/                     # Manual Kubernetes deployments
/iap-https-lb/            # IAP + HTTPS LB configs using Google-managed certs
/terraform/               # Infra provisioning (IP, IAP, secret)
/Dockerfile               # Backend
/Dockerfile.frontend      # Frontend
```

---

## 💬 Need Help?

Let me know if you want:
- GitHub Actions CI/CD
- Backend secured via IAP as well
- GCP Cloud DNS for domain
