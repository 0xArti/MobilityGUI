import sys
import setuptools


def get_excludes():
    excludes = ["*test"]
    if sys.platform != "win32":
        excludes.append("service")
    return excludes


def get_requirements():
    requirements = [
        "PySimpleGUI"
    ]
    if sys.platform == "win32":
        requirements.append("pywin32")
    return requirements


setuptools.setup(
    name="mobility-gui",
    version="0.1",
    author="Art",
    description="Cross-platform service for displaying mobility exercises on screen",
    packages=setuptools.find_packages(exclude=get_excludes()),
    python_requires=">=3.6",
    install_requires=get_requirements(),
    entry_points = {
        'console_scripts': [
            'mobility=mobility.exercises_provider:main'
        ],
    }
)