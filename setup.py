from setuptools import setup, find_packages

setup(
    name='financingtrading',
    version='1.0',
    author='Rex Liu',
    author_email='rexwp11458@gmail.com',
    description='This is a sample package',
    license='MIT',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.18.1',
        'wxPython>=4.0.3'
    ],
    entry_points={
        'console_scripts': [
            'ftrading = app.main:start',
            ]
        }
)
