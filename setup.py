from setuptools import setup


version = '0.0.1a1'


setup(
    author='Charlie Denton',
    author_email='charlie@meshy.co.uk',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ],
    description='An asynchronous IRC framework/library based upon asyncio',
    include_package_data=True,
    install_requires=[
        'beautifulsoup4>=4.3.2,<4.4',
        'chardet>=2.3.0,<2.4',
    ],
    name='asyncio-irc',
    packages=['asyncio_irc'],
    url='https://github.com/meshy/asyncio-irc/',
    version=version,
)