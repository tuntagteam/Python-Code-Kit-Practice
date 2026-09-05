import os

from flask import Flask, render_template_string, abort
from supabase import create_client, Client
from dotenv import load_dotenv


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")

# Supports either name
SUPABASE_KEY = (
    os.getenv("SUPABASE_KEY")
    or os.getenv("SUPABASE_PUBLISHABLE_KEY")
)

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing from .env")


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# BASE HTML
# =========================================================

STYLE = """
<style>
    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: #f5f5f5;
        color: #222;
    }

    nav {
        background: #111827;
        padding: 18px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    nav h2 {
        color: white;
        margin: 0;
    }

    nav div {
        display: flex;
        gap: 20px;
    }

    nav a {
        color: #d1d5db;
        text-decoration: none;
    }

    nav a:hover {
        color: white;
    }

    .container {
        max-width: 1200px;
        margin: auto;
        padding: 40px 20px;
    }

    h1 {
        margin-bottom: 10px;
    }

    .subtitle {
        color: #6b7280;
        margin-bottom: 30px;
    }

    .cards {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 35px;
    }

    .card {
        background: white;
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .card-title {
        color: #6b7280;
        font-size: 14px;
    }

    .card-value {
        font-size: 28px;
        font-weight: bold;
        margin-top: 8px;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 12px;
        overflow: hidden;
    }

    th,
    td {
        padding: 15px;
        text-align: left;
        border-bottom: 1px solid #eee;
    }

    th {
        background: #111827;
        color: white;
    }

    tr:hover {
        background: #f9fafb;
    }

    .status {
        padding: 6px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }

    .COMPLETED {
        background: #dcfce7;
        color: #166534;
    }

    .COOKING {
        background: #fef3c7;
        color: #92400e;
    }

    .PENDING {
        background: #e5e7eb;
        color: #374151;
    }

    .READY {
        background: #dbeafe;
        color: #1d4ed8;
    }

    .CANCELLED {
        background: #fee2e2;
        color: #991b1b;
    }

    .button {
        display: inline-block;
        padding: 8px 14px;
        background: #111827;
        color: white;
        text-decoration: none;
        border-radius: 6px;
    }

    .button:hover {
        background: #374151;
    }

    .price {
        font-weight: bold;
    }

    .order-info {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-bottom: 30px;
    }

    .info-box {
        background: white;
        padding: 18px;
        border-radius: 10px;
    }

    .label {
        color: #6b7280;
        font-size: 13px;
        margin-bottom: 5px;
    }

    .value {
        font-weight: bold;
    }

    @media (max-width: 800px) {
        .cards {
            grid-template-columns: 1fr 1fr;
        }

        .order-info {
            grid-template-columns: 1fr;
        }

        table {
            font-size: 13px;
        }
    }
</style>
"""


NAV = """
<nav>
    <h2>After Class Kitchen</h2>

    <div>
        <a href="/">Dashboard</a>
        <a href="/orders">Orders</a>
        <a href="/menu">Menu</a>
        <a href="/customers">Customers</a>
    </div>
</nav>
"""


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def index():

    orders_response = (
        supabase
        .table("orders")
        .select("*")
        .order("order_date", desc=True)
        .execute()
    )

    orders = orders_response.data or []

    total_orders = len(orders)

    completed_orders = [
        order
        for order in orders
        if order["order_status"] == "COMPLETED"
    ]

    total_sales = sum(
        float(order["total_amount"])
        for order in completed_orders
    )

    cooking_orders = len([
        order
        for order in orders
        if order["order_status"] == "COOKING"
    ])

    pending_orders = len([
        order
        for order in orders
        if order["order_status"] == "PENDING"
    ])

    html = """
    <!DOCTYPE html>

    <html>

    <head>
        <title>Food Shop Dashboard</title>
        {{ style|safe }}
    </head>

    <body>

        {{ nav|safe }}

        <div class="container">

            <h1>Dashboard</h1>

            <div class="subtitle">
                Food shop overview
            </div>


            <div class="cards">

                <div class="card">
                    <div class="card-title">
                        Total Orders
                    </div>

                    <div class="card-value">
                        {{ total_orders }}
                    </div>
                </div>


                <div class="card">
                    <div class="card-title">
                        Total Sales
                    </div>

                    <div class="card-value">
                        ฿{{ "%.2f"|format(total_sales) }}
                    </div>
                </div>


                <div class="card">
                    <div class="card-title">
                        Cooking
                    </div>

                    <div class="card-value">
                        {{ cooking_orders }}
                    </div>
                </div>


                <div class="card">
                    <div class="card-title">
                        Pending
                    </div>

                    <div class="card-value">
                        {{ pending_orders }}
                    </div>
                </div>

            </div>


            <h2>Recent Orders</h2>

            <table>

                <tr>
                    <th>Order</th>
                    <th>Type</th>
                    <th>Table</th>
                    <th>Status</th>
                    <th>Total</th>
                    <th></th>
                </tr>

                {% for order in orders %}

                    <tr>

                        <td>
                            #{{ order.order_id }}
                        </td>

                        <td>
                            {{ order.order_type }}
                        </td>

                        <td>
                            {{ order.table_number or "-" }}
                        </td>

                        <td>
                            <span class="status {{ order.order_status }}">
                                {{ order.order_status }}
                            </span>
                        </td>

                        <td class="price">
                            ฿{{ "%.2f"|format(order.total_amount|float) }}
                        </td>

                        <td>
                            <a
                                class="button"
                                href="/orders/{{ order.order_id }}"
                            >
                                View
                            </a>
                        </td>

                    </tr>

                {% endfor %}

            </table>

        </div>

    </body>

    </html>
    """

    return render_template_string(
        html,
        style=STYLE,
        nav=NAV,
        orders=orders[:10],
        total_orders=total_orders,
        total_sales=total_sales,
        cooking_orders=cooking_orders,
        pending_orders=pending_orders
    )


