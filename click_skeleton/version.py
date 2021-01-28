'''Preconfigured version command for root AdvancedGroup (skeleton)'''
import click
from click_help_colors import HelpColorsCommand  # type: ignore


@click.command(short_help='Print version', cls=HelpColorsCommand, help_headers_color='yellow', help_options_color='green')  # type: ignore
@click.pass_context
def version_cmd(ctx: click.Context) -> None:
    '''Print version, equivalent to -V and --version'''
    click.echo(f"{click.style(ctx.obj.prog_name, fg='yellow')}, version {click.style(ctx.obj.version, fg='green')}", color=ctx.color)
