import yaml
import click
from pprint import pformat
from crud.endpoints import *


@click.command(short_help="Check endpoint health")
@click.argument('endpoint', type=click.STRING)
@click.pass_context
def check(ctx, endpoint):
    """Check ENDPOINT health.
     \b
     $ crud-cli check redis
    """
    manager = ctx.obj.get('manager')

    ep = manager.get(endpoint)
    if not ep:
        click.echo(click.style("No such endpoint {}".format(endpoint), fg="red"))
        exit(1)

    click.echo(click.style('Calling endpoint check method', underline=True, bold=True))

    out = ep.check()

    if out:
        click.echo(pformat(out))
        exit(0)
    else:
        click.echo(click.style("No response", fg="red"))
        exit(2)
