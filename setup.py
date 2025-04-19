from setuptools import setup, find_packages

setup(
    name="cmd-aegnt",
    version="0.1.0",
    packages=find_packages(),
    scripts=["ae"],
    install_requires=[],  # No external dependencies for basic functionality
    author="AI Assistant",
    author_email="example@example.com",
    description="A command-line AI aegnt for system tasks",
    keywords="ai, command-line, automation, system-settings",
    url="https://github.com/yourusername/cmd-aegnt",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
