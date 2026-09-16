# 🌱 Cloud-Based Task Offloading System for Agricultural Robots

## 📌 Project Overview

This project presents a cloud-based task offloading system for an agricultural robot using **ROS 2, MQTT, Python, IPFS, and a web dashboard**.

The agricultural robot generates sensor data and computational tasks. A rule-based task scheduler decides whether a task should be processed locally on the robot or offloaded to the cloud.

Heavy computational tasks can be sent to the cloud through MQTT. The cloud processor executes the task and stores the generated result on **IPFS (InterPlanetary File System)**. IPFS generates a unique **Content Identifier (CID)** for each stored result.

A web dashboard allows the user to monitor the robot, view task information, and retrieve stored results using the IPFS CID.

---

## 🎯 Objectives

* Collect agricultural sensor data using ROS 2.
* Generate computational tasks from the agricultural robot.
* Decide whether tasks should run locally or in the cloud.
* Offload selected tasks using MQTT.
* Process cloud tasks using a Python cloud processor.
* Store cloud processing results using IPFS.
* Generate a unique CID for every stored result.
* Provide a web dashboard for monitoring and data retrieval.
* Demonstrate cloud task offloading without using AI/ML.

---

## 🏗️ System Architecture

```text
                 AGRICULTURAL ROBOT
                         │
                         ▼
                    ROS 2 Nodes
                         │
             ┌───────────┴───────────┐
             │                       │
       Sensor Node             Task Generator
             │                       │
             │                       ▼
             │                Offloading Node
             │                       │
             │              ┌────────┴────────┐
             │              │                 │
             │           LOCAL             CLOUD
             │                                │
             │                               MQTT
             │                                │
             │                                ▼
             │                       Cloud Processor
             │                                │
             │                                ▼
             │                               IPFS
             │                                │
             │                               CID
             │                                │
             └────────────────┐               │
                              ▼               ▼
                         Web Dashboard ◄──────┘
                              │
                              ▼
                       Retrieve IPFS Data
```

---

## ⚙️ Task Offloading Logic

The system uses a simple rule-based decision mechanism.

A task is sent to the cloud when:

```text
CPU Load >= 70%
AND
Task Size = HIGH
AND
Network = AVAILABLE
```

Otherwise, the task is processed locally.

Example:

```text
CPU Load: 85%
Task Size: HIGH
Network: AVAILABLE

Decision: CLOUD
```

---

## 🧩 Technologies Used

| Technology          | Purpose                                 |
| ------------------- | --------------------------------------- |
| ROS 2 Humble        | Robot communication and task generation |
| Python              | Node and cloud processor development    |
| MQTT                | Communication between robot and cloud   |
| Mosquitto           | MQTT broker                             |
| IPFS / Kubo         | Decentralized result storage            |
| Flask               | Dashboard backend                       |
| HTML/CSS/JavaScript | Dashboard frontend                      |
| Git/GitHub          | Version control and project storage     |
| Ubuntu 22.04        | Development environment                 |
| WSL2                | Linux environment on Windows            |

---

## 📁 Project Structure

```text
AgriCloudProject/
│
├── README.md
├── .gitignore
│
├── agri_robot_offloading/
│   ├── agri_robot_offloading/
│   │   ├── __init__.py
│   │   ├── sensor_node.py
│   │   ├── task_generator.py
│   │   ├── offloading_node.py
│   │   └── mqtt_bridge.py
│   │
│   ├── resource/
│   ├── test/
│   ├── package.xml
│   ├── setup.py
│   └── setup.cfg
│
├── agri_cloud_processor/
│   └── cloud_processor.py
│
└── agri_dashboard/
    ├── app.py
    └── templates/
        └── index.html
```

---

## 🔄 Data Flow

### 1. Sensor Data

The ROS 2 sensor node generates agricultural sensor values such as:

```text
Soil Moisture
Temperature
Humidity
```

The data is published on:

```text
/agri_sensor_data
```

---

### 2. Task Generation

The task generator creates computational tasks for the agricultural robot.

Example:

```json
{
  "robot_id": "AGRI_ROBOT_01",
  "task_id": "TASK_001",
  "task_type": "FIELD_DATA_PROCESSING",
  "task_size": "HIGH",
  "cpu_load": 85,
  "network": "AVAILABLE"
}
```

Tasks are published on:

```text
/agri_tasks
```

---

### 3. Offloading Decision

The offloading node receives the task and applies the rule-based decision.

Possible decisions:

```text
LOCAL
CLOUD
```

The decision is published on:

```text
/offloading_decision
```

---

### 4. MQTT Communication

