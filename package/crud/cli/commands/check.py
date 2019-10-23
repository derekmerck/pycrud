import click
from crud.cli.utils import validate_endpoint


@click.command(short_help="Check endpoint status")
@click.argument("endpoint", callback=validate_endpoint, type=click.STRING)
@click.pass_context
def cli(ctx, endpoint):
    """Check endpoint status

    \b
    $ crud-cli check redis
    """
    click.echo(click.style('Check Endpoint Status', underline=True, bold=True))
    avail = endpoint.check()

    s = "{}: {}".format(endpoint.name, "Ready" if avail else "Unavailable")
    if avail:
        click.echo(click.style(s, fg="green"))
    else:
        click.echo(click.style(s, fg="red"))
