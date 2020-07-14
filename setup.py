from setuptools import setup

setup(
    name='database_loader',
    version='1.0.34',
    packages=['database_loader', 'database_loader.core', 'database_loader.core.databases'],
    entry_points={
        "console_scripts": [
            "database_loader = database_loader.__main__:main",
        ]
    },
    url='https://github.com/marinellirubens/database_loader',
    author='Rubens Marinelli Ferreira',
    author_email='marinelli.rubens@gmail.com',
    description='Loader for oracle database',
    install_requires=[
        'pandas',
        'SQLAlchemy', 'numpy'
    ]
)
