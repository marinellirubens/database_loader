from setuptools import setup

setup(
    name='database_loader',
    version='1.0.9',
    packages=['database_loader', 'database_loader.core'],
    url='',
    license='',
    author='rubens.ferreira',
    author_email='rubens.ferreira@lgcns.com',
    description='Loader for oracle database',
    install_requires=[
        'pandas==1.0.5',
        #'cx-Oracle==7.3.0',
        'SQLAlchemy==1.3.18'
    ]
)
