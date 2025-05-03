import unittest
import io
import contextlib

from main import CustomerManager, calculate_shipping_fee_for_fragile_items, calculate_shipping_fee_for_heavy_items

class TestCustomerManager(unittest.TestCase):

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase]},
            cm.customers
        )

    def test_discount_eligibility(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 600}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Eligible for discount", output)

    def test_heavy_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 100, 'weight': 25}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 50)

    def test_fragile_item_shipping_fee(self):
        purchases = [{'price': 70, 'fragile': True}]

        fee = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee, 60)

    def test_no_special_items_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 40, 'weight': 5, 'fragile': False}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 20)

        fee_fragile = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee_fragile, 25)

    def test_add_purchases(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_purchases(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_generate_report_middle_range(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 400}])  # Total amount between 300-500

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("Potential future discount customer", output)

    def test_generate_report_priority_customer(self):
        cm = CustomerManager()
        # Test case for amount that will be between 800 and 1000 after tax
        cm.add_customer("Bob", [{'price': 750}])  # After tax: 900 (between 800-1000)

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("Priority Customer", output)
        self.assertNotIn("VIP Customer!", output)
        self.assertIn("Eligible for discount", output)

    def test_calculate_shipping_fee_for_heavy_items(self):
        purchases = [{'price': 100, 'weight': 25}]
        fee = calculate_shipping_fee_for_heavy_items(purchases)
        self.assertEqual(fee, 50)

        purchases = [{'price': 100, 'weight': 15}]
        fee = calculate_shipping_fee_for_heavy_items(purchases)
        self.assertEqual(fee, 20)

    def test_generate_report_no_discount(self):
        cm = CustomerManager()
        # Test case for amount less than 300 (no tax, no discount)
        cm.add_customer("Bob", [{'price': 50}])

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("No discount", output)

    def test_generate_report_below_tax_threshold(self):
        cm = CustomerManager()
        # Test case for amount below tax threshold but above 300
        cm.add_customer("Bob", [{'price': 90}, {'price': 90}, {'price': 90}, {'price': 90}])  # Total 360, no tax

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("Potential future discount customer", output)

    def test_generate_report_non_vip_customer(self):
        cm = CustomerManager()
        # Test case for amount between 300 and 800 (not Priority, not VIP)
        cm.add_customer("Bob", [{'price': 600}])  # After tax: 720

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertNotIn("Priority Customer", output)
        self.assertNotIn("VIP Customer!", output)
        self.assertIn("Eligible for discount", output)

    def test_generate_report_between_discount_and_priority(self):
        cm = CustomerManager()
        # Test case for amount between discount threshold and priority threshold
        cm.add_customer("Bob", [{'price': 550}])  # After tax: 660 (between 500 and 800)

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("Eligible for discount", output)
        self.assertNotIn("Priority Customer", output)
        self.assertNotIn("VIP Customer!", output)

    def test_generate_report_small_amount(self):
        cm = CustomerManager()
        # Test case for very small amount (no tax, no discount, no priority)
        cm.add_customer("Bob", [{'price': 80}])  # Below tax threshold and all other thresholds

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("No discount", output)
        self.assertNotIn("Priority Customer", output)
        self.assertNotIn("VIP Customer!", output)

    def test_generate_report_exact_priority_customer(self):
        cm = CustomerManager()
        # Test case for amount exactly at priority threshold
        cm.add_customer("Bob", [{'price': 850}])  # After tax: 1020 (above 1000)
        cm.add_customer("Alice", [{'price': 700}])  # After tax: 840 (between 800-1000)

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("Priority Customer", output)
        self.assertIn("VIP Customer!", output)
        self.assertIn("Eligible for discount", output)

if __name__ == "__main__":
    unittest.main()
