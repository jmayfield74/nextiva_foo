"""
Flask application routes and handlers.
"""
from flask import Flask, jsonify, request
from nextiva_foo.utils import passwords, spirals

app = Flask(__name__)


# CONSTANTS ===================================================================

PASSWORD_FIELDS = [
    "min_chars",
    "max_chars",
    "integers",
    "specials",
    "uppers",
]

SPIRAL_FIELDS = ["matrix"]


# API Routes ==================================================================

@app.route('/rpc/password', methods=["GET"])
def generate_password():
    return handle_request(
        passwords.generate,
        request.args,
        PASSWORD_FIELDS,
        cast=int
    )


@app.route('/rpc/spiral', methods=["POST"])
def spiral_sort():
    return handle_request(
        spirals.sort,
        request.get_json(),
        SPIRAL_FIELDS
    )


# Helpers =====================================================================

def handle_request(execute, input_data, valid_fields, cast=None):
    """
    Generic handler for routes. Handles input cleaning, exceptions, etc.
    """
    try:
        params = clean_input(
            input_data,
            valid_fields,
            cast=cast
        )
        result = execute(**params)
    except AssertionError, e:   # the expected assertion error
        return e.message, 400
    except Exception, e:        # all other downstream issues
        return "EGAD! {}".format(e.message), 500

    response = {"result": result}
    return jsonify(response)


def clean_input(data, fields, cast=None):
    """
    Fetch values from `data` for each field in `fields` and
    apply `cast` function if not None.
    """
    new_params = {}
    for field in fields:
        value = data.get(field)
        if value:
            if cast:
                value = cast(value)
            new_params[field] = value
    return new_params


def start():
    app.run(debug=True)
