# Assumptions

Due to some incomplete requirements in the case study, I made the following assumptions:

- SKU is unique across the platform
- Each product has a predefined threshold value for low stock
- Recent sales activity is defined as sales within the last 30 days
- A product has at least one supplier (considered primary for simplicity)
- days_until_stockout is estimated and not calculated precisely
- Inventory values cannot be negative
- Each warehouse belongs to a single company
