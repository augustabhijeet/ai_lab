class FakeDatabase:
    def __init__(self):
        self.customers = [
            {"id": "1", "name": "Alice", "email": "alice@example.com"},
            {"id": "2", "name": "Bob", "email": "bob@example.com"},
        ]
        
        self.orders = [
            {"id": "1", "customer_id": "1", "product": "Laptop", "amount": 1200},
            {"id": "2", "customer_id": "2", "product": "Phone", "amount": 800},
        ]   
    
    def get_customer(self, key: str, value):
        return next((customer for customer in self.customers if customer.get(key) == value), None)
        return f"Customer with {key}={value} not found"
    
    def get_order(self, key: str, value):
        return next((order for order in self.orders if order.get(key) == value), None)
        return f"Order with {key}={value} not found"