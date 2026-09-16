from setuptools import find_packages, setup

package_name = 'agri_robot_offloading'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='a209',
    maintainer_email='a209@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'sensor_node = agri_robot_offloading.sensor_node:main',
        'task_generator = agri_robot_offloading.task_generator:main',
        'offloading_node = agri_robot_offloading.offloading_node:main',
        'mqtt_bridge = agri_robot_offloading.mqtt_bridge:main',
    ],
},
)
