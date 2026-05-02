"""
Customer Accounts Microservice
"""

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

accounts = {}
next_account_id = 1


@app.route("/")
def index():
    """Root endpoint"""
    return jsonify(
        name="Customer Accounts Microservice",
        version="1.0"
    ), 200


@app.route("/accounts", methods=["POST"])
def create_account():
    """Create an account"""
    global next_account_id

    data = request.get_json()
    if not data:
        abort(400, description="No input data provided")

    required_fields = ["name", "email", "address", "phone_number"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing required field: {field}")

    account = {
        "id": next_account_id,
        "name": data["name"],
        "email": data["email"],
        "address": data["address"],
        "phone_number": data["phone_number"],
    }

    accounts[next_account_id] = account
    next_account_id += 1

    return jsonify(account), 201


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all accounts"""
    return jsonify(list(accounts.values())), 200


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Read one account"""
    account = accounts.get(account_id)
    if not account:
        abort(404, description="Account not found")

    return jsonify(account), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an account"""
    account = accounts.get(account_id)
    if not account:
        abort(404, description="Account not found")

    data = request.get_json()
    if not data:
        abort(400, description="No input data provided")

    account["name"] = data.get("name", account["name"])
    account["email"] = data.get("email", account["email"])
    account["address"] = data.get("address", account["address"])
    account["phone_number"] = data.get("phone_number", account["phone_number"])

    return jsonify(account), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an account"""
    account = accounts.get(account_id)
    if not account:
        abort(404, description="Account not found")

    del accounts[account_id]

    return "", 204


def reset_data():
    """Reset in-memory data for tests"""
    global next_account_id
    accounts.clear()
    next_account_id = 1
