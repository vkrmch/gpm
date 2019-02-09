from distutils.core import setup

setup(
    name='gpm',
    version='0.0.3-alpha',
    author='Vikram Chauhan',
    author_email='me@vkrm.ch',
    packages=['gpm'],
    license='MIT',
    url='https://github.com/vikc07/gpm',
    description='gpm is a set of modules that can be used for starting any python project',
    package_data={
        'gpm': ['cfg/*.json']
    }
)
