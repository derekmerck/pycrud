from typing import Mapping, List
import click
from crud.abc import Endpoint
from crud.cli.utils import CLICK_ENDPOINT, CLICK_MAPPING, CLICK_ARRAY


@click.command()
@click.argument("source", type=CLICK_ENDPOINT)
@click.argument("items", type=CLICK_ARRAY)  # oid or fn
@click.option("-k", "--kwargs", type=CLICK_MAPPING,
              help="""kwargs dict as yaml/json format string or @file.yaml, i.e., '{"level": "series"}'""")
@click.option("-b", "--binary", is_flag=True, default=False,
              help="Get binary file as well as data")
@click.pass_context
def get(ctx, source: Endpoint, items: List, kwargs: Mapping, binary: bool):
    """Get items from endpoint for chaining"""
    click.echo(click.style('Get Items from Endpoint', underline=True, bold=True))

    if not ctx.obj.get("items"):
        ctx.obj["items"] = []

    for item in items:
        _item = source.get(item, file=binary, **kwargs)
        ctx.obj["items"].append(_item)