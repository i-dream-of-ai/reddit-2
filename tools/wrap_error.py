import prawcore


def wrap_error(func):
    try:
        return func()
    except Exception as e:
        if isinstance(e, prawcore.exceptions.NotFound):
            return f"{e}: Your request returned a 404 error, indicating the resource you are looking for does not exist. Check your assumptions and try again."
        raise e
