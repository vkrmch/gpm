from setuptools import setup, find_packages

setup(
    name='gpm',
    version='0.1.1',
    author='Vikram Chauhan',
    author_email='hello@vikramchauhan.com',
    packages=find_packages(),
    license='MIT',
    url='https://github.com/vkrmch/gpm',
    description='gpm provides wrapper functions that can be used for starting any python project',
    package_data={
        'gpm': ['cfg/*.json']
    },
    data_files=[
        ('.', ['LICENSE', 'README.md'])
    ]
)
