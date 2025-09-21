from setuptools import setup, find_packages

setup(
    name="hamada-tool-v2",
    version="2.0.0",
    description="AI-Powered Procurement Automation System for AEDCO",
    author="AEDCO Development Team",
    author_email="info@aedco.com.eg",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "plotly>=5.15.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "python-docx>=0.8.11",
        "openpyxl>=3.1.0",
        "PyPDF2>=3.0.1",
        "pillow>=10.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "huggingface-hub>=0.16.0",
        "transformers>=4.30.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "hamada-tool=main:main",
        ],
    },
)
