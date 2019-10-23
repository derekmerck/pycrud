import click
from crud.cli.utils import validate_dict


@click.command()
@click.argument("update_dict", type=click.STRING, callback=validate_dict)
@click.pass_context
def cli(ctx, update_dict):
    """Set metadata kvs for chained items"""
    click.echo(click.style('Set metadata key value pairs', underline=True, bold=True))

    if not ctx.obj.get("items"):
        ctx.obj["items"] = []

    for item in ctx.obj.get("items"):
        item.meta.update(update_dict)
