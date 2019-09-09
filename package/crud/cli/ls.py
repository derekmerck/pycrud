import yaml
import click
from pprint import pformat
from crud.endpoints import *


@click.command(short_help="List endpoints")
@click.option('--check', '-c', is_flag=True, type=click.BOOL, default=False,
              help="Check health")
@click.pass_context
def ls(ctx, check):
    """List known endpoints.
     \b
     $ crud-cli ls
    """
    manager = ctx.obj.get('manager')

    for ep in manager.get_all(check):
        click.echo(pformat(ep))
