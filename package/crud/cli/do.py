import yaml
import click
from pprint import pformat
from crud.endpoints import *


@click.command(short_help="Call endpoint method")
@click.argument('endpoint', type=click.STRING)
@click.argument('method', type=click.STRING)
@click.option('--args',       '-g', type=click.STRING, default=None,
              help="Method arguments")
@click.option('--map_args',   '-G', type=click.STRING, default=None,
              help="Method arguments in json format")
@click.option('--kwargs',     '-k', type=click.STRING, default=None,
              help="Method keyword arguments in json format")
@click.pass_context
def do(ctx, endpoint, method, args, map_args, kwargs):
    """Call ENDPOINT METHOD with *args and **kwargs.
     \b
     $ crud-cli do redis
     $ crud-cli do redis put  -g key1 value
     $ crud-cli do redis find -k '{"key": "key1"}'
    """
    manager = ctx.obj.get('manager')

    ep = manager.get("endpoint")
    if not ep:
        click.echo(click.style("No such endpoint {}".format(endpoint), fg="red"))
        exit(1)

    click.echo(click.style('Calling endpoint method', underline=True, bold=True))

    _args = []
    if args:
        _args = [args]
    elif map_args:
        _args = yaml.load(map_args)
        if not isinstance(_args, list):
            _args = [_args]

    _kwargs = {}
    if kwargs:
        _kargs = yaml.load(kwargs)

    if hasattr(ep, method):
        out = getattr(ep, method)(*_args, **_kwargs)

        if out:
            click.echo(pformat(out))
            exit(0)
        else:
            click.echo(click.style("No response", fg="red"))
            exit(2)

    else:
        click.echo(click.style("No such method {}".format(method), fg="red"))
        exit(1)
