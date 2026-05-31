# Overclock

Overclock is a premium gaming PC e-commerce platform split into two independent Django applications:

| App | Folder | Port | Purpose |
|-----|--------|------|---------|
| **PC Shop** | `pcshop/` | 8000 | Customer-facing storefront |
| **Admin Portal** | `adminportal/` | 8001 | Staff management dashboard |

Both apps share the same SQLite database (`pcshop/db.sqlite3`), so products, users, reviews, and feedback stay in sync across the storefront and admin panel.

---

## Tech Stack

- **Backend:** Django 5.2
- **Database:** SQLite (shared)
- **Frontend:** Bootstrap 5, Bootstrap Icons, custom cyberpunk theme (`theme.css`)
- **Fonts:** Orbitron, Rajdhani, Inter (Google Fonts)
- **Charts (storefront analytics page):** Chart.js

---

## Prerequisites

- Python 3.10+
- pip

Install Django if needed:

```bash
pip install django
```

For product image uploads, Pillow is also required:

```bash
pip install pillow
```

---

## Project Structure

```
overclock/
├── README.md
├── pcshop/                          # Storefront Django project
│   ├── manage.py
│   ├── db.sqlite3                   # Shared database (created after migrate)
│   ├── overclock_pc_shop/           # Project settings & URLs
│   ├── shop/                        # Products, catalog, cart, builder
│   │   ├── models.py                # Category, Product, Review, Feedback
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── management/commands/
│   │       └── seed_db.py           # Seed products, reviews, feedback, admin user
│   ├── accounts/                    # User login, register, logout
│   ├── templates/                   # HTML templates
│   ├── static/                      # CSS, JS, images
│   └── media/                       # Uploaded product images
│
└── adminportal/                     # Admin Django project (separate app)
    ├── manage.py
    ├── config/                      # Project settings & URLs
    ├── portal/                      # Admin views, forms, decorators
    │   ├── views.py
    │   ├── forms.py
    │   ├── urls.py
    │   └── management/commands/
    │       └── setup_admin.py       # Create/update admin user
    └── templates/portal/            # Admin panel templates
```

---

## Development Setup

### 1. Set up PC Shop (first time)

```bash
cd pcshop
python manage.py migrate
python manage.py seed_db
```

