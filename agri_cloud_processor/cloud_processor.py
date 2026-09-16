import json
import time
import subprocess
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "agri/robot/cloud_tasks"


def process_task(task):
    print("\n==============================")
    print("CLOUD TASK RECEIVED")
    print("==============================")

    print("Task ID:", task["task_id"])
    print("Robot ID:", task["robot_id"])
    print("Task Type:", task["task_type"])
    print("Task Size:", task["task_size"])
    print("CPU Load:", task["cpu_load"], "%")

    # Simulate cloud processing
    time.sleep(2)

    # Simple agriculture rule
    soil_moisture = task.get("soil_moisture", 50)

    if soil_moisture < 30:
        irrigation_status = "REQUIRED"
    else:
        irrigation_status = "NOT_REQUIRED"

    result = {
        "task_id": task["task_id"],
        "robot_id": task["robot_id"],
        "task_type": task["task_type"],
        "soil_moisture": soil_moisture,
        "irrigation_status": irrigation_status,
        "status": "COMPLETED",
        "processing_location": "CLOUD"
    }

    # Save result temporarily
    with open("cloud_result.json", "w") as file:
        json.dump(result, file, indent=2)

    # Add result to IPFS
    command = ["ipfs", "add", "-Q", "cloud_result.json"]

    try:
        cid = subprocess.check_output(command, text=True).strip()

        print("\nIPFS STORAGE SUCCESS")
        print("CID:", cid)

        result["ipfs_cid"] = cid

        print("\nFINAL RESULT:")
        print(json.dumps(result, indent=2))

    except Exception as e:
        print("IPFS ERROR:", e)


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT Broker")
    client.subscribe(MQTT_TOPIC)
    print("Subscribed to:", MQTT_TOPIC)


def on_message(client, userdata, msg):
    try:
        task = json.loads(msg.payload.decode())
        process_task(task)

    except Exception as e:
        print("Message processing error:", e)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="agri_cloud_processor"
)

client.on_connect = on_connect
client.on_message = on_message

print("Agriculture Cloud Processor Started")
print("Waiting for CLOUD tasks...")

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
