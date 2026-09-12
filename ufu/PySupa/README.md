# PySupa — Python + Supabase lesson

This project demonstrates how a Flask API talks to the restaurant tables in
Supabase. The existing pages are still available, and the JSON API starts at
`/api`.

## 1. Setup

Open PowerShell in this folder, then run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and replace the example values with the values
from Supabase **Project Settings > API**. Never commit `.env` or paste a secret
key into Python code.

## 2. Database

The supplied tables must already exist in Supabase. `schema.sql` is a teaching
and sample-data script; it begins with `DROP TABLE`, so do not run it against a
database containing data you need to keep.

Supabase exposes database tables through its Data API. Make sure these tables
are exposed and that the key used by this server has the required grants:

- `customers`
- `categories`
- `menu_items`
- `orders`
- `order_items`
- `payments`

Use Row Level Security and least-privilege policies before making this project
public. A secret or service-role key belongs only on a trusted backend and must
never be included in browser JavaScript.

## 3. Run

```powershell
python app.py
```

Open:

- Dashboard: <http://127.0.0.1:5000/>
- API guide: <http://127.0.0.1:5000/api>
- Connection check: <http://127.0.0.1:5000/api/health>

## 4. Lesson requests

Read menu items:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/menu-items
```

Create a customer:

```powershell
$body = @{ full_name = "Ufu Student"; phone = "0812345678" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/customers -ContentType "application/json" -Body $body
```

Create an order. The API reads current menu prices from Supabase and calculates
the subtotal and total itself:

```powershell
$body = @{
    customer_id = 1
    order_type = "DINE_IN"
    table_number = "A1"
    items = @(
        @{ menu_item_id = 1; quantity = 1; note = "Not spicy" }
        @{ menu_item_id = 11; quantity = 1 }
    )
} | ConvertTo-Json -Depth 4

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/orders -ContentType "application/json" -Body $body
```

Update an order status:

```powershell
$body = @{ order_status = "COOKING" } | ConvertTo-Json
Invoke-RestMethod -Method Patch -Uri http://127.0.0.1:5000/api/orders/1/status -ContentType "application/json" -Body $body
```

## API overview

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Test the Supabase connection |
| GET, POST | `/api/categories` | List or create categories |
| GET, POST | `/api/menu-items` | List or create menu items |
| GET, PATCH, DELETE | `/api/menu-items/<id>` | Work with one menu item |
| GET, POST | `/api/customers` | List or create customers |
| GET, POST | `/api/orders` | List or create orders |
| GET | `/api/orders/<id>` | Get an order with items and payments |
| PATCH | `/api/orders/<id>/status` | Change an order status |
| POST | `/api/orders/<id>/payments` | Record a payment |

The multi-table order example uses cleanup if inserting its items fails. In a
production system, implement order creation as a PostgreSQL function so the
order and its items are committed in one database transaction.
