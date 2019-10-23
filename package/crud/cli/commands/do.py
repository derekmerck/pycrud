import yaml
import click
from pprint import pformat
from crud.cli.utils import validate_array, validate_dict, validate_endpoint


@click.command(short_help="Call endpoint method")
@click.argument('endpoint', callback=validate_endpoint, type=click.STRING)
@click.argument('method',   type=click.STRING)
@click.option('--args',    '-g', type=click.STRING, callback=validate_array,
              help="Arguments as comma or newline separated or @file.txt format")
@click.option('--mapargs', '-m', type=click.STRING, callback=validate_dict,
              help="Mapping-type arguments as json or @file.yaml format")
@click.option('--kwargs',  '-k', type=click.STRING, callback=validate_dict,
              help="Keyword arguments as json or @file.yaml format")
@click.pass_context
def cli(ctx, endpoint, method, args, mapargs, kwargs):
    """Call an arbitrary endpoint method with *args or *mapargs and **kwargs.

    \b
    $ crud-cli do redis check
    $ crud-cli do redis find -m '{"data":"test"}'
    $ crud-cli do redis get -g my_key print
    $ crud-cli do orthanc get xxxx-xxxx... -k '{"level":"series"}'
    """

    click.echo(click.style('Calling endpoint method {}'.format(method), underline=True, bold=True))

    if hasattr(endpoint, method):

        if not ctx.obj.get("items"):
            ctx.obj["items"] = []

        for arg in [*args, *mapargs]:
            out = getattr(endpoint, method)(arg, **kwargs)
            ctx.obj["items"].append(out)

    else:
        click.echo(click.style("No such method {}".format(method), fg="red"))
        exit(1)