`seed_db` populates:
- Product categories (prebuilt, GPU, CPU, RAM, storage)
- 7 sample products (prebuilt rigs and components)
- Sample reviews and feedback
- Admin user credentials (see [Credentials](#credentials))

To reset and re-seed everything:

```bash
python manage.py seed_db --clear
```

### 2. Set up Admin Portal (first time)

```bash
cd adminportal
python manage.py migrate
python manage.py setup_admin
```

`setup_admin` creates or updates the staff superuser used to log into the admin portal.

---

## Running the Servers

Each app runs in its own terminal from its own folder.

**Terminal 1 — PC Shop:**

```bash
cd pcshop
python manage.py runserver 8000
```

Open: http://127.0.0.1:8000/

**Terminal 2 — Admin Portal:**

```bash
cd adminportal
python manage.py runserver 8001
```

Open: http://127.0.0.1:8001/

> Both apps can run at the same time. They share one SQLite database with a 20-second lock timeout to reduce conflicts during development.

---

## Credentials

| App | Username | Password | Notes |
|-----|----------|----------|-------|
| Admin Portal | `soorya` | `soorya2006` | Staff/superuser — created by `setup_admin` |
| PC Shop | *(register)* | *(your choice)* | Create a customer account via `/accounts/register/` |

The admin portal login is at http://127.0.0.1:8001/login/

---

## PC Shop Features

### Storefront Pages

| URL | Page | Description |
|-----|------|-------------|
| `/` | Home | Featured prebuilt rigs and trending components |
| `/catalog/` | Catalog | Browse all products with category filter and search |
| `/product/<slug>/` | Product Detail | Full specs, pricing, and related products |
| `/builder/` | PC Builder | Interactive custom PC configurator with part selection |
| `/cart/` | Shopping Cart | Cart items, upgrades, and add-on suggestions |
| `/checkout/` | Checkout | Order summary and checkout flow |
| `/dashboard/` | User Dashboard | Order history, saved builds, and wishlist |
| `/admin-dashboard/` | Analytics | Sales charts and inventory overview (demo/mock data) |

### User Accounts

| URL | Description |
|-----|-------------|
| `/accounts/register/` | Create a new customer account |
| `/accounts/login/` | Log in to the storefront |
| `/accounts/logout/` | Log out |

### Shop App — Data Models

- **Category** — Product type (prebuilt, gpu, cpu, ram, storage, etc.)
- **Product** — Full product record with pricing, specs, stock, badges, and homepage flags
- **Review** — Customer product reviews (rating, title, content, approval status)
- **Feedback** — General support/contact messages (new, read, resolved)

### Shop App — Key Features

- Category-based product filtering and text search
- Featured and trending product sections on the homepage
- Hardware spec fields per product (CPU, GPU, RAM, storage, mobo, PSU, cooler, case)
- Product badges (FLAGSHIP, NEW, HOT, etc.)
- Stock tracking and in-stock toggle
- Image support via static filename or uploaded file
- Cyberpunk-themed responsive UI with floating PC Builder shortcut
- Django admin at `/admin/` for low-level database access

### Static Assets (PC Shop)

```
pcshop/static/
├── css/theme.css       # Cyberpunk design system
└── js/
    ├── app.js          # Global UI behavior
    ├── builder.js      # PC builder logic
    ├── cart.js         # Cart interactions
    └── admin.js        # Analytics dashboard charts
```

---

## Admin Portal Features

The admin portal is a completely separate Django project. It reads and writes the same database as PC Shop but has its own login, templates, and URL structure.

### Admin Pages

| URL | Page | Description |
|-----|------|-------------|
| `/login/` | Login | Staff-only authentication |
| `/` | Dashboard | Overview stats, recent reviews, feedback, and products |
| `/products/` | Product List | Search and filter all products |
| `/products/add/` | Add Product | Create a new product |
| `/products/<id>/edit/` | Edit Product | Update product details and specs |
| `/products/<id>/delete/` | Delete Product | Remove a product |
| `/users/` | User List | Search all registered users |
| `/users/<id>/edit/` | Edit User | Update user info, active/staff status |
| `/reviews/` | Review List | Filter by pending or approved |
| `/reviews/<id>/edit/` | Edit Review | Modify review content and approval |
| `/reviews/<id>/toggle/` | Toggle Approval | Approve or unapprove a review |
| `/reviews/<id>/delete/` | Delete Review | Remove a review |
| `/feedback/` | Feedback List | Filter by status (new, read, resolved) |
| `/feedback/<id>/` | Feedback Detail | View message and update status |
| `/feedback/<id>/delete/` | Delete Feedback | Remove a feedback entry |

### Admin Portal — Key Features

- Staff-only access enforced by `@staff_required` decorator
- Full product CRUD with all hardware spec fields
- User management (username, email, name, active, staff flags)
- Review moderation with approve/unapprove and automatic product rating recalculation
- Feedback triage with status workflow (new → read → resolved)
- Sidebar navigation with cyberpunk theme matching the storefront
- "View Shop" link opens the PC Shop in a new tab

### How Admin Portal Connects to PC Shop

`adminportal/config/settings.py` adds the pcshop folder to `sys.path` and registers the `shop` app. This lets the admin portal import and manage the same models without duplicating code:

```python
PCSHOP_DIR = BASE_DIR.parent / 'pcshop'
sys.path.insert(0, str(PCSHOP_DIR))

DATABASES = {
    'default': {
        'NAME': PCSHOP_DIR / 'db.sqlite3',  # shared database
    }
}
```

Static files (CSS theme) are also loaded from `pcshop/static/`.

---

## Management Commands

### PC Shop

```bash
# Seed categories, products, reviews, feedback, and admin user
python manage.py seed_db

# Clear existing data and re-seed
python manage.py seed_db --clear

# Run database migrations
python manage.py migrate
```

### Admin Portal

```bash
# Create or reset the admin portal login (soorya / soorya2006)
python manage.py setup_admin
```

> Database migrations for the shared database are already covered in the setup sections above.

---

## Typical Development Workflow

1. **Start PC Shop** and seed the database if this is a fresh setup:
   ```bash
   cd pcshop
   python manage.py migrate
   python manage.py seed_db
   python manage.py runserver 8000
   ```

2. **Start Admin Portal** in a second terminal:
   ```bash
   cd adminportal
   python manage.py setup_admin
   python manage.py runserver 8001
   ```

3. **Manage content** via the admin portal — add/edit products, moderate reviews, handle feedback.

4. **Verify changes** on the storefront at http://127.0.0.1:8000/ — product updates appear immediately since both apps share the same database.

5. **Register a test customer** at http://127.0.0.1:8000/accounts/register/ to test the user-facing account flow.

---

## URL Quick Reference

| Service | Base URL |
|---------|----------|
| PC Shop storefront | http://127.0.0.1:8000/ |
| PC Shop Django admin | http://127.0.0.1:8000/admin/ |
| Admin Portal | http://127.0.0.1:8001/ |
| Admin Portal login | http://127.0.0.1:8001/login/ |

The PC Shop navbar includes an **ADMIN** link that opens the admin portal at port 8001 in a new tab.

---

## Notes

- **Shared database:** All migrations should be run from `pcshop/` first. The admin portal reads the same `db.sqlite3` file.
- **SQLite limits:** Running both servers simultaneously is fine for development, but SQLite is not ideal for production with concurrent writes. Consider PostgreSQL for production deployment.
- **Mock data:** Cart, checkout, user dashboard order history, and the storefront analytics page (`/admin-dashboard/`) use demo/mock data and are not yet backed by real order models.
- **Product images:** Products can reference a static image name or use an uploaded file stored in `pcshop/media/products/`.
- **Review ratings:** When reviews are approved or deleted in the admin portal, the parent product's average rating and review count are recalculated automatically.
