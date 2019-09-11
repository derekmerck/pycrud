import logging, os
import yaml
import click
from crud import __version__
from crud.endpoints import *
from crud.daemons import *
from crud.manager import EndpointManager
from crud.cli import *

epilog = """
SERVICES or SERVICE_PATH is a required platform endpoint description in yaml format.

\b
---
redis:
  ctype: Redis
  host: localhost
  port: 6789
...
"""

@click.group(name="crud-cli", epilog=epilog)
@click.option('--verbose/--no-verbose', default=False)
@click.version_option(version=__version__, prog_name="python-wuphf")
@click.option('-s', '--services', type=click.STRING,
              help="CRUD service desc as yaml format string")
@click.option('-S', '--services_path', type=click.Path(exists=True),
              help="CRUD service desc as a yaml format file")
@click.pass_context
def cli(ctx, verbose, services, services_path):
    """Call CRUD endpoints using a command-line interface."""

    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        # suppress_urllib_debug()
        click.echo('Verbose mode is %s' % ('on' if verbose else 'off'))
        # suppress_watcher_debug()
    else:
        logging.basicConfig(level=logging.WARNING)
        # suppress_urllib_debug()

    manager = EndpointManager(json=services, file=services_path)

    # Runner does not instantiate ctx properly
    if not ctx.obj:
        ctx.obj = {}
    ctx.obj['manager'] = manager


cmds = [
    check,
    do,
    ls
]
for c in cmds:
    cli.add_command(c)


# Indirection to set envar prefix from setuptools entry pt
def main():
    cli(auto_envvar_prefix='CRUD', obj={})


if __name__ == "__main__":
    main()
