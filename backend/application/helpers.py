from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if "admin" in claims["roles"]:
                return fn(*args, **kwargs)
            else:
                return jsonify({"msg": "Admins only!"}).get_json(), 403

        return decorator

    return wrapper


def eval_get_list(input_val):
    if not input_val:
        return []
    input_val = eval(input_val)
    print("eval func", input_val, type(input_val))
    if not isinstance(input_val, (tuple, list)):
        input_val = [input_val]
    return input_val

