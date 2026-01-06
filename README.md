# Start date- 02/01/26.
# AI Home Designer – End-to-End DevOps Project

AI Home Designer is a Flask-based web application with user authentication. This project demonstrates an **end-to-end DevOps workflow**, covering application development, containerization, CI/CD automation, and deployment on Kubernetes.

The main goal of this project is to gain **hands-on experience with real-world DevOps tools and practices**.

---

## 🛠️ Tech Stack

* **Application**: Python, Flask
* **Database**: SQLite
* **Version Control**: Git & GitHub
* **CI/CD**: Jenkins
* **Containerization**: Docker
* **Container Registry**: Docker Hub
* **Orchestration**: Kubernetes
* **Cloud**: AWS (EC2, LoadBalancer)

---

## 🏗️ Architecture Flow

1. Developer pushes code to GitHub
2. Jenkins triggers CI pipeline
3. Jenkins builds Docker image
4. Docker image is pushed to Docker Hub
5. Kubernetes pulls image from Docker Hub
6. Application is deployed using Kubernetes Deployment
7. Service (LoadBalancer) exposes the application publicly

---

## 🚀 Features

* User Registration & Login
* Secure routing with Flask
* Dockerized application
* Automated CI pipeline using Jenkins
* Kubernetes Deployment & Service
* Public access using LoadBalancer

---

## 🐳 Docker

### Build Image

```bash
docker build -t <docker-username>/ai-home-designer:latest .
```

### Run Container

```bash
docker run -d -p 5000:5000 <docker-username>/ai-home-designer:latest
```

---

## ⚙️ CI/CD with Jenkins

* Jenkins pulls code from GitHub
* Builds Docker image
* Pushes image to Docker Hub
* Ensures automated and repeatable builds

---

## ☸️ Kubernetes Deployment

### Apply Deployment and Service

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### Verify

```bash
kubectl get pods
kubectl get svc
```

---

## 🌐 Access Application

* Application is exposed using **Kubernetes LoadBalancer**
* Accessed via external IP provided by the cloud provider

---

## 📚 Learning Outcomes

* Hands-on CI/CD pipeline creation
* Docker image creation and optimization
* Kubernetes deployment and service exposure
* Debugging real-world issues in cloud environments
* Understanding DevOps best practices

---

## 👨‍💻 Author

**Om Prakash Swain**
Aspiring DevOps Engineer
GitHub: [https://github.com/ops86199](https://github.com/ops86199)

---
Based on our exact service name, port, and labels, we create a correct Ingress YAML for AWS Load Balancer Controller (ALB).
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ai-home-designer-ingress
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80}]'
spec:
  ingressClassName: alb
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: service
            port:
              number: 80
for seeing end point :-- kubectl get ingress
---------------------------
Then we install Halm ::-- curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
check version;;- helm version
✅ STEP 2: Now Install AWS Load Balancer Controller (Correct Way)
2.1 Associate OIDC (if not done already)
eksctl utils associate-iam-oidc-provider \
--region ap-south-1 \
--cluster my-cluster \
--approve
2.2 Create IAM Policy
curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
aws iam create-policy \
--policy-name AWSLoadBalancerControllerIAMPolicy \
--policy-document file://iam_policy.json
2.3 Create IAM Service Account (MOST IMPORTANT)
eksctl create iamserviceaccount \
--cluster=my-cluster \
--namespace=kube-system \
--name=aws-load-balancer-controller \
--attach-policy-arn=arn:aws:iam::<YOUR_ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
--approve
2.4 Install Controller Using Helm
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
-n kube-system \
--set clusterName=my-cluster \
--set serviceAccount.create=false \
--set serviceAccount.name=aws-load-balancer-controller
✅ STEP 3: Verify Controller Is Running
kubectl get pods -n kube-system | grep aws-load-balancer
✅ STEP 4: Check Ingress Again
kubectl get ingress


## ⭐ Conclusion

This project reflects my practical DevOps skills and readiness to work on real-world DevOps tasks. Feedback and suggestions are welcome!

