from crud.utils import deserialize_dict, deserialize_array
import click
from crud.exceptions import EndpointFactoryException



def validate_dict(ctx, param, value):
    """Convert json str or @file.yaml to dict"""

    if not value:
        return {}
    try:
        return deserialize_dict(value)
    except:
        raise click.BadParameter("Failed to deserialize dict")


def validate_array(ctx, param, value):
    """Convert comma or new line separated str or @file.txt to array"""

    if not value:
        return []
    try:
        return deserialize_array(value)
    except:
        raise click.BadParameter("Failed to deserialize array")


def validate_endpoint(ctx, param, value):
    if not value:
        return
    mgr = ctx.obj.get("services")
    if not mgr:
        raise click.BadParameter("No service manager available")
    try:
        ep = mgr.get(value)
    except EndpointFactoryException:
        raise click.BadParameter('Service "{}" could not be instantiated'.format(value))
    return ep

