from setuptools import setup


name = "pyscfg"
version = "0.1.1"

# get list of requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# get README as long description
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=name,
    version=version,
    author="Christopher Mertens",
    author_email="suppetia@gmx.de",
    description="simple handling of user configuration",
    project_urls={
                    "Source Code": "https://github.com/suppetia/pyscfg"
                 },
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["pyscfg"],
    install_requires=requirements,
    python_requires=">=3.6.0"
)
