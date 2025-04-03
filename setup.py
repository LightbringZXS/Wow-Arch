from setuptools import setup, find_packages

setup(
    name='wowarch',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'wowarch=wowarch.main:main',
            'wowarch.installhelper=wowarch.installhelper:main',
        ],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
)
