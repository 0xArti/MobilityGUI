import setuptools

setuptools.setup(
    name="mobility-gui",
    version="0.1",
    author="Art",
    description="Cross-platform service for displaying mobility exercises on screen",
    packages=setuptools.find_packages(exclude=("*test")),
    python_requires=">=3.6",
    install_requires=[
        "pywin32",
        "PySimpleGUI",
    ]
)