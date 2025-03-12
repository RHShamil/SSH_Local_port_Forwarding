# SSH_Local_Port_Forwarding

## 📌 **Project Overview**
This project sets up a secure SSH local port forwarding to enable access to a MySQL server hosted in a private subnet through a bastion host in AWS. The infrastructure is created using **Pulumi**.

### **Architecture Overview**
- **Bastion Host**:
  - Launched in a **public subnet**.
  - Acts as a secure entry point for SSH connections.

- **MySQL Server**:
  - Hosted in a **private subnet**.
  - Cannot be accessed directly from the internet.
  - Configured with a **NAT Gateway** for outbound traffic.

### **Flow Summary**  
1. A network engineer connects to the bastion host using SSH.  
2. SSH local port forwarding is established.  
3. Traffic from the engineer's local machine (port `3306`) is securely forwarded to the MySQL server's port `3306` through the bastion host.  

---

## 🔎 **What is SSH Tunnel Port Forwarding?**
SSH port forwarding (also called SSH tunneling) creates an encrypted tunnel between a local machine and a remote server over the SSH protocol. It allows you to securely forward traffic from a local port to a remote service through an intermediate server.

---

## 🔎 **What is Local Port Forwarding?**
Local port forwarding allows forwarding a port from your local machine to a remote server through an SSH connection.  
- In this project:
  - Local machine’s **port 3306** is forwarded to the MySQL server’s **port 3306**.
  - Traffic flows through the bastion host, creating a secure connection between the local machine and the private MySQL server.

