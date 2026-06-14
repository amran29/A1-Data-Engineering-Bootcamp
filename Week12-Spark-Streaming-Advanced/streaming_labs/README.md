# Week 12: Apache Spark Structured Streaming Assignments

This repository contains the practical assignments for **Week 12** of the **A1 Data Engineering Bootcamp**. The focus of these labs is on building scalable, fault-tolerant, and real-time streaming data pipelines using **Apache Spark Structured Streaming (v3.1.2)** inside a Dockerized Hadoop environment.

---

## 📁 Repository Structure

```text
streaming_labs/
├── lab2_temperature/
│   ├── spark_streaming_json.ipynb
│   └── json_input_dir/
│
└── lab5_flights/
    ├── spark_streaming_csv.ipynb
    └── csv_input_dir/
```

| Directory          | Description                                              |
| ------------------ | -------------------------------------------------------- |
| `lab2_temperature` | Advanced Windowing & Watermarking Lab using JSON streams |
| `lab5_flights`     | CSV Aggregation & Streaming Analytics Lab                |
| `json_input_dir`   | Directory monitored for incoming JSON micro-batches      |
| `csv_input_dir`    | Directory monitored for incoming CSV flight batches      |

---

# 🌡️ Lab 2: Real-Time Temperature Monitoring (JSON Stream)

## Project Overview

This application consumes a continuous stream of temperature data from globally distributed weather sensors. The pipeline processes incoming events in real-time, performs time-based aggregations, handles late-arriving records, and persists analytical outputs to multiple destinations.

### Key Requirements & Implementation

#### 📥 Stream Source

* Monitors JSON files continuously using Spark Structured Streaming.
* Uses `readStream` with `multiLine=True` to ingest JSON array batches.

#### ⏱️ Windowing

* Implements a **15-minute tumbling window**.
* Aggregates temperature readings based on event time.

#### 🕒 Watermarking (Late Data Handling)

* Applies a **10-minute watermark** on the `event_timestamp` column.
* Records arriving later than the watermark threshold are automatically discarded.

#### 📤 Output Mode

* Uses **Append Mode**.
* Finalized windows are written only after Spark determines that no more late events are expected.

#### 💾 Dual Sink Architecture

* Writes processed data simultaneously to two separate destinations.
* Uses **Parquet** format for efficient storage and analytics.
* Demonstrates fault tolerance and multi-target streaming outputs.

---

# ✈️ Lab 5: Flight Aggregation Pipeline (CSV Stream)

## Project Overview

A real-time streaming analytics pipeline designed to process continuous flight records stored in CSV format. The application continuously computes cumulative traffic metrics between countries and updates aggregated results as new batches arrive.

### Key Requirements & Implementation

#### 📥 Stream Source

* Directory-based streaming ingestion.
* Uses explicitly defined schemas for consistent processing of CSV files.

#### ⚙️ Business Logic

Groups incoming records by:

* `ORIGIN_COUNTRY_NAME`
* `DEST_COUNTRY_NAME`

and calculates cumulative traffic using:

```python
sum("count")
```

#### 🔄 Output Mode

Uses **Update Mode**, allowing Spark to:

* Recompute only modified aggregations.
* Display only changed records in each micro-batch.
* Improve processing efficiency.

#### 🖥️ Sink Configuration

The pipeline outputs results to:

1. **Console Sink**

   * Real-time monitoring of streaming updates.

2. **Memory Sink**

   * In-memory table for debugging and validation.
   * Enables SQL-based inspection inside Jupyter Notebook.

---

# 🛠️ Technology Stack

| Component               | Technology                              |
| ----------------------- | --------------------------------------- |
| Streaming Engine        | Apache Spark Structured Streaming 3.1.2 |
| Programming Language    | Python (PySpark)                        |
| Execution Environment   | itversity/itvdelab Docker Container     |
| Development Environment | Visual Studio Code (VS Code)            |
| Notebook Interface      | Jupyter Notebook                        |
| Storage Protocol        | Local File System Volumes (`file://`)   |

---

# 🚀 Running the Pipelines

## 1. Start the Docker Environment

```bash
docker compose up -d
```

---

## 2. Connect VS Code to Jupyter

Open VS Code and connect your notebook to the running Jupyter server:

```text
http://localhost:8888/?token=<your-token>
```

---

## 3. Execute the Streaming Notebook

Run all streaming cells in the notebook.

Once started, the Spark application will enter a continuous listening state:

```text
[*]
```

---

## 4. Simulate Real-Time Data

Copy data batches into the corresponding input directories:

### Temperature Stream

```text
json_input_dir/
├── batch1.json
├── batch2.json
└── ...
```

### Flight Stream

```text
csv_input_dir/
├── flight_data.csv
├── flight_data_2.csv
└── ...
```

Spark will automatically:

* Detect new files
* Process incoming batches
* Update aggregations
* Persist outputs
* Display streaming results in real-time

---

# ✅ Learning Objectives

By completing these labs, you will gain hands-on experience with:

* Spark Structured Streaming fundamentals
* File-based streaming ingestion
* Event-time windowing
* Watermarking and late data management
* Stateful aggregations
* Append and Update output modes
* Multiple streaming sinks
* Real-time analytics pipelines
* Docker-based Spark environments
* Streaming application debugging and monitoring

---

## Author

**Amran Al-gaafari – Week 12 Labs**
