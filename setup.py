from setuptools import setup, find_packages

setup(
    name='difoss_pyutil',
    version='0.1.4',
    py_modules=['difoss_pyutil'],
    packages=find_packages(),
    install_requires=[
        'Click',
        'GitPython',
    ],
    license='Apache License Version 2.0',

    url='https://github.com/difosschan/difoss-pyutil',
    author='DifossChan',
    author_mail='difoss@163.com',
    entry_points={
        'console_scripts': {
            "df.cmd = difoss_pyutil.__main__:main"
        },
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
