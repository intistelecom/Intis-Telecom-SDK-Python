from distutils.core import setup

setup(
    name='intis',
    packages=['intis'],
    version='0.2',
    description='A Python 2/3 client for the Intis',
    author='Ilya Mukhortov',
    author_email='ilya.muhortov@gmail.com',
    url='https://github.com/intistelecom/Intis-Telecom-SDK-Python',
    download_url='https://github.com/intistelecom/Intis-Telecom-SDK-Python/archive/master.zip',
    keywords=['api', 'sms'],
    classifiers=[],
    install_requires=[
        'six>=1.8.0'
    ]
)
