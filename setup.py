from setuptools import setup


setup(
    name='pivotal-sorter',
    author='James Kelly',
    version='1.0',
    py_modules=['sorter'],
    install_requires=[
        'click',
        'requests',
    ],
    entry_points='''
    [console_scripts]
    pivotal-sorter=sorter:pivotal_sorter
    ''',
)
