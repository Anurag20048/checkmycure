"""
Script to populate the database with sample data
Run: python populate_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Category, Product, Customer, Order, OrderItem
from decimal import Decimal

def populate():
    print("Populating database with sample data...")
    
    # Clear existing data
    print("\n1. Clearing existing data...")
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    Customer.objects.all().delete()
    print("✓ Existing data cleared")
    
    # Create Categories
    print("\n2. Creating categories...")
    categories = [
        {"name": "Electronics", "description": "Electronic devices and accessories"},
        {"name": "Clothing", "description": "Fashion and apparel"},
        {"name": "Books", "description": "Books and literature"},
        {"name": "Home & Kitchen", "description": "Home and kitchen appliances"},
        {"name": "Sports", "description": "Sports and outdoor equipment"},
    ]
    
    created_categories = []
    for cat_data in categories:
        cat = Category.objects.create(**cat_data)
        created_categories.append(cat)
        print(f"  - Created category: {cat.name}")
    
    # Create Products
    print("\n3. Creating products...")
    products_data = [
        {"name": "Laptop", "description": "High-performance laptop for work and gaming", "price": "1299.99", "category": created_categories[0], "stock": 15},
        {"name": "Smartphone", "description": "Latest smartphone with amazing features", "price": "899.99", "category": created_categories[0], "stock": 25},
        {"name": "Wireless Headphones", "description": "Premium noise-canceling headphones", "price": "299.99", "category": created_categories[0], "stock": 40},
        {"name": "T-Shirt", "description": "Comfortable cotton t-shirt", "price": "19.99", "category": created_categories[1], "stock": 100},
        {"name": "Jeans", "description": "Classic denim jeans", "price": "49.99", "category": created_categories[1], "stock": 75},
        {"name": "Running Shoes", "description": "Professional running shoes", "price": "89.99", "category": created_categories[1], "stock": 50},
        {"name": "Python Programming Book", "description": "Learn Python from scratch", "price": "39.99", "category": created_categories[2], "stock": 30},
        {"name": "Science Fiction Novel", "description": "Bestselling sci-fi adventure", "price": "14.99", "category": created_categories[2], "stock": 60},
        {"name": "Coffee Maker", "description": "Automatic coffee brewing machine", "price": "79.99", "category": created_categories[3], "stock": 20},
        {"name": "Blender", "description": "High-speed blender for smoothies", "price": "59.99", "category": created_categories[3], "stock": 35},
        {"name": "Yoga Mat", "description": "Non-slip exercise yoga mat", "price": "24.99", "category": created_categories[4], "stock": 45},
        {"name": "Basketball", "description": "Professional basketball", "price": "29.99", "category": created_categories[4], "stock": 55},
    ]
    
    created_products = []
    for prod_data in products_data:
        prod = Product.objects.create(**prod_data)
        created_products.append(prod)
        print(f"  - Created product: {prod.name}")
    
    # Create Customers
    print("\n4. Creating customers...")
    customers_data = [
        {"name": "John Doe", "email": "john.doe@example.com", "phone": "+1234567890", "address": "123 Main St, New York, NY"},
        {"name": "Jane Smith", "email": "jane.smith@example.com", "phone": "+1234567891", "address": "456 Oak Ave, Los Angeles, CA"},
        {"name": "Bob Johnson", "email": "bob.johnson@example.com", "phone": "+1234567892", "address": "789 Pine Rd, Chicago, IL"},
        {"name": "Alice Williams", "email": "alice.williams@example.com", "phone": "+1234567893", "address": "321 Elm St, Houston, TX"},
        {"name": "Charlie Brown", "email": "charlie.brown@example.com", "phone": "+1234567894", "address": "654 Maple Dr, Phoenix, AZ"},
    ]
    
    created_customers = []
    for cust_data in customers_data:
        cust = Customer.objects.create(**cust_data)
        created_customers.append(cust)
        print(f"  - Created customer: {cust.name}")
    
    # Create Orders
    print("\n5. Creating orders...")
    orders_data = [
        {
            "customer": created_customers[0],
            "status": "delivered",
            "notes": "First order - delivered successfully",
            "items": [
                {"product": created_products[0], "quantity": 1, "price": created_products[0].price},
                {"product": created_products[2], "quantity": 2, "price": created_products[2].price},
            ]
        },
        {
            "customer": created_customers[1],
            "status": "shipped",
            "notes": "Express delivery requested",
            "items": [
                {"product": created_products[1], "quantity": 1, "price": created_products[1].price},
                {"product": created_products[5], "quantity": 1, "price": created_products[5].price},
            ]
        },
        {
            "customer": created_customers[2],
            "status": "processing",
            "notes": "Gift wrapping required",
            "items": [
                {"product": created_products[6], "quantity": 3, "price": created_products[6].price},
                {"product": created_products[7], "quantity": 2, "price": created_products[7].price},
            ]
        },
        {
            "customer": created_customers[3],
            "status": "pending",
            "notes": "Waiting for payment confirmation",
            "items": [
                {"product": created_products[8], "quantity": 1, "price": created_products[8].price},
                {"product": created_products[9], "quantity": 1, "price": created_products[9].price},
            ]
        },
        {
            "customer": created_customers[0],
            "status": "delivered",
            "notes": "Repeat customer - thank you!",
            "items": [
                {"product": created_products[3], "quantity": 5, "price": created_products[3].price},
                {"product": created_products[4], "quantity": 2, "price": created_products[4].price},
            ]
        },
    ]
    
    for order_data in orders_data:
        items_data = order_data.pop('items')
        order = Order.objects.create(**order_data)
        
        total = Decimal('0.00')
        for item_data in items_data:
            order_item = OrderItem.objects.create(order=order, **item_data)
            total += order_item.get_total()
        
        order.total_amount = total
        order.save()
        print(f"  - Created order #{order.id} for {order.customer.name} - Total: ${order.total_amount}")
    
    print("\n" + "="*50)
    print("Database populated successfully!")
    print("="*50)
    print(f"\nSummary:")
    print(f"  Categories: {Category.objects.count()}")
    print(f"  Products: {Product.objects.count()}")
    print(f"  Customers: {Customer.objects.count()}")
    print(f"  Orders: {Order.objects.count()}")
    print(f"  Order Items: {OrderItem.objects.count()}")
    print("\n✓ Ready to use!")

if __name__ == '__main__':
    populate()
