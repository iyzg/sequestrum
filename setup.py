from setuptools import setup

setup(
    name='sequestrum',
    description='Modern Dotfile Manager',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    url='http://github.com/iiPlasma/sequestrum',
    author='Ivy Zhang',
    author_email="ZIvy042003@gmail.com",
    license='MIT',
    packages=['sequestrum'],
    install_requires=[
        'pyyaml == 3.13',
    ],
    entry_points={
    'console_scripts':
    ['sequestrum = sequestrum.sequestrum:main']
    }
)
