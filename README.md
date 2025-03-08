# **Kubernetes & Data Processing**

This project deploys a **web application** and a **PostgreSQL database** in **Kubernetes**, troubleshoots issues, and enhances the system with a **CSV processing service** that reads files from **MinIO** and inserts data into **PostgreSQL**.

---

## **Project Overview**
The project consists of:
1. **Web Application** - Connects to PostgreSQL.
2. **PostgreSQL Database** - A stateful database in Kubernetes.
3. **MinIO Blob Storage** - Stores CSV files for processing.
4. **CSV Processor** - Watches MinIO, processes CSV files, and inserts data into PostgreSQL.

---

## **Deployment**
### **Prerequisites**
Ensure you have:
- A **Kubernetes cluster** (EKS, GKE, AKS)
- **kubectl** CLI
- **Docker**
- **MinIO** or an **S3-compatible** storage
- **PostgreSQL** client for verification

---

### **Deploying the Application**
1. **Clone the repository**:
   ```sh
   git clone <your-repository>
   cd <your-repository>
   ```

2. **Apply the Kubernetes manifests**:
   ```sh
   kubectl apply -f webapp-manifest.yaml
   ```

3. **Verify pod status**:
   ```sh
   kubectl get pods
   ```

4. **Update security groups** on the node to allow NodePort traffic (30007).

Now, access the application at:
```
http://<Node-IP>:30007
```

---

## **Enhancements - CSV Processing Application**
### **Service Overview**
The **CSV Processor**:
- Watches **MinIO** for new CSV files.
- Reads and parses CSV data.
- Inserts the data into **PostgreSQL**.

---

### **Dockerizing the CSV Processor**
#### **Dockerfile**
```dockerfile
# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application files
COPY csv_processor.py .
COPY requirements.txt .
COPY .env .  # Copy the .env file

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python3", "csv_processor.py"]
```

#### **Build and Push Image**
1. **Build the Docker image**:
   ```sh
   docker build -t myrepo/csv-processor:latest .
   ```

2. **Push to Docker Hub**:
   ```sh
   docker push myrepo/csv-processor:latest
   ```

3. **Deploy in Kubernetes**:
   ```sh
   kubectl apply -f processor-app.yaml
   ```

---

## **Testing**
### **Deploy MinIO**
Apply the MinIO manifest:
```sh
kubectl apply -f new-application-minio.yaml
```
Check the browser to confirm MinIO is running.

![Minio](png/annotely_image%20(5).png)

### **Upload a Test CSV to MinIO**
- On the **MinIO dashboard**, create a **bucket**.
- Upload a **test CSV file**.
- The **CSV Processor** will detect, process, and insert data into **PostgreSQL**.

### **Verify PostgreSQL Data**
```sh
kubectl exec -it <postgres-pod> -- psql -U postgres -d postgresdb
```
Run:
```sql
SELECT * FROM actuals;
```
You should see the inserted data.

![Database](png/annotely_image%20(6).png)

Refresh the **Web App** to see the new data.

![Final Output](png/annotely_image%20(4).png)

---

## **Cleanup**
To remove all resources:
```sh
kubectl delete -f webapp-manifest.yaml
docker stop $(docker ps -aq)
```

---

## **Conclusion**
This project demonstrates **Kubernetes deployment, troubleshooting, and enhancement** with a **CSV processing service** using **MinIO, PostgreSQL, and Python**. 🚀