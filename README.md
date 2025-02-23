# 📊 Restaurant Sales Dashboard

## Overview
This project is a **live interactive dashboard** for tracking restaurant sales, customer trends, and ratings using **Streamlit** and **SQL Server**. The goal is to provide real-time insights into restaurant performance by visualizing sales data dynamically.

## 🚀 Features
- 📌 **Interactive Dashboard**: Built using **Streamlit** for real-time data visualization.
- 🛢 **SQL Server Integration**: Data is stored and managed in **Azure SQL Server**.
- 📈 **Sales & Ratings Analysis**: Insights from customer orders, locations, and feedback.
- 📂 **CSV Data Import**: Allows bulk import of restaurant data using **Azure Data Studio**.
- 🐳 **Dockerized Database**: SQL Server runs inside a **Docker container** for easy setup.

---

## 🏗 Setup Instructions

### **1️⃣ Run SQL Server using Docker**
First, ensure Docker is installed on your system. Then, run the command given below to start an **SQL Server instance**. For more details about this docker image, click [here](https://hub.docker.com/r/microsoft/mssql-server).

```bash
docker run -e 'ACCEPT_EULA=y' -e 'SA_PASSWORD=yourStrong(!)Password' -p 1433:1433 --name azuresqledge -d mcr.microsoft.com/mssql/server:latest
```

### 2️⃣ Install Azure Data Studio  
If you haven’t already, [download and install Azure Data Studio](https://learn.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio).

### 3️⃣ Install Necessary Extensions  
In **Azure Data Studio**, install the following extensions:  
- **SQL Server Import** (to import CSV or TXT files to create Tables in the database)  
- **New Database** (to create a new database)  

### 4️⃣ Create a Database  
1. Open **Azure Data Studio**.  
2. Connect to **SQL Server** using:  
   - **Server**: `localhost,1433`  
   - **Username**: `SA`  
   - **Password**: `yourStrong(!)Password`  
3. Right-click on **Databases** → Click **New Database** → Name it **"Restaurant"**.  

### 5️⃣ Import Data into the Database  
Import the following **CSV files** into the **Restaurant** database:  
- `item.csv`  
- `customers.csv`  
- `addresses.csv`  
- `ratings.csv`  

Use the **SQL Server Import** extension for easy import.  

### 6️⃣ Install UnixODBC (For macOS)  
If you're on macOS, install the **ODBC driver**:  
```bash
brew install unixODBC
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/unixodbc/lib:$DYLD_LIBRARY_PATH
```
### 7️⃣ Install Microsoft ODBC Driver 17

Run the following commands to install Microsoft ODBC Driver 17:
```sh
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_NO_AUTO_UPDATE=1 brew install msodbcsql17
```
✅ Verify the Installation

Run the following command to check if the driver is installed correctly:
```sh
odbcinst -q -d -n "ODBC Driver 17 for SQL Server"
```
