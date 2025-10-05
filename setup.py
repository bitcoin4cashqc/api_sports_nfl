from setuptools import setup, find_packages

setup(
    name="api-sports-nfl",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
    ],
    author="SoliditySam",
    description="NFL API client for API-Sports",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
