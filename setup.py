from setuptools import setup, find_packages

setup(
    name = 'file-update',
    version = '1.0',
    description = 'Updates multiple copies of a file\
        residing in different directories',
    author = 'Faris Al-Bloshi',
    author_email = 'faris_ddx@hotmail.com',
    url = 'https://github.com/falblocatshi/file-update',
    packages=find_packages
    (
        where = "src",
    ),
    package_dir=
    {
        "":"src"
    },
    entry_points=
    {
        'console_scripts':
        [
            'file-update = file_update.__main__:start',
            'fud = file_update.__main__:start'
        ],
    },
    python_requires='>=3.6',    
)
