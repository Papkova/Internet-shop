from flask_login import current_user


def admin_only(func):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.admin == 1:
            return func(*args, **kwargs)
        else:
            return "You do not have access"

    wrapper.__name__ = func.__name__
    return wrapper