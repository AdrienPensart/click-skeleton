'''Preconfigured version command for root AdvancedGroup (skeleton)'''
import rich_click as click  # type: ignore


@click.command(short_help='Print version')
@click.pass_context
def version_cmd(ctx: click.Context) -> None:
    '''Print version, equivalent to -V and --version'''
    click.echo(f"{click.style(ctx.obj.prog_name, fg='yellow')}, version {click.style(ctx.obj.version, fg='green')}", color=ctx.color)
