from setuptools import setup, find_packages

setup(
    name='AutoNotater',
    version='0.1.2',
    author='Arsdeep',
    author_email='arsdeepdewangan@example.com',
    description="A Python script processes all the files in a source directory, adds comments to the code using Google's Generative AI model (Gemini), and saves the processed files to a specified destination directory.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Arsdeep/AutoAnnotate',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'google-generativeai',
        'python-dotenv',
        'discord.py',
        'Ipython'
    ],
    entry_points = {
        'console_scripts':[
            "AutoNotater = Annotate:main"
        ]
    }
)