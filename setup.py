from setuptools import find_packages, setup


version = '0.0.1'


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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ],
    description='An asynchronous IRC framework/library based upon asyncio',
    include_package_data=True,
    install_requires=[
        'cchardet>=0.3.5,<2',
    ],
    name='framewirc',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/meshy/framewirc/',
    version=version,
)
