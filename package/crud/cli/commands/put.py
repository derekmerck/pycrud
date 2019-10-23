import click
from crud.cli.utils import validate_endpoint, validate_dict


@click.command(short_help="Put chained items in endpoint")
@click.argument("dest", callback=validate_endpoint, type=click.STRING)
@click.option("-k", "--kwargs", callback=validate_dict, type=click.STRING,
              help="""kwargs dict as yaml/json format string or @file.yaml, i.e., '{"level": "series"}'""")
@click.pass_context
def cli(ctx, dest, kwargs):
    """Put chained items in endpoint"""
    click.echo(click.style('Putting Items in Dest', underline=True, bold=True))
    for item in ctx.obj.get("items", []):
        dest.put(item, **kwargs)
