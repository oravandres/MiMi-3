from setuptools import setup, find_packages

setup(
    name="mimi3",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "crewai>=0.2.0",
        "ollama>=0.1.5",
        "SQLAlchemy>=2.0",
        "psycopg2-binary>=2.9",
        "pydantic>=2.0",
        "pydantic-settings>=2.0",
        "typer[all]>=0.9",
        "python-dotenv>=1.0",
    ],
    extras_require={
        "test": ["pytest>=8.2"],
    },
    python_requires=">=3.10",
) 