When the decision is `CLOUD`, the MQTT bridge sends the task to:

```text
agri/robot/cloud_tasks
```

The Mosquitto MQTT broker handles the communication.

---

### 5. Cloud Processing

The cloud processor receives the task and performs the required processing.

For example, a soil moisture rule is applied:

```text
Soil Moisture < 30%
        ↓
IRRIGATION REQUIRED
```

Otherwise:

```text
Soil Moisture >= 30%
        ↓
IRRIGATION NOT REQUIRED
```

---

### 6. IPFS Storage

After processing, the result is stored in IPFS.

Example:

```text
IPFS STORAGE SUCCESS

CID:
Qmxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

The CID uniquely identifies the stored result.

---

### 7. Dashboard

The Flask dashboard provides:

* Robot information
* Field information
* Crop information
* Soil moisture
* Task status
* Processing location
* IPFS CID
* IPFS result retrieval

The user can enter an IPFS CID and retrieve the stored result.

---

## 🚀 Installation and Setup

### Prerequisites

Install or configure:

* Ubuntu 22.04
* ROS 2 Humble
* Python 3
* Mosquitto
* Paho MQTT
* Flask
* IPFS Kubo

---

## ▶️ Running the System

### Terminal 1 — ROS 2 Sensor Node

```bash
source /opt/ros/humble/setup.bash
cd ~/agri_robot_ws
source install/setup.bash
ros2 run agri_robot_offloading sensor_node
```

---

### Terminal 2 — Start IPFS

```bash
ipfs daemon
```

The IPFS API runs locally on:

```text
http://127.0.0.1:5001
```

---

### Terminal 3 — Cloud Processor

```bash
cd ~/AgriCloudProject/agri_cloud_processor
python3 cloud_processor.py
```

Expected:

```text
Agriculture Cloud Processor Started
Waiting for CLOUD tasks...
Connected to MQTT Broker
Subscribed to: agri/robot/cloud_tasks
```

---

### Terminal 4 — Task Generator

```bash
source /opt/ros/humble/setup.bash
cd ~/agri_robot_ws
source install/setup.bash
ros2 run agri_robot_offloading task_generator
```

---

### Terminal 5 — Offloading Node

```bash
source /opt/ros/humble/setup.bash
cd ~/agri_robot_ws
source install/setup.bash
ros2 run agri_robot_offloading offloading_node
```

---

### Terminal 6 — MQTT Bridge

```bash
source /opt/ros/humble/setup.bash
cd ~/agri_robot_ws
source install/setup.bash
ros2 run agri_robot_offloading mqtt_bridge
```

---

### Terminal 7 — Dashboard

```bash
cd ~/AgriCloudProject/agri_dashboard
python3 app.py
```

Open the dashboard in a browser:

```text
http://localhost:5000
```

---

## 📦 IPFS Data Retrieval

To retrieve a result directly using its CID:

```bash
ipfs cat <CID>
```

Example:

```bash
ipfs cat Qmxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

The Flask dashboard also provides a CID-based retrieval endpoint:

```text
/retrieve/<CID>
```

---

## 📊 Example Cloud Result

```json
{
  "task_id": "TASK_183",
  "robot_id": "AGRI_ROBOT_01",
  "task_type": "FIELD_DATA_PROCESSING",
  "soil_moisture": 50,
  "irrigation_status": "NOT_REQUIRED",
  "status": "COMPLETED",
  "processing_location": "CLOUD",
  "ipfs_cid": "Qmxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

---

## 🔐 Security and Data Integrity

IPFS identifies stored content using a CID derived from the content. This allows the system to retrieve the stored result using its content identifier.

The project currently uses a local IPFS node for demonstration and development.

---

## 🌾 Agricultural Application

The system can be used as a basic architecture for agricultural robots that generate computationally intensive tasks.

Possible future applications include:

* Soil monitoring
* Crop field data processing
* Irrigation status analysis
* Environmental monitoring
* Agricultural image processing
* Remote agricultural robot monitoring

---

## 🔮 Future Enhancements

Future versions can include:

* Real hardware sensors
* Camera-based agricultural data collection
* Real cloud deployment
* Multiple agricultural robots
* Persistent task history
* Real-time dashboard updates
* IPFS pinning services
* Robot location tracking
* Improved task scheduling
* Secure MQTT communication

---

## 👨‍💻 Project

**Cloud-Based Task Offloading System for Agricultural Robots using ROS 2 and IPFS**

This project demonstrates the integration of:

```text
Robotics + ROS 2 + Cloud Computing + MQTT + IPFS + Web Dashboard
```

---

## 📜 License

This project is developed for educational and academic purposes.
