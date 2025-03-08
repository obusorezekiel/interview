# **Kubernetes & Data Processing**

This project is a **Kubernetes-based application** where you deploy a **web application** and a **PostgreSQL database**, troubleshoot issues, and enhance the system with an additional service that processes CSV files from a **MinIO blob storage** into PostgreSQL.

## **Project Overview**
The project consists of:
1. **Web Application** - A containerized web service that connects to a PostgreSQL database.
2. **PostgreSQL Database** - A stateful database deployed in Kubernetes.
3. **MinIO Blob Storage** - Stores CSV files that will be processed and inserted into the PostgreSQL database.
4. **CSV Processor** - A Python script that watches MinIO, processes new CSV files, and stores the data in PostgreSQL.

---

## **Deployment**
### **Prerequisites**
Ensure you have the following installed:
- Kubernetes cluster (I used EKS)
- `kubectl` CLI
- Docker
- MinIO or an S3-compatible storage
- PostgreSQL client for verification

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

3. **Verify the status of your pods**:
   ```sh
   kubectl get pods
   ```

Once the application is running, Adjust the security groups on the Node to accept traffic from the NodePort(30007):

Now, you can access the application at:
```
http://<Nodes-IP>:30007
```

---

## **Enhancements - CSV Processing Application**
### **Service Overview**
A separate service runs a Python script that:
- Watches a **MinIO bucket** for new CSV files.
- Reads and parses the CSV data.
- Inserts the data into the PostgreSQL database.

---



### **Dockerizing the CSV Processor**
#### **Dockerfile**
```dockerfile
# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Set environment variables to prevent interactive prompts during package installation
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

#### **Build and Run**
1. **Build the Docker image**:
   ```sh
   docker build -t myrepo/csv-processor:latest .
   ```

2. **Push the image to Dockerhub**:
   ```sh
   docker push -t myrepo/csv-processor:latest
   ```

3. **Attach the image to the Kubernetes Manifest and deploy the csv-processor application**


```sh
kubectl apply -f processor-app.yaml
```
---

## **Testing**
### Create Minio on Kubernetes
Write a Kubernetes Manifest to deploy minio on Kubernetes using the following manifest

###
```sh
kubectl apply -f new-application-minio.yaml
```

Check your browser to confirm minio is running

![Minio](png/annotely_image%20(5).png)


### **Upload a test CSV to MinIO**

On the Minio dashboard, create a bucket and upload a test csv file.
The CSV Processor application running on Kubernetes will detect the file, process it, and insert data into PostgreSQL.

### **Check the PostgreSQL database**
```sh
kubectl exec -it <postgres-pod> -- psql -U postgres -d postgresdb
```
Then run:
```sql
SELECT * FROM actuals;
```
You should see the inserted data.

![Database](png/annotely_image%20(6).png)


Refresh the Webapp, and the new data will be inserted.

![Final Output](png/annotely_image%20(4).png)

---

## **Cleaning Up**
To delete all resources:
```sh
kubectl delete -f webapp-manifest.yaml
docker stop $(docker ps -aq)
```

---

## **Conclusion**
This project showcases **Kubernetes deployment, troubleshooting, and enhancements** with an additional **CSV processing service** using **MinIO, PostgreSQL, and Python**. 🚀