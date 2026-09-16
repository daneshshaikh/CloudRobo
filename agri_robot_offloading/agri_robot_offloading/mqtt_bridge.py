import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import paho.mqtt.client as mqtt


class MQTTBridge(Node):

    def __init__(self):
        super().__init__('mqtt_bridge')

        self.subscription = self.create_subscription(
            String,
            '/offloading_decision',
            self.process_decision,
            10
        )

        self.mqtt_client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id='agri_robot_cloud_bridge'
        )

        self.mqtt_client.connect(
            'localhost',
            1883,
            60
        )

        self.mqtt_client.loop_start()

        self.get_logger().info(
            'ROS 2 to MQTT Cloud Bridge Started'
        )

        self.get_logger().info(
            'Connected to MQTT Broker'
        )

    def process_decision(self, msg):

        task = json.loads(msg.data)

        if task['processing_location'] == 'CLOUD':

            mqtt_message = json.dumps(task)

            self.mqtt_client.publish(
                'agri/robot/cloud_tasks',
                mqtt_message
            )

            self.get_logger().info(
                f"CLOUD TASK SENT: {task['task_id']}"
            )

            self.get_logger().info(
                f"MQTT Message: {mqtt_message}"
            )

        else:

            self.get_logger().info(
                f"LOCAL TASK: {task['task_id']}"
            )


def main(args=None):

    rclpy.init(args=args)

    node = MQTTBridge()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.mqtt_client.loop_stop()
    node.mqtt_client.disconnect()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
