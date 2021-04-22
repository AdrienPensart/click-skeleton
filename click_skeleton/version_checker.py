'''Checks if a new version of current program is available on PyPI'''
import logging
import threading
import re
from html.parser import HTMLParser
from typing import Any, Optional, Tuple, List
import click
import requests
import semver  # type: ignore


logger = logging.getLogger(__name__)
DEFAULT_PYPI = 'pypi.org'


class MyParser(HTMLParser):
    '''Parser to extract http links'''
    def __init__(
        self,
        *args: Any,
        output_list: Optional[List[Any]] = None,
        **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.output_list = output_list if output_list is not None else []

    def handle_starttag(
        self,
        tag: str,
        attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        '''We parse only http links'''
        if tag == 'a':
            self.output_list.append(dict(attrs).get('href'))

    def error(self, message: str) -> None:
        '''Print parsing error, implement parser abstract method'''
        logger.error(message)


class VersionCheckerThread(threading.Thread):
    '''Background thread to check version, to start at beginning of CLI'''
    def __init__(self, prog_name: str, current_version: str, domain: str = DEFAULT_PYPI, autostart: bool = True, **kwargs: Any):
        super().__init__(**kwargs)
        self.prog_name = prog_name
        self.new_version_warning: Optional[str] = None
        self.domain = domain
        self.current_version = current_version
        self.url = f'https://{domain}/simple/{prog_name}/'
        if autostart:
            self.start()

    def run(self) -> None:
        '''This threads auto-start by default and store a result you can read at end of program execution'''
        try:
            resp = requests.get(self.url)
            if not resp.ok:
                logger.info(f'{self.prog_name} : unable to fetch {self.url} : {resp.text}')  # pylint: disable=logging-fstring-interpolation
                return

            parser = MyParser()
            parser.feed(resp.text)
            if not parser.output_list:
                logger.info(f'{self.prog_name} : no packages links detected in {resp.text}')  # pylint: disable=logging-fstring-interpolation
                return

            last_link = parser.output_list[-1]
            last_version_matches = re.search(r'(?:(\d+\.[.\d]*\d+))', last_link)
            if not last_version_matches:
                logger.info(f'{self.prog_name} : no version found in string {last_link}')  # pylint: disable=logging-fstring-interpolation
                return

            last_version = last_version_matches.group(1)

            last_version_info = semver.VersionInfo.parse(last_version)
            current_version_info = semver.VersionInfo.parse(self.current_version)
            if current_version_info < last_version_info:
                pip_extra_index_url = ''
                pipx_extra_index_url = ''
                if self.domain != DEFAULT_PYPI:
                    pip_extra_index_url = f'--extra-index-url=https://{self.domain} '
                    pipx_extra_index_url = f'--index-url=https://{self.domain} '
                self.new_version_warning = click.style(
                    f'''
{self.prog_name} : new version {last_version} available (current version: {self.current_version})
upgrade command :
    pip3 install -U {pip_extra_index_url}{self.prog_name}
    pipx upgrade {pipx_extra_index_url}{self.prog_name}''',
                    fg='bright_blue',
                )
        except Exception as error:  # pylint: disable=broad-except
            logger.exception(error)

    def print(self) -> None:
        '''Join thread and print result on stderr'''
        try:
            if not self.is_alive():
                logger.debug('Version checker thread may have exited')
                return
            self.join()
            if self.new_version_warning:
                click.echo(self.new_version_warning, err=True)
            else:
                logger.info(f'{self.prog_name} : no new version available')  # pylint: disable=logging-fstring-interpolation
        except Exception as error:  # pylint: disable=broad-except
            logger.exception(error)
