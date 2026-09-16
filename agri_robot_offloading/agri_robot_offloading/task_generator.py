import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


class TaskGenerator(Node):

    def __init__(self):
        super().__init__('task_generator')

        self.publisher = self.create_publisher(
            String,
            '/agri_tasks',
            10
        )

        self.timer = self.create_timer(
            5.0,
            self.generate_task
        )

        self.task_number = 1

        self.get_logger().info(
            'Agricultural Task Generator Started'
        )

    def generate_task(self):

        # Every 3rd task is designed to require cloud offloading
        if self.task_number % 3 == 0:

            task_type = 'FIELD_DATA_PROCESSING'
            task_size = 'HIGH'
            cpu_load = 85
            network = 'AVAILABLE'

        else:

            task_type = 'SOIL_ANALYSIS'
            task_size = 'LOW'
            cpu_load = 50
            network = 'AVAILABLE'

        task = {
            'robot_id': 'AGRI_ROBOT_01',
            'task_id': f'TASK_{self.task_number:03d}',
            'task_type': task_type,
            'task_size': task_size,
            'cpu_load': cpu_load,
            'network': network
        }

        message = String()
        message.data = json.dumps(task)

        self.publisher.publish(message)

        self.get_logger().info(
            f'Task Generated: {message.data}'
        )

        self.task_number += 1


def main(args=None):

    rclpy.init(args=args)

    node = TaskGenerator()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
