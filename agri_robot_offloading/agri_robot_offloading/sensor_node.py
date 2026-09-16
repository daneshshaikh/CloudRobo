import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random


class AgriculturalSensorNode(Node):

    def __init__(self):
        super().__init__('agricultural_sensor_node')

        self.publisher = self.create_publisher(
            String,
            '/agri_sensor_data',
            10
        )

        self.timer = self.create_timer(
            2.0,
            self.publish_sensor_data
        )

        self.get_logger().info(
            'Agricultural Robot Sensor Node Started'
        )

    def publish_sensor_data(self):

        soil_moisture = round(random.uniform(20, 80), 2)
        temperature = round(random.uniform(24, 35), 2)
        humidity = round(random.uniform(40, 80), 2)

        message = String()

        message.data = (
            f"robot_id=AGRI_ROBOT_01, "
            f"soil_moisture={soil_moisture}, "
            f"temperature={temperature}, "
            f"humidity={humidity}"
        )

        self.publisher.publish(message)

        self.get_logger().info(
            f"Published: {message.data}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = AgriculturalSensorNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
