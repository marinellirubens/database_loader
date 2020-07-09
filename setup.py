from setuptools import setup

setup(
    name='database_loader',
    version='1.0.31',
    packages=['database_loader', 'database_loader.core', 'database_loader.core.databases'],
    entry_points={
        "console_scripts": [
            "database_loader = database_loader.core.loader:main",
        ]
    },
    url='',
    license='',
    author='rubens.ferreira',
    author_email='rubens.ferreira@lgcns.com',
    description='Loader for oracle database',
    install_requires=[
        'pandas',
        #'cx-Oracle==7.3.0',
        'SQLAlchemy'
    ]
)
