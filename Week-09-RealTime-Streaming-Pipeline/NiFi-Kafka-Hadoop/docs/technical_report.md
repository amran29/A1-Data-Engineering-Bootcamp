# Technical Documentation & Pipeline Report

## 1. Pipeline Explanation
The pipeline is designed to handle high-throughput streaming data using a decoupled microservices architecture. It begins with a Python-based generator simulating e-commerce transactions, which writes CSV chunks continuously. Apache NiFi acts as the primary ingestion and routing engine, pulling files, chunking them, and handling schema transformations. Apache Kafka serves as the central messaging backbone to ensure data durability, while a secondary NiFi flow consumes these messages and persists them into HDFS.

## 2. Data Flow Explanation
* **Generation**: The Python script creates records with intentional inconsistencies (missing values, varying timestamps) simulating real-world messiness.
* **Ingestion**: NiFi's `GetFile` processor ingests the CSV files.
* **Chunking**: The `SplitText` processor guarantees no single FlowFile exceeds the 64 KB threshold, optimizing memory usage.
* **Transformation**: `ConvertRecord` parses the messy CSV using a predefined schema and serializes the clean output into JSON.
* **Messaging**: JSON payloads are published to the Kafka topic `ecommerce-transactions` using `PublishKafka_2_6`.
* **Storage**: `ConsumeKafka_2_6` retrieves the records, and `PutHDFS` writes them to the Hadoop cluster.

## 3. Transformation Logic
The transformation phase converts raw CSV structures into strictly formatted JSON documents.
* **Input**: Raw CSV (`transaction_id`, `customer_id`, `amount`, `timestamp`).
* **Process**: A CSVReader reads the incoming FlowFile. A JSONRecordSetWriter outputs the structured data.
* **Validation**: Records failing to match the expected data types or schema constraints are automatically routed to a `failure` relationship for auditing.

## 4. Error Handling Approach
Robust error handling mechanisms are integrated throughout the NiFi canvas:
* **Back Pressure**: Object and size thresholds are configured on critical queues to prevent OutOfMemory errors during sudden data spikes.
* **Dead Letter Queues (DLQ)**: Processors utilizing `failure` relationships route invalid data to a `LogAttribute` processor for inspection rather than dropping the data.
* **Retry Logic**: Network-dependent processors (`PutHDFS`, `PublishKafka`) are configured with Yield Durations and Penalization times to automatically retry transient connection issues.

## 5. Partitioning Strategy
To optimize future querying and data lifecycle management, HDFS storage relies on a dynamic, time-based partitioning strategy.
* NiFi Expression Language extracts the current processing time.
* Data is written to the HDFS path: `/data/year=${now():format('yyyy')}/month=${now():format('MM')}/day=${now():format('dd')}/`.

## 6. Challenges Faced During Implementation
Several complex infrastructure challenges were encountered and successfully resolved:
* **Docker DNS & Kafka Advertised Listeners**: NiFi initially failed to resolve the Kafka broker due to `localhost` routing inside containers. This was resolved by configuring the internal network listener port `29092` and utilizing the container name `kafka`.
* **HDFS Network Binding**: `Connection Refused` exceptions occurred because the Hadoop NameNode was bound to `127.0.0.1`. The `core-site.xml` was modified to bind to `0.0.0.0:9000`, enabling cross-container communication.
* **HDFS Write Permissions**: The NiFi user initially lacked write access to the root Hadoop volume. Executing `chmod 777 /data` within the HDFS container granted the necessary execution and write privileges.