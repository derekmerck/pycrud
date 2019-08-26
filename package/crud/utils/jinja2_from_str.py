import datetime
from jinja2 import Environment, BaseLoader


def render_template(template: str, **data):

    _template = Environment(loader=BaseLoader()).from_string(template)
    _template.globals['now'] = datetime.datetime.utcnow

    return _template.render(**data)