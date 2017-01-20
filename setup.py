from setuptools import setup, find_packages


def requirements() -> list:
    with open('requirements/prod.txt') as f:
        return [l.strip() for l in f.readlines()]


setup(
    name='httpmeter',
    version='0.1.0',
    description='Hackable HTTP benchmarking tool.',
    long_description=open('README.rst').read(),
    url='https://github.com/povilasb/httpmeter',
    author='Povilas Balciunas',
    author_email='balciunas90@gmail.com',
    license='MIT',
    packages=find_packages(exclude=('tests')),
    entry_points={
        'console_scripts': ['httpmeter = httpmeter.__main__:main']
    },
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
    ],
    install_requires=requirements(),
)
