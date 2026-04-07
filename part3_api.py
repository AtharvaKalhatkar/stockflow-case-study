from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    alerts = []

    try:
        # Fetch all warehouses for the company
        warehouses = Warehouse.query.filter_by(company_id=company_id).all()

        for warehouse in warehouses:
            inventories = Inventory.query.filter_by(warehouse_id=warehouse.id).all()

            for inventory in inventories:
                product = Product.query.get(inventory.product_id)

                # Check for recent sales (last 30 days)
                recent_sales = Sale.query.filter(
                    Sale.product_id == product.id,
                    Sale.created_at >= datetime.utcnow() - timedelta(days=30)
                ).count()

                if recent_sales == 0:
                    continue

                # Check if stock is below threshold
                if inventory.quantity < product.threshold:

                    supplier_link = ProductSupplier.query.filter_by(product_id=product.id).first()
                    supplier = None

                    if supplier_link:
                        supplier = Supplier.query.get(supplier_link.supplier_id)

                    alert = {
                        "product_id": product.id,
                        "product_name": product.name,
                        "sku": product.sku,
                        "warehouse_id": warehouse.id,
                        "warehouse_name": warehouse.name,
                        "current_stock": inventory.quantity,
                        "threshold": product.threshold,
                        "days_until_stockout": 10,  # estimated value
                        "supplier": {
                            "id": supplier.id if supplier else None,
                            "name": supplier.name if supplier else None,
                            "contact_email": supplier.contact_email if supplier else None
                        }
                    }

                    alerts.append(alert)

        return {
            "alerts": alerts,
            "total_alerts": len(alerts)
        }

    except Exception as e:
        return {"error": str(e)}, 500
