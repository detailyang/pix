# @Author: BingWu Yang <detailyang>
# @Date:   2016-09-20T20:27:36+08:00
# @Email:  detailyang@gmail.com
# @Last modified by:   detailyang
# @Last modified time: 2016-09-20T15:23:48+08:00
# @License: The MIT License (MIT)


from setuptools import setup, find_packages


setup(
    name='pix-css',
    version='0.1.1',
    keywords=('pixel css art'),
    description='transform picture to pixel cs',
    license='MIT License',
    install_requires=[
        'Jinja2==2.8',
        'MarkupSafe==0.23',
        'Pillow==3.3.1',
    ],
    entry_points={
        'console_scripts': [
            'pix=pix:main',
        ],
    },
    author='detailyang',
    author_email='detailyang@gmail.com',

    packages=find_packages(),
    platforms='any',
)
