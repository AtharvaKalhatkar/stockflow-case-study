# Part 2: Database Design

## Schema Design

Based on the given requirements, I designed the following tables:

### Company
- id (Primary Key)
- name

### Warehouse
- id (Primary Key)
- company_id (Foreign Key → Company.id)
- name
- location

Each company can have multiple warehouses.

---

### Product
- id (Primary Key)
- name
- sku (Unique)
- price
- threshold

SKU is kept unique across the platform as per requirement.

---

### Inventory
- id (Primary Key)
- product_id (Foreign Key → Product.id)
- warehouse_id (Foreign Key → Warehouse.id)
- quantity

This table handles the relationship between products and warehouses, since a product can exist in multiple warehouses.

---

### Supplier
- id (Primary Key)
- name
- contact_email

---

### ProductSupplier
- id (Primary Key)
- product_id (Foreign Key → Product.id)
- supplier_id (Foreign Key → Supplier.id)

This allows a product to be linked with one or more suppliers.

---

### InventoryLog
- id (Primary Key)
- product_id (Foreign Key)
- warehouse_id (Foreign Key)
- change
- timestamp

Used to track inventory changes over time.

---

### Bundle
- id (Primary Key)
- name

---

### BundleItems
- id (Primary Key)
- bundle_id (Foreign Key → Bundle.id)
- product_id (Foreign Key → Product.id)
- quantity

Used to represent products that are bundles of other products.

---

## Relationships

- One company can have multiple warehouses
- One product can exist in multiple warehouses (handled via Inventory)
- One product can have multiple suppliers
- Bundles contain multiple products

---

## Missing Requirements / Questions

While designing the schema, I identified some missing details:

- Can a product have multiple suppliers or only one primary supplier?
- How is the low stock threshold defined (per product or per warehouse)?
- What exactly counts as "recent sales activity" (time window)?
- Can inventory go negative?
- Do we need soft delete for products or warehouses?
- How frequently will inventory be updated?

---

## Design Decisions

- SKU is marked as UNIQUE to enforce business rules
- Inventory table is used for many-to-many mapping between product and warehouse
- InventoryLog is added to track historical changes
- Indexing should be applied on product_id and warehouse_id for faster queries
