import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


class OffloadingNode(Node):

    def __init__(self):
        super().__init__('offloading_node')

        self.subscription = self.create_subscription(
            String,
            '/agri_tasks',
            self.process_task,
            10
        )

        self.publisher = self.create_publisher(
            String,
            '/offloading_decision',
            10
        )

        self.get_logger().info(
            'Task Offloading Decision Node Started'
        )

    def process_task(self, msg):

        task = json.loads(msg.data)

        cpu_load = task['cpu_load']
        task_size = task['task_size']
        network = task['network']

        if (
            cpu_load >= 70
            and task_size == 'HIGH'
            and network == 'AVAILABLE'
        ):
            decision = 'CLOUD'
        else:
            decision = 'LOCAL'

        result = {
            'robot_id': task['robot_id'],
            'task_id': task['task_id'],
            'task_type': task['task_type'],
            'task_size': task_size,
            'cpu_load': cpu_load,
            'network': network,
            'processing_location': decision
        }

        output = String()
        output.data = json.dumps(result)

        self.publisher.publish(output)

        self.get_logger().info(
            f"Task: {task['task_id']} | "
            f"CPU: {cpu_load}% | "
            f"Size: {task_size} | "
            f"Network: {network} | "
            f"Decision: {decision}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = OffloadingNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
