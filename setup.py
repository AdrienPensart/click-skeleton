# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_skeleton']

package_data = \
{'': ['*']}

install_requires = \
['click-aliases>=1.0.1,<2.0.0',
 'click-completion>=0.5.0,<0.6.0',
 'click-didyoumean>=0.0.3,<0.0.4',
 'click-help-colors>=0.9,<0.10',
 'click-option-group>=0.5.1,<0.6.0',
 'click>=8.0.1,<9.0.0',
 'munch>=2.5.0,<3.0.0',
 'pytest-click>=1.0.2,<2.0.0',
 'pytest>=6.0.1,<7.0.0',
 'requests>=2.24.0,<3.0.0',
 'semver>=2.10.2,<3.0.0',
 'types-requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'click-skeleton',
    'version': '0.15',
    'description': 'Click app skeleton',
    'long_description': None,
    'author': 'Adrien Pensart',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<=3.9',
}


setup(**setup_kwargs)

