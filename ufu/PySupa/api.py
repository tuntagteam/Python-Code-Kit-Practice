"""Teaching-friendly JSON API for the After Class Kitchen database."""

from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request


ORDER_TYPES = {"DINE_IN", "TAKEAWAY", "DELIVERY"}
ORDER_STATUSES = {"PENDING", "COOKING", "READY", "COMPLETED", "CANCELLED"}
PAYMENT_METHODS = {"CASH", "QR", "CARD", "TRANSFER"}
PAYMENT_STATUSES = {"PENDING", "PAID", "REFUNDED"}


class ApiProblem(Exception):
    """An expected client error that should be returned as JSON."""

    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


def register_api(app, supabase):
    """Register all /api routes on an existing Flask application."""

    api = Blueprint("api", __name__, url_prefix="/api")

    def body():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            raise ApiProblem("Send a JSON object in the request body.")
        return data

    def required(data, *names):
        missing = [name for name in names if data.get(name) in (None, "")]
        if missing:
            raise ApiProblem("Missing required field(s): " + ", ".join(missing))

    def positive_int(value, name):
        try:
            number = int(value)
        except (TypeError, ValueError):
            raise ApiProblem(f"{name} must be a whole number.") from None
        if number <= 0:
            raise ApiProblem(f"{name} must be greater than zero.")
        return number

    def non_negative_money(value, name, default="0"):
        if value in (None, ""):
            value = default
        try:
            number = Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise ApiProblem(f"{name} must be a number.") from None
        if number < 0:
            raise ApiProblem(f"{name} cannot be negative.")
        return number.quantize(Decimal("0.01"))

    def one_row(response, resource_name):
        rows = response.data or []
        if not rows:
            raise ApiProblem(f"{resource_name} not found.", 404)
        return rows[0]

    @api.errorhandler(ApiProblem)
    def handle_api_problem(error):
        return jsonify({"error": error.message}), error.status

    @api.errorhandler(Exception)
    def handle_database_error(error):
        app.logger.exception("API request failed")
        return jsonify({
            "error": "The database request failed.",
            "detail": str(error),
        }), 500

    @api.get("")
    def api_home():
        return jsonify({
            "name": "After Class Kitchen API",
            "version": "1.0",
            "endpoints": {
                "health": "GET /api/health",
                "categories": "GET, POST /api/categories",
                "menu_items": "GET, POST /api/menu-items",
                "menu_item": "GET, PATCH, DELETE /api/menu-items/<id>",
                "customers": "GET, POST /api/customers",
                "orders": "GET, POST /api/orders",
                "order": "GET /api/orders/<id>",
                "order_status": "PATCH /api/orders/<id>/status",
                "payments": "POST /api/orders/<id>/payments",
            },
        })

    @api.get("/health")
    def health():
        supabase.table("categories").select("category_id").limit(1).execute()
        return jsonify({"status": "ok", "database": "connected"})

    @api.get("/categories")
    def list_categories():
        result = (
            supabase.table("categories")
            .select("category_id, category_name")
            .order("category_name")
            .execute()
        )
        return jsonify(result.data or [])

    @api.post("/categories")
    def create_category():
        data = body()
        required(data, "category_name")
        result = supabase.table("categories").insert({
            "category_name": str(data["category_name"]).strip(),
        }).execute()
        return jsonify(one_row(result, "Category")), 201

    @api.get("/menu-items")
    def list_menu_items():
        query = (
            supabase.table("menu_items")
            .select("menu_item_id, item_name, description, price, is_available, categories(category_id, category_name)")
            .order("item_name")
        )
        if request.args.get("category_id"):
            query = query.eq("category_id", positive_int(request.args["category_id"], "category_id"))
        if request.args.get("available", "").lower() in {"true", "false"}:
            query = query.eq("is_available", request.args["available"].lower() == "true")
        return jsonify(query.execute().data or [])

    @api.get("/menu-items/<int:item_id>")
    def get_menu_item(item_id):
        result = (
            supabase.table("menu_items")
            .select("menu_item_id, category_id, item_name, description, price, is_available, created_at")
            .eq("menu_item_id", item_id)
            .limit(1)
            .execute()
        )
        return jsonify(one_row(result, "Menu item"))

    @api.post("/menu-items")
    def create_menu_item():
        data = body()
        required(data, "category_id", "item_name", "price")
        payload = {
            "category_id": positive_int(data["category_id"], "category_id"),
            "item_name": str(data["item_name"]).strip(),
            "description": data.get("description"),
            "price": str(non_negative_money(data["price"], "price")),
            "is_available": bool(data.get("is_available", True)),
        }
        result = supabase.table("menu_items").insert(payload).execute()
        return jsonify(one_row(result, "Menu item")), 201

    @api.patch("/menu-items/<int:item_id>")
    def update_menu_item(item_id):
        data = body()
        allowed = {"category_id", "item_name", "description", "price", "is_available"}
        payload = {key: value for key, value in data.items() if key in allowed}
        if not payload:
            raise ApiProblem("Send at least one menu item field to update.")
        if "category_id" in payload:
            payload["category_id"] = positive_int(payload["category_id"], "category_id")
        if "item_name" in payload:
            payload["item_name"] = str(payload["item_name"]).strip()
            if not payload["item_name"]:
                raise ApiProblem("item_name cannot be empty.")
        if "price" in payload:
            payload["price"] = str(non_negative_money(payload["price"], "price"))
        if "is_available" in payload and not isinstance(payload["is_available"], bool):
            raise ApiProblem("is_available must be true or false.")
        result = (
            supabase.table("menu_items")
            .update(payload)
            .eq("menu_item_id", item_id)
            .execute()
        )
        return jsonify(one_row(result, "Menu item"))

    @api.delete("/menu-items/<int:item_id>")
    def delete_menu_item(item_id):
        result = (
            supabase.table("menu_items")
            .delete()
            .eq("menu_item_id", item_id)
            .execute()
        )
        one_row(result, "Menu item")
        return "", 204

    @api.get("/customers")
    def list_customers():
        result = (
            supabase.table("customers")
            .select("customer_id, full_name, phone, email, created_at")
            .order("customer_id")
            .execute()
        )
        return jsonify(result.data or [])

    @api.post("/customers")
    def create_customer():
        data = body()
        required(data, "full_name")
        payload = {
            "full_name": str(data["full_name"]).strip(),
            "phone": data.get("phone"),
            "email": data.get("email"),
        }
        result = supabase.table("customers").insert(payload).execute()
        return jsonify(one_row(result, "Customer")), 201

    @api.get("/orders")
    def list_orders():
        query = (
            supabase.table("orders")
            .select("order_id, order_type, table_number, order_status, subtotal, discount_amount, delivery_fee, total_amount, order_date, customers(customer_id, full_name)")
            .order("order_date", desc=True)
        )
        status = request.args.get("status", "").upper()
        if status:
            if status not in ORDER_STATUSES:
                raise ApiProblem("Invalid order status.")
            query = query.eq("order_status", status)
        return jsonify(query.execute().data or [])

    @api.get("/orders/<int:order_id>")
    def get_order(order_id):
        result = (
            supabase.table("orders")
            .select("*, customers(customer_id, full_name, phone, email), order_items(*, menu_items(item_name)), payments(*)")
            .eq("order_id", order_id)
            .limit(1)
            .execute()
        )
        return jsonify(one_row(result, "Order"))

    @api.post("/orders")
    def create_order():
        data = body()
        required(data, "order_type", "items")
        order_type = str(data["order_type"]).upper()
        if order_type not in ORDER_TYPES:
            raise ApiProblem("order_type must be DINE_IN, TAKEAWAY, or DELIVERY.")
        if order_type == "DINE_IN" and not data.get("table_number"):
            raise ApiProblem("table_number is required for a dine-in order.")
        if not isinstance(data["items"], list) or not data["items"]:
            raise ApiProblem("items must be a non-empty list.")

        requested = {}
        for item in data["items"]:
            if not isinstance(item, dict):
                raise ApiProblem("Every item must be a JSON object.")
            required(item, "menu_item_id", "quantity")
            item_id = positive_int(item["menu_item_id"], "menu_item_id")
            if item_id in requested:
                raise ApiProblem(f"menu_item_id {item_id} appears more than once.")
            requested[item_id] = {
                "quantity": positive_int(item["quantity"], "quantity"),
                "note": item.get("note"),
            }

        menu_result = (
            supabase.table("menu_items")
            .select("menu_item_id, item_name, price, is_available")
            .in_("menu_item_id", list(requested))
            .execute()
        )
        menu_by_id = {row["menu_item_id"]: row for row in (menu_result.data or [])}
        missing = sorted(set(requested) - set(menu_by_id))
        if missing:
            raise ApiProblem(f"Unknown menu_item_id value(s): {missing}")
        unavailable = [row["item_name"] for row in menu_by_id.values() if not row["is_available"]]
        if unavailable:
            raise ApiProblem("Unavailable menu item(s): " + ", ".join(unavailable))

        order_items = []
        subtotal = Decimal("0")
        for item_id, request_item in requested.items():
            unit_price = Decimal(str(menu_by_id[item_id]["price"]))
            subtotal += unit_price * request_item["quantity"]
            order_items.append({
                "menu_item_id": item_id,
                "quantity": request_item["quantity"],
                "unit_price": str(unit_price),
                "note": request_item["note"],
            })

        discount = non_negative_money(data.get("discount_amount"), "discount_amount")
        delivery_fee = non_negative_money(data.get("delivery_fee"), "delivery_fee")
        if discount > subtotal:
            raise ApiProblem("discount_amount cannot be greater than subtotal.")
        total = subtotal - discount + delivery_fee
        order_payload = {
            "customer_id": data.get("customer_id"),
            "order_type": order_type,
            "table_number": data.get("table_number") if order_type == "DINE_IN" else None,
            "order_status": "PENDING",
            "subtotal": str(subtotal.quantize(Decimal("0.01"))),
            "discount_amount": str(discount),
            "delivery_fee": str(delivery_fee),
            "total_amount": str(total.quantize(Decimal("0.01"))),
        }
        if order_payload["customer_id"] is not None:
            order_payload["customer_id"] = positive_int(order_payload["customer_id"], "customer_id")

        created_order = one_row(
            supabase.table("orders").insert(order_payload).execute(),
            "Order",
        )
        order_id = created_order["order_id"]
        for item in order_items:
            item["order_id"] = order_id
        try:
            supabase.table("order_items").insert(order_items).execute()
        except Exception:
            # Best-effort cleanup. For production, move this operation into a
            # PostgreSQL function so the order and its items use one transaction.
            supabase.table("orders").delete().eq("order_id", order_id).execute()
            raise

        return get_order(order_id), 201

    @api.patch("/orders/<int:order_id>/status")
    def update_order_status(order_id):
        data = body()
        required(data, "order_status")
        status = str(data["order_status"]).upper()
        if status not in ORDER_STATUSES:
            raise ApiProblem("Invalid order_status.")
        result = (
            supabase.table("orders")
            .update({"order_status": status})
            .eq("order_id", order_id)
            .execute()
        )
        return jsonify(one_row(result, "Order"))

    @api.post("/orders/<int:order_id>/payments")
    def create_payment(order_id):
        data = body()
        required(data, "payment_method", "amount")
        method = str(data["payment_method"]).upper()
        status = str(data.get("payment_status", "PAID")).upper()
        if method not in PAYMENT_METHODS:
            raise ApiProblem("Invalid payment_method.")
        if status not in PAYMENT_STATUSES:
            raise ApiProblem("Invalid payment_status.")
        amount = non_negative_money(data["amount"], "amount")
        if amount <= 0:
            raise ApiProblem("amount must be greater than zero.")
        payload = {
            "order_id": order_id,
            "payment_method": method,
            "amount": str(amount),
            "payment_status": status,
        }
        result = supabase.table("payments").insert(payload).execute()
        return jsonify(one_row(result, "Payment")), 201

    app.register_blueprint(api)

