class CustomerManager:
    def __init__(self):
        self.customers = {}
        self.tax_rate = 0.2
        self.tax_threshold = 100
        self.discount_threshold = 500
        self.priority_threshold = 800
        self.vip_threshold = 1000
        self.potential_discount_threshold = 300

    def add_customer(self, name, purchases):
        if name in self.customers:
            self.customers[name].extend(purchases)
        else:
            self.customers[name] = purchases

    def add_purchase(self, name, purchase):
        self.add_customer(name, [purchase])

    def add_purchases(self, name, purchases):
        self.add_customer(name, purchases)

    def calculate_total_with_tax(self, purchases):
        total = 0
        for purchase in purchases:
            price = purchase['price']
            if price > self.tax_threshold:
                total += price * (1 + self.tax_rate)
            else:
                total += price
        return total

    def get_customer_status(self, total_amount):
        status = []
        
        if total_amount > self.discount_threshold:
            status.append("Eligible for discount")
        elif total_amount > self.potential_discount_threshold:
            status.append("Potential future discount customer")
        else:
            status.append("No discount")

        if total_amount > self.vip_threshold:
            status.append("VIP Customer!")
        elif total_amount > self.priority_threshold:
            status.append("Priority Customer")
            
        return status

    def generate_report(self):
        for customer_name, purchases in self.customers.items():
            total_amount = self.calculate_total_with_tax(purchases)
            print(customer_name)
            
            for status in self.get_customer_status(total_amount):
                print(status)

    def calculate_shipping_fee(self, purchases):
        if any(purchase.get('weight', 0) > 20 for purchase in purchases):
            return 50
        return 20

def calculate_shipping_fee_for_heavy_items(purchases):
    if any(purchase.get('weight', 0) > 20 for purchase in purchases):
        return 50
    return 20

def calculate_shipping_fee_for_fragile_items(purchases):
    if any(purchase.get('fragile', False) for purchase in purchases):
        return 60
    return 25

flat_tax = 0.2