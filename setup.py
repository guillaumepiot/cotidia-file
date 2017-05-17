from setuptools import find_packages, setup


setup(
    name="cotidia-file",
    description="File management and API for the Cotidia ecosystem.",
    version="1.0",
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://code.cotidia.com/cotidia/file/",
    packages=find_packages(),
    package_dir={'file': 'file'},
    package_data={
        'cotidia.file': []
    },
    namespace_packages=['cotidia'],
    include_package_data=True,
    install_requires=[
        'django>=1.10',
        'djangorestframework>=3.5',
        'django-appconf>=1.0',
        'reportlab>=3.4',
        'python-magic>=0.4'
    ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
)
