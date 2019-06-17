from setuptools import setup, find_packages


setup(
    name="RecordLib",
    version="0.0.1",
    author="Nate Vogel",
    author_email="nvogel@clsphila.org",
    description="Lib for managing Criminal Records dockets..",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
            "Click",
    ],
    entry_points='''
        [console_scripts]
        download_docs=scripts.download_dockets:cli
    ''',
)
