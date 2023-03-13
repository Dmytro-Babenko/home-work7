from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1',
    description='Handle contact dictionary',
    url='https://github.com/Dmytro-Babenko/home-work4',
    author='Dmytro Babenko',
    author_email='dmytro.babenko87@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['contact-bot = console_bot.main:main']}
)