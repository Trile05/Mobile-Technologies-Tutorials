import tkinter as tk
from tkinter import messagebox
import time

class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None

class ContactDirectory:
    def __init__(self):
        self.root = None

    def insert(self, root, name, phone):
        if root is None:
            return Contact(name, phone)
        if name < root.name:
            root.left = self.insert(root.left, name, phone)
        elif name > root.name:
            root.right = self.insert(root.right, name, phone)
        else:
            # Update phone if already exists
            root.phone = phone
        return root

    def search(self, root, name):
        if root is None or root.name == name:
            return root
        if name < root.name:
            return self.search(root.left, name)
        else:
            return self.search(root.right, name)

    def find_min(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    def delete(self, root, name):
        if root is None:
            return root
        if name < root.name:
            root.left = self.delete(root.left, name)
        elif name > root.name:
            root.right = self.delete(root.right, name)
        else:
            # Node with one or no child
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            # Node with two children
            temp = self.find_min(root.right)
            root.name = temp.name
            root.phone = temp.phone
            root.right = self.delete(root.right, temp.name)
        return root

    def inorder(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.inorder(root.left, result)
            result.append((root.name, root.phone))
            self.inorder(root.right, result)
        return result

# ---- Tkinter GUI Visualiser ----
class BSTVisualizerApp:
    def __init__(self, root):
        self.directory = ContactDirectory()
        self.root = root
        self.root.title("Contact Directory BST")

        # Top frame for Inputs
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Phone:").grid(row=1, column=0, padx=5)
        self.phone_entry = tk.Entry(frame)
        self.phone_entry.grid(row=1, column=1, padx=5)

        button_frame = tk.Frame(root)
        button_frame.pack()

        self.insert_btn = tk.Button(button_frame, text="Insert Contact", command=self.insert_contact)
        self.insert_btn.grid(row=0, column=0, padx=5)

        self.search_btn = tk.Button(button_frame, text="Search Contact", command=self.search_contact)
        self.search_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = tk.Button(button_frame, text="Delete Contact", command=self.delete_contact)
        self.delete_btn.grid(row=0, column=2, padx=5)

        self.show_all_btn = tk.Button(button_frame, text="Show All Contacts", command=self.show_all)
        self.show_all_btn.grid(row=0, column=3, padx=5)

        self.benchmark_btn = tk.Button(button_frame, text="Run Benchmark", command=self.benchmark)
        self.benchmark_btn.grid(row=0, column=4, padx=5)

        # Area to display contacts
        self.output_text = tk.Text(root, height=10, width=60)
        self.output_text.pack(pady=10)

        # Canvas to visualize BST
        self.canvas = tk.Canvas(root, width=800, height=400, bg='white')
        self.canvas.pack(pady=10)

    # GUI functions
    def insert_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if not name or not phone:
            messagebox.showwarning("Input Error", "Please enter both name and phone number.")
            return
        self.directory.root = self.directory.insert(self.directory.root, name, phone)
        messagebox.showinfo("Success", f"Inserted/Updated contact: {name}")
        self.clear_entries()
        self.show_all()
        self.draw_tree()

    def search_contact(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name to search.")
            return
        node = self.directory.search(self.directory.root, name)
        self.output_text.delete(1.0, tk.END)
        if node:
            self.output_text.insert(tk.END, f"Found Contact:\nName: {node.name}\nPhone: {node.phone}\n")
        else:
            self.output_text.insert(tk.END, "Contact not found.")

    def delete_contact(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name to delete.")
            return
        self.directory.root = self.directory.delete(self.directory.root, name)
        messagebox.showinfo("Success", f"Deleted contact (if existed): {name}")
        self.clear_entries()
        self.show_all()
        self.draw_tree()

    def show_all(self):
        self.output_text.delete(1.0, tk.END)
        contacts = self.directory.inorder(self.directory.root)
        if not contacts:
            self.output_text.insert(tk.END, "No contacts found.\n")
        else:
            for name, phone in contacts:
                self.output_text.insert(tk.END, f"Name: {name}, Phone: {phone}\n")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    # BST Visualization on Canvas
    def draw_tree(self):
        self.canvas.delete("all")
        if not self.directory.root:
            return
        start_x = self.canvas.winfo_width() // 2
        start_y = 20
        level_gap = 70
        node_radius = 20
        self._draw_node(self.directory.root, start_x, start_y, self.canvas.winfo_width() // 4, level_gap, node_radius)

    def _draw_node(self, node, x, y, x_offset, level_gap, radius):
        if node is None:
            return
        # Draw left subtree
        if node.left:
            x_left = x - x_offset
            y_left = y + level_gap
            # line to left child
            self.canvas.create_line(x, y, x_left, y_left)
            self._draw_node(node.left, x_left, y_left, x_offset // 2, level_gap, radius)
        # Draw right subtree
        if node.right:
            x_right = x + x_offset
            y_right = y + level_gap
            # line to right child
            self.canvas.create_line(x, y, x_right, y_right)
            self._draw_node(node.right, x_right, y_right, x_offset // 2, level_gap, radius)
        # Draw the current node (circle with name inside)
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue")
        display_name = node.name if len(node.name) <= 10 else node.name[:10] + "..."
        self.canvas.create_text(x, y, text=display_name)

    # Benchmarking
    def benchmark(self):
        # For benchmarking, generate a large number of random contacts
        import random
        import string
        # Clear any existing contacts
        self.directory.root = None
        N = 1000  # Number of contacts
        names = [''.join(random.choices(string.ascii_lowercase, k=7)) for _ in range(N)]
        phones = [''.join(random.choices(string.digits, k=10)) for _ in range(N)]

        # Benchmark Insertions
        start = time.time()
        for i in range(N):
            self.directory.root = self.directory.insert(self.directory.root, names[i], phones[i])
        insert_time = time.time() - start

        # Benchmark Searches (search half of inserted names + some random)
        search_names = random.sample(names, N//2) + ['notfoundname'] * (N//2)
        start = time.time()
        found_count = 0
        for name in search_names:
            node = self.directory.search(self.directory.root, name)
            if node:
                found_count += 1
        search_time = time.time() - start

        # Benchmark Deletions (delete 100 random contacts)
        delete_names = random.sample(names, 100)
        start = time.time()
        for name in delete_names:
            self.directory.root = self.directory.delete(self.directory.root, name)
        delete_time = time.time() - start

        result_text = (
            f"Benchmark Results (N={N}):\n"
            f"Insertion time: {insert_time:.4f} seconds\n"
            f"Search time (for {len(search_names)} queries, found {found_count}): {search_time:.4f} seconds\n"
            f"Deletion time (for 100 deletions): {delete_time:.4f} seconds\n"
        )
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result_text)
        # Redraw tree after deletions
        self.draw_tree()

if __name__ == "__main__":
    root = tk.Tk()
    app = BSTVisualizerApp(root)
    root.mainloop()