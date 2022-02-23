'''A subgroup example'''
import rich_click as click  # type: ignore

from click_skeleton import AdvancedGroup


@click.group(short_help='A sub group short help', cls=AdvancedGroup, aliases=['subgroup-alias'])
def cli() -> None:
    '''I am a long subgroup help!'''


@cli.command(short_help='A sub command short help')
def subcommand() -> None:
    '''I am a long subcommand help!'''
    print('hello from subcommand!')
