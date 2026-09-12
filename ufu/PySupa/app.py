import os
from collections import Counter, defaultdict
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, abort, render_template
from supabase import Client, create_client


load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = (
    os.getenv("SUPABASE_SECRET_KEY")
    or os.getenv("SUPABASE_KEY")
    or os.getenv("SUPABASE_PUBLISHABLE_KEY")
)

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing from .env")
if not SUPABASE_KEY:
    raise ValueError("A Supabase API key is missing from .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.template_filter("money")
def money(value):
    return f"฿{float(value or 0):,.2f}"


@app.template_filter("short_date")
def short_date(value):
    if not value:
        return "—"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d %b, %H:%M")
    except (ValueError, AttributeError):
        return value


def get_orders():
    response = (
        supabase.table("orders")
        .select("*, customers(customer_id, full_name)")
        .order("order_date", desc=True)
        .execute()
    )
    return response.data or []


@app.route("/")
def index():
    orders = get_orders()
    menu_items = (
        supabase.table("menu_items")
        .select("menu_item_id, is_available")
        .execute()
        .data
        or []
    )
    customers = (
        supabase.table("customers")
        .select("customer_id")
        .execute()
        .data
        or []
    )

    completed = [order for order in orders if order["order_status"] == "COMPLETED"]
    revenue = sum(float(order["total_amount"]) for order in completed)
    average_order = revenue / len(completed) if completed else 0
    status_counts = Counter(order["order_status"] for order in orders)
    type_counts = Counter(order["order_type"] for order in orders)
    completion_rate = round((len(completed) / len(orders)) * 100) if orders else 0
    available_menu = sum(1 for item in menu_items if item["is_available"])

    daily_sales = defaultdict(float)
    for order in completed:
        date = (order.get("order_date") or "")[:10]
        if date:
            daily_sales[date] += float(order["total_amount"])
    sales_points = [
        {"date": date, "label": date[5:].replace("-", "/"), "value": value}
        for date, value in sorted(daily_sales.items())[-7:]
    ]
    max_sales = max((point["value"] for point in sales_points), default=1)

    return render_template(
        "dashboard.html",
        active="dashboard",
        page_title="Dashboard",
        orders=orders,
        recent_orders=orders[:7],
        total_orders=len(orders),
        revenue=revenue,
        average_order=average_order,
        customer_count=len(customers),
        status_counts=status_counts,
        type_counts=type_counts,
        completion_rate=completion_rate,
        available_menu=available_menu,
        menu_count=len(menu_items),
        sales_points=sales_points,
        max_sales=max_sales,
    )


@app.route("/orders")
def orders():
    all_orders = get_orders()
    return render_template(
        "orders.html",
        active="orders",
        page_title="Orders",
        orders=all_orders,
        status_counts=Counter(order["order_status"] for order in all_orders),
    )


@app.route("/orders/<int:order_id>")
def order_detail(order_id):
    response = (
        supabase.table("orders")
        .select("*, customers(*), order_items(*, menu_items(item_name)), payments(*)")
        .eq("order_id", order_id)
        .limit(1)
        .execute()
    )
    if not response.data:
        abort(404)
    return render_template(
        "order_detail.html",
        active="orders",
        page_title=f"Order #{order_id}",
        order=response.data[0],
    )


@app.route("/menu")
def menu():
    response = (
        supabase.table("menu_items")
        .select("*, categories(category_id, category_name)")
        .order("item_name")
        .execute()
    )
    items = response.data or []
    categories = sorted({
        (item.get("categories") or {}).get("category_name", "Uncategorised")
        for item in items
    })
    return render_template(
        "menu.html",
        active="menu",
        page_title="Menu",
        menu_items=items,
        categories=categories,
        available_count=sum(1 for item in items if item["is_available"]),
    )


@app.route("/customers")
def customers():
    response = (
        supabase.table("customers")
        .select("*, orders(order_id, total_amount, order_status, order_date)")
        .order("customer_id")
        .execute()
    )
    customer_rows = response.data or []
    for customer in customer_rows:
        customer_orders = customer.get("orders") or []
        customer["lifetime_value"] = sum(
            float(order["total_amount"])
            for order in customer_orders
            if order["order_status"] == "COMPLETED"
        )
    return render_template(
        "customers.html",
        active="customers",
        page_title="Customers",
        customers=customer_rows,
    )


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html", active="", page_title="Not found"), 404


from api import register_api

register_api(app, supabase)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

