from setuptools import setup, find_packages

setup(
    name="sainsmart_relay",
    version="0.1.0",
    description="Control SainSmart relays using FTDI bit-bang mode",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/sainsmart-relay",
    packages=find_packages(),
    install_requires=[
        "pylibftdi",  # List any other dependencies that are required here
    ],
    entry_points={
        "console_scripts": [
            "relay-server=sainsmart_relay.server:main",
            "relay=sainsmart_relay.client:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",  # Assuming you choose MIT License
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
