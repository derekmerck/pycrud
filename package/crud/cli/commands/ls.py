import click


@click.command(short_help="List all services and health")
@click.pass_context
def cli(ctx):
    """List all services and health

    \b
    $ crud-cli ls
    """
    click.echo(click.style('List Services and Health', underline=True, bold=True))

    for ep in ctx.obj["services"].get_all():
        avail = ep.check()
        click.echo("{}: {}".format(ep.name, avail))