# =========================================================
# ALL ORDERS
# =========================================================

@app.route("/orders")
def orders():

    response = (
        supabase
        .table("orders")
        .select("""
            order_id,
            order_date,
            order_type,
            table_number,
            order_status,
            subtotal,
            discount_amount,
            delivery_fee,
            total_amount,
            customers (
                customer_id,
                full_name,
                phone
            )
        """)
        .order("order_date", desc=True)
        .execute()
    )

    orders = response.data or []

    html = """
    <!DOCTYPE html>

    <html>

    <head>
        <title>Orders</title>
        {{ style|safe }}
    </head>

    <body>

    {{ nav|safe }}

    <div class="container">

        <h1>Orders</h1>

        <div class="subtitle">
            All customer orders
        </div>

        <table>

            <tr>
                <th>Order</th>
                <th>Customer</th>
                <th>Type</th>
                <th>Table</th>
                <th>Status</th>
                <th>Total</th>
                <th></th>
            </tr>


            {% for order in orders %}

            <tr>

                <td>
                    #{{ order.order_id }}
                </td>


                <td>

                    {% if order.customers %}

                        {{ order.customers.full_name }}

                    {% else %}

                        Walk-in Customer

                    {% endif %}

                </td>


                <td>
                    {{ order.order_type }}
                </td>


                <td>
                    {{ order.table_number or "-" }}
                </td>


                <td>

                    <span class="status {{ order.order_status }}">
                        {{ order.order_status }}
                    </span>

                </td>


                <td class="price">

                    ฿{{ "%.2f"|format(order.total_amount|float) }}

                </td>


                <td>

                    <a
                        href="/orders/{{ order.order_id }}"
                        class="button"
                    >
                        View
                    </a>

                </td>

            </tr>

            {% endfor %}

        </table>

    </div>

    </body>
    </html>
    """

    return render_template_string(
        html,
        orders=orders,
        style=STYLE,
        nav=NAV
    )


# =========================================================
# ONE ORDER / RECEIPT
# =========================================================

@app.route("/orders/<int:order_id>")
def order_detail(order_id):

    response = (
        supabase
        .table("orders")
        .select("""
            order_id,
            customer_id,
            order_type,
            table_number,
            order_status,
            subtotal,
            discount_amount,
            delivery_fee,
            total_amount,
            order_date,

            customers (
                customer_id,
                full_name,
                phone,
                email
            ),

            order_items (
                order_item_id,
                quantity,
                unit_price,
                line_total,
                note,

                menu_items (
                    menu_item_id,
                    item_name,

                    categories (
                        category_name
                    )
                )
            ),

            payments (
                payment_id,
                payment_method,
                amount,
                payment_status,
                paid_at
            )
        """)
        .eq("order_id", order_id)
        .execute()
    )

    if not response.data:
        abort(404)

    order = response.data[0]

    html = """
    <!DOCTYPE html>

    <html>

    <head>

        <title>
            Order #{{ order.order_id }}
        </title>

        {{ style|safe }}

    </head>


    <body>

    {{ nav|safe }}


    <div class="container">

        <h1>
            Order #{{ order.order_id }}
        </h1>


        <div class="subtitle">
            Complete order information
        </div>


        <div class="order-info">


            <div class="info-box">

                <div class="label">
                    Customer
                </div>

                <div class="value">

                    {% if order.customers %}

                        {{ order.customers.full_name }}

                    {% else %}

                        Walk-in Customer

                    {% endif %}

                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    Order Type
                </div>

                <div class="value">
                    {{ order.order_type }}
                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    Status
                </div>

                <div class="value">

                    <span class="status {{ order.order_status }}">
                        {{ order.order_status }}
                    </span>

                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    Table
                </div>

                <div class="value">
                    {{ order.table_number or "-" }}
                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    Date
                </div>

                <div class="value">
                    {{ order.order_date }}
                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    Total
                </div>

                <div class="value">

                    ฿{{ "%.2f"|format(order.total_amount|float) }}

                </div>

            </div>

        </div>


        <h2>Order Items</h2>


        <table>

            <tr>
                <th>Item</th>
                <th>Category</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Total</th>
                <th>Note</th>
            </tr>


            {% for item in order.order_items %}

            <tr>

                <td>

                    {{ item.menu_items.item_name }}

                </td>


                <td>

                    {% if item.menu_items.categories %}

                        {{ item.menu_items.categories.category_name }}

                    {% else %}

                        -

                    {% endif %}

                </td>


                <td>
                    {{ item.quantity }}
                </td>


                <td>

                    ฿{{ "%.2f"|format(item.unit_price|float) }}

                </td>


                <td>

                    ฿{{ "%.2f"|format(item.line_total|float) }}

                </td>


                <td>

                    {{ item.note or "-" }}

                </td>

            </tr>

            {% endfor %}

        </table>


        <br><br>


        <div class="order-info">

            <div class="info-box">

                <div class="label">
                    Subtotal
                </div>

                <div class="value">
                    ฿{{ "%.2f"|format(order.subtotal|float) }}
                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    Discount
                </div>

                <div class="value">
                    ฿{{ "%.2f"|format(order.discount_amount|float) }}
                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    Delivery
                </div>

                <div class="value">
                    ฿{{ "%.2f"|format(order.delivery_fee|float) }}
                </div>

            </div>


            <div class="info-box">

                <div class="label">
                    Grand Total
                </div>

                <div class="value">
                    ฿{{ "%.2f"|format(order.total_amount|float) }}
                </div>

            </div>

        </div>


        <h2>Payment</h2>


        {% if order.payments %}

            <table>

                <tr>
                    <th>Method</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Paid At</th>
                </tr>


                {% for payment in order.payments %}

                <tr>

                    <td>
                        {{ payment.payment_method }}
                    </td>

                    <td>
                        ฿{{ "%.2f"|format(payment.amount|float) }}
                    </td>

                    <td>
                        {{ payment.payment_status }}
                    </td>

                    <td>
                        {{ payment.paid_at }}
                    </td>

                </tr>

                {% endfor %}

            </table>

        {% else %}

            <p>No payment found.</p>

        {% endif %}


    </div>

    </body>
    </html>
    """

    return render_template_string(
        html,
        order=order,
        style=STYLE,
        nav=NAV
    )


