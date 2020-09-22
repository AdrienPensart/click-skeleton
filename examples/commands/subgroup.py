'''A subgroup example'''
from click_skeleton import AdvancedGroup
from examples.cli import main_cli


@main_cli.group('subgroup', short_help='A sub group', cls=AdvancedGroup, aliases=['subgroup_alias'])
def subgroup() -> None:
    '''I am a subgroup!'''
    print('hello from subgroup!')


@subgroup.command(short_help='A sub command')
def subcommand() -> None:
    '''I am a subcommand!'''
    print('hello from subcommand!')
