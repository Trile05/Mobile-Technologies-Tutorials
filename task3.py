import tkinter as tk
from tkinter import messagebox
import time

# === AVL Tree Node ===
class AVLNode:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None
        self.height = 1

# === AVL Tree Class ===
class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        # Rotation
        y.right = z
        z.left = T3
        # Update heights
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        # Rotation
        y.left = z
        z.right = T2
        # Update heights
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def insert(self, node, name, phone):
        # Normal BST insert
        if not node:
            return AVLNode(name, phone)
        if name < node.name:
            node.left = self.insert(node.left, name, phone)
        elif name > node.name:
            node.right = self.insert(node.right, name, phone)
        else:
            # Update phone if name exists
            node.phone = phone
            return node

        # Update height
        node.height = 1 + max(self.height(node.left), self.height(node.right))

        # Check balance
        balance = self.get_balance(node)

        # Left Left
        if balance > 1 and name < node.left.name:
            return self.right_rotate(node)
        # Right Right
        if balance < -1 and name > node.right.name:
            return self.left_rotate(node)
        # Left Right
        if balance > 1 and name > node.left.name:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Right Left
        if balance < -1 and name < node.right.name:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, root, name):
        # Standard BST delete
        if not root:
            return root
        if name < root.name:
            root.left = self.delete(root.left, name)
        elif name > root.name:
            root.right = self.delete(root.right, name)
        else:
            # Node with one or zero children
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            # Node with two children
            temp = self.min_value_node(root.right)
            root.name = temp.name
            root.phone = temp.phone
            root.right = self.delete(root.right, temp.name)

        if root is None:
            return root

        # Update height
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # Check balance
        balance = self.get_balance(root)

        # Left Left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        # Left Right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # Right Right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        # Right Left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, node, name):
        if node is None or node.name == name:
            return node
        if name < node.name:
            return self.search(node.left, name)
        else:
            return self.search(node.right, name)

    def inorder(self, root, res=None):
        if res is None:
            res = []
        if root:
            self.inorder(root.left, res)
            res.append((root.name, root.phone))
            self.inorder(root.right, res)
        return res

# === Tkinter GUI App ===
class AVLApp:
    def __init__(self, master):
        self.tree = AVLTree()
        self.master = master
        master.title("AVL Contact Directory")

        # Input frame
        self.frame = tk.Frame(master)
        self.frame.pack(pady=10)

        tk.Label(self.frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Phone:").grid(row=1, column=0)
        self.phone_entry = tk.Entry(self.frame)
        self.phone_entry.grid(row=1, column=1)

        # Buttons
        self.btn_frame = tk.Frame(master)
        self.btn_frame.pack(pady=5)

        tk.Button(self.btn_frame, text="Insert", command=self.insert_contact).grid(row=0, column=0, padx=5)
        tk.Button(self.btn_frame, text="Search", command=self.search_contact).grid(row=0, column=1, padx=5)
        tk.Button(self.btn_frame, text="Delete", command=self.delete_contact).grid(row=0, column=2, padx=5)
        tk.Button(self.btn_frame, text="Show All", command=self.show_all).grid(row=0, column=3, padx=5)

        # Output text box
        self.output_text = tk.Text(master, height=10, width=60)
        self.output_text.pack(pady=10)

        # Canvas for tree visualization
        self.canvas = tk.Canvas(master, width=800, height=400, bg="white")
        self.canvas.pack(pady=10)

    def insert_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if not name or not phone:
            messagebox.showwarning("Input Error", "Please enter both Name and Phone.")
            return
        self.tree.root = self.tree.insert(self.tree.root, name, phone)
        messagebox.showinfo("Success", f"Inserted/Updated contact: {name}")
        self.clear_entries()
        self.show_all()
        self.draw_tree()

    def search_contact(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter Name to search.")
            return
        node = self.tree.search(self.tree.root, name)
        self.output_text.delete(1.0, tk.END)
        if node:
            self.output_text.insert(tk.END, f"Found Contact:\nName: {node.name}\nPhone: {node.phone}\n")
        else:
            self.output_text.insert(tk.END, "Contact not found.\n")

    def delete_contact(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter Name to delete.")
            return
        self.tree.root = self.tree.delete(self.tree.root, name)
        messagebox.showinfo("Success", f"Deleted contact (if existed): {name}")
        self.clear_entries()
        self.show_all()
        self.draw_tree()

    def show_all(self):
        self.output_text.delete(1.0, tk.END)
        contacts = self.tree.inorder(self.tree.root)
        if not contacts:
            self.output_text.insert(tk.END, "No contacts found.\n")
        else:
            for n, p in contacts:
                self.output_text.insert(tk.END, f"Name: {n}, Phone: {p}\n")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def draw_tree(self):
        self.canvas.delete("all")
        if not self.tree.root:
            return
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self._draw_node(self.tree.root, width // 2, 20, width // 4)

    def _draw_node(self, node, x, y, x_offset):
        if not node:
            return
        radius = 20
        # Draw left subtree + edge
        if node.left:
            x_left = x - x_offset
            y_left = y + 70
            self.canvas.create_line(x, y+radius, x_left, y_left - radius)
            self._draw_node(node.left, x_left, y_left, x_offset // 2)
        # Draw right subtree + edge
        if node.right:
            x_right = x + x_offset
            y_right = y + 70
            self.canvas.create_line(x, y+radius, x_right, y_right - radius)
            self._draw_node(node.right, x_right, y_right, x_offset // 2)
        # Draw node circle
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightgreen")
        # Draw text - shortened name if long
        display_name = node.name if len(node.name) <= 10 else node.name[:10] + "..."
        self.canvas.create_text(x, y, text=display_name, font=("Arial", 10, "bold"))

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AVLApp(root)
    root.mainloop()