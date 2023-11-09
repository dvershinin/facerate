from setuptools import setup, find_packages

setup(
    name='facerate',
    version='0.0.1',  # Adjust as necessary
    author='Danila Vershinin',
    author_email='your-email@example.com',
    description='A package for scoring facial beauty.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your-username/facerate',  # Replace with your repository URL
    project_urls={
        "Bug Tracker": "https://github.com/your-username/facerate/issues"
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        'httpx',
        'beautifulsoup4',
        'lxml',  # if you're using lxml as the parser for BeautifulSoup
        'Pillow'  # compressing images prior to upload to avoid 500 errors
    ],
    extras_require={
        'tests': [
            'pytest',
            'pytest-asyncio',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='facial, beauty, score, rating, facerate',  # Add some relevant keywords
    entry_points={
        'console_scripts': [
            'facerate=facerate.cli:main',  # Adjust the entry point to your CLI, if you have one
        ],
    },
)
