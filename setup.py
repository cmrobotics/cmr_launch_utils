import os
from setuptools import setup, find_packages
from glob import glob

package_name = 'cmr_launch_utils'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Joao Carlos Espiuca Monteiro',
    maintainer_email='joao.monteiro@cm-robotics.com',
    description='Helper classes to be used with the launch package and some helper launch files',
    license='Coalescent Mobile Robotics',
)
