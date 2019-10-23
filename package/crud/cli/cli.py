# generic crud-cli version 2

import sys
import os
import logging
import click
import attr

from ..import __version__
from ..manager import EndpointManager

# Any command imports must be made here as well?
from pprint import pformat
import yaml


epilog = """
SERVICES is a required platform endpoint description in json/yaml format.

\b
---
orthanc:
  ctype: Orthanc
  port: 8042
  host: my_orthanc
redis:
  ctype: Redis
...
"""

class PluggableCli(click.MultiCommand):

    plugin_folders = [os.path.join(os.path.dirname(__file__), 'commands')]

    def list_commands(self, ctx):
        rv = []
        for plugin_folder in self.plugin_folders:
            for filename in os.listdir(plugin_folder):
                if filename == "utils.py" or filename.startswith("__"):
                    continue
                if filename.endswith('.py'):
                    rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        for plugin_folder in self.plugin_folders:
            fn = os.path.join(plugin_folder, name + '.py')
            if os.path.exists(fn):
                with open(fn) as f:
                    ns = {}
                    code = compile(f.read(), fn, 'exec')
                    gl = globals()
                    gl.update({"__name__": "commands"})
                    eval(code, gl, ns)
                return ns['cli']


# plugins = os.path.join( os.pardir( diana.cli.__file__ ), "commands" )
# logging.debug(plugins)

try:
    import diana
    diana_loc = os.path.dirname(diana.__file__)
    path = os.path.join(diana_loc, "cli", "commands")
    PluggableCli.plugin_folders.append(path)

    # Monkey patch serializable factory
    from diana.apis import *
    from diana.dixel import *
    from ..abc import Serializable
    Serializable.Factory.registry["Orthanc"] = Orthanc
    Serializable.Factory.registry["DcmDir"] = DcmDir
except ImportError:
    pass

try:
    import wuphf
    wuphf_loc = os.path.dirname(wuphf.__file__)
    path = os.path.join(wuphf_loc, "cli", "commands")
    PluggableCli.plugin_folders.append(path)
except ImportError:
    pass


@click.group(name="crud-cli", epilog=epilog, chain=True, cls=PluggableCli)
@click.version_option(version=__version__, prog_name="crud-cli")
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('-s', '--services',
              help="Services dict as yaml/json format string or @file.yaml")
@click.pass_context
def cli(ctx, verbose, services):
    """Run diana packages using a command-line interface."""

    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        click.echo('Verbose mode is ON')
    else:
        logging.basicConfig(level=logging.WARNING)

    if verbose:
        click.echo("Using services: {}".format(services))

    # Runner does not instantiate ctx properly
    if not ctx.obj:
        ctx.obj = {}

    service_mgr = EndpointManager(services)

    ctx.obj['services'] = service_mgr
