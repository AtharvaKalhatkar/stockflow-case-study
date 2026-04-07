# Part 1: Code Review & Debugging

## Issues Identified

### 1. No Input Validation
The code directly accesses fields like `data['name']`, `data['sku']`, etc.  
If any field is missing in the request, it will raise an error.

**Impact:**  
This can lead to API crashes (500 errors) instead of proper client error responses.

---

### 2. No Transaction Handling
The product is committed to the database before creating the inventory.  
If the inventory creation fails, the product will still exist.

**Impact:**  
This results in inconsistent data (product without inventory).

---

### 3. SKU Uniqueness Not Checked
There is no check to ensure that the SKU is unique.

**Impact:**  
Duplicate SKUs can break business logic and create confusion in product identification.

---

### 4. Multiple Commits
The code uses two separate `commit()` calls.

**Impact:**  
If the second operation fails, the first one is already saved, leading to partial data.  
It also reduces performance due to unnecessary database operations.

---

### 5. No Error Handling
There is no try-except block to handle exceptions.

**Impact:**  
Any runtime error will crash the application without a meaningful response.

---

### 6. Price Handling
The price is taken directly from input without ensuring proper decimal handling.

**Impact:**  
Using floating point values can lead to precision issues in financial data.

---

### 7. Business Logic Issue (Warehouse Handling)
The code assumes a product belongs to a single warehouse, but the requirement states that products can exist in multiple warehouses.

**Impact:**  
This limits scalability and does not align with the system design requirements.

---

### 8. No Validation for Quantity
The code does not check if `initial_quantity` is valid (e.g., negative values).

**Impact:**  
Invalid inventory data can be stored.

---

## Corrected Code

```python
from decimal import Decimal
from flask import request

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    try:
        # Validate required fields
        required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400

        # Validate quantity
        if data['initial_quantity'] < 0:
            return {"error": "Quantity cannot be negative"}, 400

        # Check SKU uniqueness
        existing_product = Product.query.filter_by(sku=data['sku']).first()
        if existing_product:
            return {"error": "SKU already exists"}, 400

        # Create product
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=Decimal(str(data['price']))
        )

        db.session.add(product)
        db.session.flush()  # Get product ID before commit

        # Create inventory
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=data['initial_quantity']
        )

        db.session.add(inventory)

        # Single commit for atomic operation
        db.session.commit()

        return {
            "message": "Product created",
            "product_id": product.id
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
