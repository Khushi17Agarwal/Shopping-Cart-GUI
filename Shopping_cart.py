import tkinter as tk
from tkinter import messagebox
import pickle

class ShoppingCartGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Cart")
        self.root.geometry("800x600")

        self.cart = {}  # Dictionary to store items (item: quantity)
        self.item_data = {
            "Apples": {"Product ID": 101, "Price": 1.0, "Expected Delivery": "2 days", "Availability": "In stock"},
            "Bananas": {"Product ID": 102, "Price": 0.5, "Expected Delivery": "3 days", "Availability": "In stock"},
            "Oranges": {"Product ID": 103, "Price": 0.75, "Expected Delivery": "4 days", "Availability": "Out of stock"},
            "Strawberries": {"Product ID": 104, "Price": 2.5, "Expected Delivery": "2 days", "Availability": "In stock"},
            "Grapes": {"Product ID": 105, "Price": 2.0, "Expected Delivery": "3 days", "Availability": "In stock"},
            "Mangoes": {"Product ID": 106, "Price": 1.8, "Expected Delivery": "2 days", "Availability": "In stock"},
            "Pineapples": {"Product ID": 107, "Price": 2.5, "Expected Delivery": "3 days", "Availability": "In stock"},
            "Blueberries": {"Product ID": 108, "Price": 3.0, "Expected Delivery": "2 days", "Availability": "In stock"},
            "Peaches": {"Product ID": 109, "Price": 1.5, "Expected Delivery": "3 days", "Availability": "In stock"},
            "Kiwis": {"Product ID": 110, "Price": 2.2, "Expected Delivery": "4 days", "Availability": "In stock"},
        }

        # Create a mapping of lowercased item names to original item names
        self.item_data_normalized = {item.lower(): item for item in self.item_data.keys()}

        # Define a custom color scheme
        self.bg_color = "#f7f7f7"
        self.button_color = "#4CAF50"
        self.label_color = "#333333"

        # Create a frame for better organization
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(fill=tk.BOTH, expand=True)

        # Labels
        available_items_label = tk.Label(frame, text="Available Items", bg=self.bg_color, fg=self.label_color, font=("Helvetica", 16))
        available_items_label.pack(pady=(20, 10))

        for item, data in self.item_data.items():
            label_text = f"{item} | Price: ${data['Price']:.2f} | Availability: {data['Availability']}"
            item_label = tk.Label(frame, text=label_text, bg=self.bg_color, font=("Helvetica", 12))
            item_label.pack()

        # Entry fields
        select_item_label = tk.Label(frame, text="Select an item:", bg=self.bg_color, font=("Helvetica", 12))
        select_item_label.pack(pady=(10, 0))
        self.item_var = tk.StringVar()
        item_entry = tk.Entry(frame, textvariable=self.item_var, font=("Helvetica", 12))
        item_entry.pack()

        quantity_label = tk.Label(frame, text="Quantity:", bg=self.bg_color, font=("Helvetica", 12))
        quantity_label.pack(pady=(10, 0))
        self.quantity_var = tk.IntVar()
        quantity_entry = tk.Entry(frame, textvariable=self.quantity_var, font=("Helvetica", 12))
        quantity_entry.pack()

        # Buttons
        add_button = tk.Button(frame, text="Add to Cart", command=self.add_to_cart, bg=self.button_color, fg="white", font=("Helvetica", 12))
        add_button.pack(pady=10, padx=10, side=tk.LEFT)

        remove_button = tk.Button(frame, text="Remove from Cart", command=self.remove_from_cart, bg=self.button_color, fg="white", font=("Helvetica", 12))
        remove_button.pack(pady=10, padx=10, side=tk.LEFT)

        update_button = tk.Button(frame, text="Update Quantity", command=self.update_quantity, bg=self.button_color, fg="white", font=("Helvetica", 12))
        update_button.pack(pady=10, padx=10, side=tk.LEFT)

        view_cart_button = tk.Button(frame, text="View Cart", command=self.view_cart, bg=self.button_color, fg="white", font=("Helvetica", 12))
        view_cart_button.pack(pady=10, padx=10, side=tk.LEFT)

        checkout_button = tk.Button(frame, text="Checkout", command=self.checkout, bg=self.button_color, fg="white", font=("Helvetica", 12))
        checkout_button.pack(pady=10, padx=10, side=tk.LEFT)

        save_button = tk.Button(frame, text="Save Cart", command=self.save_cart, bg=self.button_color, fg="white", font=("Helvetica", 12))
        save_button.pack(pady=10, padx=10, side=tk.LEFT)

        load_button = tk.Button(frame, text="Load Cart", command=self.load_cart, bg=self.button_color, fg="white", font=("Helvetica", 12))
        load_button.pack(pady=10, padx=10, side=tk.LEFT)

        clear_button = tk.Button(frame, text="Clear Cart", command=self.clear_cart, bg=self.button_color, fg="white", font=("Helvetica", 12))
        clear_button.pack(pady=10, padx=10, side=tk.LEFT)

        # Label to display the total count in the cart
        self.total_count_label = tk.Label(frame, text="Total Items in Cart: 0", bg=self.bg_color, fg=self.label_color, font=("Helvetica", 12))
        self.total_count_label.pack(pady=(10, 20))

        # Search functionality
        search_label = tk.Label(frame, text="Search Items:", bg=self.bg_color, font=("Helvetica", 12))
        search_label.pack(pady=(10, 0))
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(frame, textvariable=self.search_var, font=("Helvetica", 12))
        search_entry.pack()
        search_button = tk.Button(frame, text="Search", command=self.search_items, bg=self.button_color, fg="white", font=("Helvetica", 12))
        search_button.pack(pady=10, padx=10)

    def add_to_cart(self):
        item = self.item_var.get().lower()
        quantity = self.quantity_var.get()
        if item in self.item_data_normalized:
            original_item_name = self.item_data_normalized[item]
            if self.item_data[original_item_name]['Availability'] == "Out of stock":
                messagebox.showerror("Error", f"{original_item_name} is out of stock and cannot be added to the cart.")
            else:
                if original_item_name in self.cart:
                    self.cart[original_item_name] += quantity
                else:
                    self.cart[original_item_name] = quantity
                messagebox.showinfo("Added to Cart", f"Added {quantity} {original_item_name} to the cart.")
                self.update_total_count()
        else:
            messagebox.showerror("Error", "Item not found in available items.")

    def remove_from_cart(self):
        item = self.item_var.get().lower()
        quantity = self.quantity_var.get()
        if item in self.item_data_normalized:
            original_item_name = self.item_data_normalized[item]
            if original_item_name in self.cart:
                if quantity >= self.cart[original_item_name]:
                    del self.cart[original_item_name]
                else:
                    self.cart[original_item_name] -= quantity
                messagebox.showinfo("Removed from Cart", f"Removed {quantity} {original_item_name} from the cart.")
                self.update_total_count()
            else:
                messagebox.showerror("Error", "Item not found in the cart.")
        else:
            messagebox.showerror("Error", "Item not found in the cart.")

    def update_quantity(self):
        item = self.item_var.get().lower()
        quantity = self.quantity_var.get()
        if item in self.item_data_normalized:
            original_item_name = self.item_data_normalized[item]
            if original_item_name in self.cart:
                self.cart[original_item_name] = quantity
                messagebox.showinfo("Updated Quantity", f"Updated {original_item_name} quantity to {quantity}.")
                self.update_total_count()
            else:
                messagebox.showerror("Error", "Item not found in the cart.")
        else:
            messagebox.showerror("Error", "Item not found in the cart.")

    def update_total_count(self):
        total_items = sum(self.cart.values())
        self.total_count_label.config(text=f"Total Items in Cart: {total_items}")

    def view_cart(self):
        cart_text = "Shopping Cart:\n"
        for item, quantity in self.cart.items():
            cart_text += f"{item}: {quantity}\n"
        if not self.cart:
            cart_text = "Your shopping cart is empty."
        messagebox.showinfo("View Cart", cart_text)

    def checkout(self):
        total_cost = sum(self.item_data[item]['Price'] * quantity for item, quantity in self.cart.items())
        cart_items = "\n".join([f"{item}: {quantity}" for item, quantity in self.cart.items()])
        checkout_message = f"Items in Cart:\n{cart_items}\n\nTotal Cost: ${total_cost:.2f}"
        messagebox.showinfo("Checkout", checkout_message)

    def save_cart(self):
        with open('cart.pkl', 'wb') as f:
            pickle.dump(self.cart, f)
        messagebox.showinfo("Save Cart", "Cart saved successfully.")

    def load_cart(self):
        try:
            with open('cart.pkl', 'rb') as f:
                self.cart = pickle.load(f)
            self.update_total_count()
            messagebox.showinfo("Load Cart", "Cart loaded successfully.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved cart found.")

    def clear_cart(self):
        self.cart.clear()
        self.update_total_count()
        messagebox.showinfo("Clear Cart", "Cart cleared.")

    def search_items(self):
        search_query = self.search_var.get().lower()
        search_results = [item for item in self.item_data if search_query in item.lower()]
        search_text = "Search Results:\n" + "\n".join(search_results) if search_results else "No items found."
        messagebox.showinfo("Search Results", search_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingCartGUI(root)
    root.mainloop()