# =========================================================
# MENU
# =========================================================

@app.route("/menu")
def menu():

    response = (
        supabase
        .table("menu_items")
        .select("""
            menu_item_id,
            item_name,
            description,
            price,
            is_available,

            categories (
                category_id,
                category_name
            )
        """)
        .order("item_name")
        .execute()
    )

    menu_items = response.data or []

    html = """
    <!DOCTYPE html>

    <html>

    <head>
        <title>Menu</title>
        {{ style|safe }}
    </head>

    <body>

    {{ nav|safe }}


    <div class="container">

        <h1>Menu</h1>

        <div class="subtitle">
            Food and drink menu
        </div>


        <table>

            <tr>
                <th>ID</th>
                <th>Category</th>
                <th>Food</th>
                <th>Description</th>
                <th>Price</th>
                <th>Available</th>
            </tr>


            {% for item in menu_items %}

            <tr>

                <td>
                    {{ item.menu_item_id }}
                </td>


                <td>

                    {% if item.categories %}

                        {{ item.categories.category_name }}

                    {% else %}

                        -

                    {% endif %}

                </td>


                <td>
                    {{ item.item_name }}
                </td>


                <td>
                    {{ item.description or "-" }}
                </td>


                <td class="price">

                    ฿{{ "%.2f"|format(item.price|float) }}

                </td>


                <td>

                    {% if item.is_available %}

                        Yes

                    {% else %}

                        No

                    {% endif %}

                </td>

            </tr>

            {% endfor %}

        </table>

    </div>

    </body>

    </html>
    """

    return render_template_string(
        html,
        menu_items=menu_items,
        style=STYLE,
        nav=NAV
    )


# =========================================================
# CUSTOMERS
# =========================================================

@app.route("/customers")
def customers():

    response = (
        supabase
        .table("customers")
        .select("""
            customer_id,
            full_name,
            phone,
            email,
            created_at,
            orders (
                order_id,
                total_amount,
                order_status
            )
        """)
        .order("customer_id")
        .execute()
    )

    customers = response.data or []

    html = """
    <!DOCTYPE html>

    <html>

    <head>
        <title>Customers</title>
        {{ style|safe }}
    </head>

    <body>

    {{ nav|safe }}

    <div class="container">

        <h1>Customers</h1>

        <div class="subtitle">
            Customer database
        </div>


        <table>

            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Orders</th>
            </tr>


            {% for customer in customers %}

            <tr>

                <td>
                    {{ customer.customer_id }}
                </td>

                <td>
                    {{ customer.full_name }}
                </td>

                <td>
                    {{ customer.phone or "-" }}
                </td>

                <td>
                    {{ customer.email or "-" }}
                </td>

                <td>
                    {{ customer.orders|length }}
                </td>

            </tr>

            {% endfor %}

        </table>

    </div>

    </body>

    </html>
    """

    return render_template_string(
        html,
        customers=customers,
        style=STYLE,
        nav=NAV
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )