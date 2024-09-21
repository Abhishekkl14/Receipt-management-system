#!/usr/bin/env python
# coding: utf-8

# In[6]:


import datetime


class Item:
    """Represents a single item in the receipt."""
    
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_total(self) -> float:
        """Calculates the total price for this item."""
        return self.price * self.quantity


class Receipt:
    """Manages a list of items and calculates totals, including tax and discount."""
    
    def __init__(self):
        self.items = []
        self.subtotal = 0.0
        self.discount = 0.0
        self.tax = 0.0
        self.final_total = 0.0

    def add_item(self, name: str, price: float, quantity: int):
        """Adds an item to the receipt."""
        self.items.append(Item(name, price, quantity))

    def calculate_subtotal(self):
        """Calculates the subtotal (sum of all item totals)."""
        self.subtotal = sum(item.get_total() for item in self.items)

    def apply_discount(self, discount_percent: float):
        """Applies a discount to the subtotal."""
        self.discount = (discount_percent / 100) * self.subtotal

    def apply_tax(self, tax_percent: float):
        """Applies tax to the amount after the discount."""
        self.tax = (tax_percent / 100) * (self.subtotal - self.discount)

    def calculate_final_total(self):
        """Calculates the final total by applying discount and tax."""
        self.final_total = (self.subtotal - self.discount) + self.tax

    def generate_receipt(self) -> str:
        """Generates and returns a formatted receipt."""
        receipt_lines = [
            "===== Receipt =====",
            f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\nItems Purchased:"
        ]

        for item in self.items:
            receipt_lines.append(f"{item.name} (x{item.quantity}): ₹{item.get_total():.2f}")

        receipt_lines.append(f"\nSubtotal: ₹{self.subtotal:.2f}")
        receipt_lines.append(f"Discount: -₹{self.discount:.2f}")
        receipt_lines.append(f"Tax: +₹{self.tax:.2f}")
        receipt_lines.append(f"Total: ₹{self.final_total:.2f}")
        receipt_lines.append("===================")

        return "\n".join(receipt_lines)

    def save_receipt(self, filename: str):
        """Saves the receipt to a text file with UTF-8 encoding."""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.generate_receipt())
        print(f"Receipt saved as {filename}")


def get_valid_input(prompt: str, input_type: type):
    """Helper function to ensure valid input from the user."""
    while True:
        try:
            return input_type(input(prompt))
        except ValueError:
            print(f"Invalid input! Please enter a valid {input_type.__name__}.")


def collect_items() -> Receipt:
    """Collects items from the user and returns a populated Receipt object."""
    receipt = Receipt()

    while True:
        name = input("Enter the item name (or type 'done' to finish): ").strip()
        if name.lower() == 'done':
            break

        price = get_valid_input(f"Enter the price of {name} in ₹: ", float)
        quantity = get_valid_input(f"Enter the quantity of {name}: ", int)
        
        receipt.add_item(name, price, quantity)
    
    return receipt


def main():
    print("Welcome to the Receipt Generator!\n")

    # Collecting items
    receipt = collect_items()

    if not receipt.items:
        print("No items added. Exiting...")
        return

    # Collecting discount and tax
    discount_percent = get_valid_input("Enter the discount percentage: ", float)
    tax_percent = get_valid_input("Enter the tax percentage: ", float)

    # Applying discount and tax
    receipt.calculate_subtotal()
    receipt.apply_discount(discount_percent)
    receipt.apply_tax(tax_percent)
    receipt.calculate_final_total()

    # Displaying receipt
    print("\n" + receipt.generate_receipt())

    # Saving receipt option
    save_option = input("Would you like to save the receipt? (yes/no): ").strip().lower()
    if save_option == 'yes':
        filename = input("Enter the filename to save the receipt (e.g., 'receipt.txt'): ").strip()
        if not filename.endswith(".txt"):
            filename += ".txt"
        receipt.save_receipt(filename)
    else:
        print("Receipt not saved.")

    print("Thank you for using the Receipt Generator!")


if __name__ == "__main__":
    main()


# In[ ]:




