import click
from crud.cli.utils import validate_endpoint, validate_dict, validate_array


@click.command(short_help="Get items from endpoint for chaining")
@click.argument("source", callback=validate_endpoint, type=click.STRING)
@click.argument("items", callback=validate_array, type=click.STRING)  # oid or fn
@click.option("-k", "--kwargs", callback=validate_dict, type=click.STRING,
              help="""kwargs dict as yaml/json format string or @file.yaml, i.e., '{"level": "series"}'""")
@click.option("-b", "--binary", help="Get binary file as well as data", is_flag=True, default=False)
@click.pass_context
def cli(ctx, source, items, kwargs, binary):
    """Get items from endpoint for chaining"""
    click.echo(click.style('Get Items from Endpoint', underline=True, bold=True))

    if not ctx.obj.get("items"):
        ctx.obj["items"] = []

    for item in items:
        _item = source.get(item, file=binary, **kwargs)
        ctx.obj["items"].append(_item)
