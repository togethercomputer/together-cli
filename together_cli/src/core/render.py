def render(template, **kwargs):
    """Render a template with the given context."""
    for key, value in kwargs.items():
        template = template.replace("{{"+key.upper()+"}}", value)
    return template