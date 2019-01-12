import os

from setuptools import find_packages, setup


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        # Only keep the last directory of the path
        path = path.replace(directory, directory.split("/")[-1])
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths


template_files = package_files("cotidia/file/templates")

setup(
    name="cotidia-file",
    description="File management and API for the Cotidia ecosystem.",
    version="1.0",
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://code.cotidia.com/cotidia/file/",
    packages=find_packages(),
    package_dir={"file": "file"},
    package_data={"cotidia.file": template_files},
    namespace_packages=["cotidia"],
    include_package_data=True,
    install_requires=["django-storages==1.7.*", "reportlab>=3.4", "python-magic>=0.4"],
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
)
