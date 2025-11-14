# Synthetic E-Commerce Data Project (Python & SQLite)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete, self-contained project for generating, ingesting, and querying synthetic e-commerce data. This exercise was completed using the **Cursor IDE** and demonstrates a simple data pipeline using Python and SQLite.

## Overview

This project simulates a basic e-commerce backend by performing three main tasks:

1.  **Data Generation:** Creates 5 mock CSV files (`users`, `products`, `categories`, `orders`, `order_items`) with realistic, related data.
2.  **Database Ingestion:** A Python script (`ingest.py`) reads all 5 CSV files, creates a new SQLite database (`ecommerce.db`), and populates it.
3.  **Data Querying:** A second Python script (`query.py`) connects to the database, performs a complex `JOIN` query, and outputs a report on total customer spending.

## 🚀 How to Use This Project

You can clone this repository and run the scripts to generate the database and query results yourself.

### Prerequisites

* **Python 3.x**
* No external libraries are needed (only built-in `sqlite3` and `csv` modules are used).

### Installation

1.  Clone this repository to your local machine:
    ```bash
    git clone [https://github.com/Sumanthgs0005/cursor-ecommerce-project.git](https://github.com/Sumanthgs0005/cursor-ecommerce-project.git)
    ```
2.  Navigate into the project directory:
    ```bash
    cd cursor-ecommerce-project
    ```

### Running the Scripts

The scripts are meant to be run in order.

**Step 1: Ingest Data and Build the Database**
This script will read all the `.csv` files and generate the `ecommerce.db` file.

```bash
python ingest.py
