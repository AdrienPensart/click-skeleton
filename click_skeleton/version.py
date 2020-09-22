'''Preconfigured version command for root AdvancedGroup (skeleton)'''
import click


@click.command(short_help='Print version')
@click.pass_context
def version_cmd(ctx: click.Context) -> None:
    '''Print version

       Equivalent : -V
    '''
    click.echo(f"{click.style(ctx.obj.prog_name, fg='yellow')}, version {click.style(ctx.obj.version, fg='green')}")
