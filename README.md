# Smart Retail Inventory Management & Automated Reorder Alert System

A Python-based automation project that simulates inventory monitoring for retail stores and supermarkets. The system automatically analyzes inventory data, identifies low-stock products, classifies inventory priority, and generates professional restocking reports.

This project demonstrates practical Python programming concepts such as CSV file handling, dictionaries, loops, conditional statements, exception handling, automation, and report generation.

---

# Project Overview

Retail stores manage hundreds of products every day, making manual inventory tracking inefficient and prone to errors.

This application automates the inventory monitoring process by reading product data from a CSV file, validating inventory records, detecting products below their reorder threshold, calculating reorder quantities, and generating a detailed inventory report for store managers.

---

# Objectives

* Automate inventory stock monitoring
* Reduce manual inventory verification
* Identify products requiring immediate replenishment
* Generate professional inventory reports
* Demonstrate real-world Python automation

---

# Features

## Inventory Processing

* Read inventory data from CSV files
* Store inventory using Python dictionaries
* Validate product records
* Skip invalid or malformed rows safely

## Stock Analysis

* Compare current stock with reorder threshold
* Detect products requiring restocking
* Identify critical inventory shortages

## Priority Classification

Products are categorized as:

* Healthy
* Low Stock
* Critical Stock

## Reorder Suggestions

Automatically calculates the recommended reorder quantity required to restore healthy inventory levels.

## Budget Estimation

Calculates the estimated procurement cost for products requiring replenishment.

## Report Generation

* Console inventory report
* CSV restock report
* Email-style inventory summary

## Error Handling

Handles:

* Missing values
* Invalid numeric data
* Empty fields
* Malformed CSV records

without interrupting the execution of the program.

---

# Technology Stack

| Category             | Technology                     |
| -------------------- | ------------------------------ |
| Language             | Python 3                       |
| File Processing      | CSV Module                     |
| Data Structure       | Lists & Dictionaries           |
| Programming Concepts | Loops, Functions, Conditionals |
| Error Handling       | Try-Except                     |
| Output               | CSV Reports                    |

---

# Repository Structure

```text
inventory-reorder-alert/
│
├── inventory_system.py
├── daily_inventory.csv
├── restock_report.csv
└── README.md
```

---

# Workflow

```text
Daily Inventory CSV
        │
        ▼
Read Inventory Data
        │
        ▼
Validate Records
        │
        ▼
Analyze Stock Levels
        │
        ▼
Classify Product Priority
        │
        ▼
Calculate Reorder Quantity
        │
        ▼
Generate Inventory Report
        │
        ▼
Export Restock Report
```

---

# Sample Output

```text
=========================================================
SMART RETAIL INVENTORY DASHBOARD
=========================================================

Products Scanned      : 100
Healthy Products      : 72
Low Stock             : 18
Critical Products     : 10

Inventory Health      : 72%

Report Generated Successfully

=========================================================
```

---

# Python Concepts Demonstrated

* CSV File Handling
* Dictionaries
* Lists
* Loops
* Conditional Statements
* Functions
* Exception Handling
* Data Validation
* Automation
* Report Generation

---

# Future Enhancements

* MySQL or PostgreSQL database integration
* Barcode and QR code scanning
* Supplier management
* Automatic purchase order generation
* Email notifications using SMTP
* SMS alerts
* Streamlit dashboard
* REST API using FastAPI or Flask
* Machine Learning demand forecasting
* Multi-store inventory management

---

# Getting Started

## Clone the Repository

```bash
git clone https://github.com/Ragunathapoorva/inventory-reorder-alert.git
```

## Navigate to the Project Directory

```bash
cd inventory-reorder-alert
```

## Run the Application

```bash
python inventory_system.py
```

---

# Input File

The application reads inventory data from:

```text
daily_inventory.csv
```

---

# Output File

The application generates:

```text
restock_report.csv
```

which contains all products requiring replenishment, along with their priority level and suggested reorder quantity.

---

# Learning Outcomes

This project demonstrates practical knowledge of:

* Python programming
* File handling
* Business automation
* Inventory analysis
* Data validation
* Report generation
* Problem-solving using real-world retail scenarios

---

# Author

**Ragunath Suresh**

GitHub: https://github.com/Ragunathapoorva

---

# License

This project is developed for educational, learning, and portfolio purposes.

