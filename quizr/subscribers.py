from pyramid.renderers import get_renderer
from pyramid.events import (
    subscriber,
    BeforeRender,
    )

@subscriber(BeforeRender)
def add_base_template(event):
    base = get_renderer('templates/base.pt').implementation()
    event.update({'base': base})