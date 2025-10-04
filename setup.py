from setuptools import setup, find_packages

setup(
    name="rimp-telemetry",
    version="0.1.0",
    description="Real-time telemetry system for RIMP",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "python-dateutil>=2.8.0",
    ],
    python_requires=">=3.8",
)
