from setuptools import find_packages, setup

setup(
    name="mcqgenrator",
    version="0.0.1",
    author="Muhammad Abdullah",
    author_email="aideveloper453@gmail.com",
    install_requires=[
        "openai",
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2",
        "langchain_community",
        "google-generativeai",
        "langchain-google-genai",
        "langchain-groq",
    ],
    packages=find_packages(),
)
