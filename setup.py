from setuptools import setup, find_packages


__version__ = '0.1'


url = 'https://github.com/skarrok/django-liqpay'


setup(
    name='django-liqpay',
    version=__version__,
    description='Django liqpay app',
    long_description=open('README.md').read(),
    author='skarrok',
    author_email='skarrok.h@gmail.com',
    url=url,
    # download_url='%s/archive/%s.tar.gz' % (url, __version__),
    download_url='%s/zipball/master',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    install_requires=[
        'liqpay-python@git+https://github.com/liqpay/sdk-python@f3a81847f2b518c3936461880e0451eb02f33b25#egg=liqpay-python-2.0',
    ],
)
