from sqlalchemy import inspect


def model_to_dict(model_instance):
    return {c.key: getattr(model_instance, c.key) for c in inspect(model_instance).mapper.column_attrs}
