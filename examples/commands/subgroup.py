'''A subgroup example'''
import click
from click_skeleton import AdvancedGroup


@click.group('subgroup', short_help='A sub group', cls=AdvancedGroup, aliases=['subgroup_alias'])
def subgroup() -> None:
    '''I am a subgroup!'''
    print('hello from subgroup!')


@subgroup.command(short_help='A sub command')
def subcommand() -> None:
    '''I am a subcommand!'''
    print('hello from subcommand!')
