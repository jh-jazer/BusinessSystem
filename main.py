import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class ComputerShop:
    def __init__(self, root):
        self.root = root
        self.root.title("Yash Rafael Computer Shop")

        # Configure style for all widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Choosing 'clam' as a theme for more consistent look

        # Center the window on the screen
        window_width = 600
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Special members data (example data)
        self.special_members = {
            "member1": {"id": "member1", "password": "password1", "discount": 0.9, "join_date": "2023-01-01"},
            "member2": {"id": "member2", "password": "password2", "discount": 0.8, "join_date": "2023-02-15"}
        }

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill=tk.BOTH)

        # Tab 1: Calculate Total
        self.tab_calculate = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_calculate, text="Calculate Total")

        # Centering content in Calculate Total tab
        frame_calculate = tk.Frame(self.tab_calculate, bg='light blue')
        frame_calculate.pack(expand=True, fill='both', padx=20, pady=20)

        # Calculate Total section
        self.hours_label = tk.Label(frame_calculate, text="Hours Used:", font=("Arial", 12, "bold"), bg='light blue')
        self.hours_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.hours_entry = tk.Entry(frame_calculate, font=("Arial", 12), width=10)
        self.hours_entry.grid(row=0, column=1, padx=10, pady=10)

        self.member_label = tk.Label(frame_calculate, text="Member ID:", font=("Arial", 12, "bold"), bg='light blue')
        self.member_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.member_entry = tk.Entry(frame_calculate, font=("Arial", 12), width=10)
        self.member_entry.grid(row=1, column=1, padx=10, pady=10)

        self.password_label = tk.Label(frame_calculate, text="Password:", font=("Arial", 12, "bold"), bg='light blue')
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.password_entry = tk.Entry(frame_calculate, show="*", font=("Arial", 12), width=10)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        self.calculate_button = tk.Button(frame_calculate, text="Calculate Total", command=self.calculate_total, font=("Arial", 12, "bold"))
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(frame_calculate, text="Total Amount Payable (₱):", font=("Arial", 12, "bold"), bg='light blue')
        self.result_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)
        self.result_textbox = tk.Text(frame_calculate, height=1, width=10, font=("Arial", 12), state='disabled')
        self.result_textbox.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

        # Tab 2: Special Members List
        self.tab_members_list = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_members_list, text="Special Members List")

        self.special_members_label = tk.Label(self.tab_members_list, text="Special Members", font=("Arial", 14, "bold"))
        self.special_members_label.pack(pady=(10, 5))

        # Listbox to display special members
        self.special_members_listbox = tk.Listbox(self.tab_members_list, height=8, width=50, font=("Arial", 12))
        self.special_members_listbox.pack(padx=10, pady=(0, 10))

        # Populate special members listbox
        self.update_members_listbox()

        # Buttons for update and delete actions
        button_frame = tk.Frame(self.tab_members_list)
        button_frame.pack(pady=10)

        update_button = tk.Button(button_frame, text="Update Password", command=self.update_password, font=("Arial", 12, "bold"))
        update_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(button_frame, text="Delete Member", command=self.delete_member, font=("Arial", 12, "bold"))
        delete_button.grid(row=0, column=1, padx=5)

        # Tab 3: Register Special Member
        self.tab_register = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_register, text="Register Special Member")

        self.register_frame = tk.Frame(self.tab_register)
        self.register_frame.pack(pady=10)

        self.register_label = tk.Label(self.register_frame, text="Register as Special Member:", font=("Arial", 12, "bold"))
        self.register_label.grid(row=0, columnspan=2, pady=(0, 5))

        self.register_id_label = tk.Label(self.register_frame, text="Member ID:", font=("Arial", 12, "bold"))
        self.register_id_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.register_id_entry = tk.Entry(self.register_frame, font=("Arial", 12), width=15)
        self.register_id_entry.grid(row=1, column=1, padx=10, pady=5)

        self.register_password_label = tk.Label(self.register_frame, text="Password:", font=("Arial", 12, "bold"))
        self.register_password_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.register_password_entry = tk.Entry(self.register_frame, show="*", font=("Arial", 12), width=15)
        self.register_password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.register_button = tk.Button(self.register_frame, text="Register", command=self.register_member, font=("Arial", 12, "bold"))
        self.register_button.grid(row=3, column=0, columnspan=2, pady=10)

    def calculate_total(self):
        try:
            hours_used = float(self.hours_entry.get())
            member_id = self.member_entry.get().strip().lower()
            password = self.password_entry.get()

            if member_id in self.special_members and self.special_members[member_id]["password"] == password:
                discount_rate = self.special_members[member_id]["discount"]
            else:
                discount_rate = 1.0  # No discount if not a special member or incorrect password

            total_amount = hours_used * 15 * discount_rate  # Fixed rate of 15 pesos per hour
            
            self.result_textbox.config(state='normal')
            self.result_textbox.delete('1.0', tk.END)
            self.result_textbox.insert(tk.END, f"{total_amount:.2f}")
            self.result_textbox.config(state='disabled')

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for hours used.")

    def update_members_listbox(self):
        self.special_members_listbox.delete(0, tk.END)
        for member_id, member_info in self.special_members.items():
            self.special_members_listbox.insert(tk.END, f"ID: {member_info['id']} - Discount: {member_info['discount']*100}% - Join Date: {member_info['join_date']}")

    def update_password(self):
        selected_index = self.special_members_listbox.curselection()
        if selected_index:
            member_id = self.special_members_listbox.get(selected_index[0]).split()[1]  # Extract member ID from selected item
            new_password = simpledialog.askstring("Update Password", f"Enter new password for member ID '{member_id}':", parent=self.root)
            if new_password:
                self.special_members[member_id]["password"] = new_password
                self.update_members_listbox()
                messagebox.showinfo("Password Updated", f"Password updated successfully for member ID '{member_id}'.")

    def delete_member(self):
        selected_index = self.special_members_listbox.curselection()
        if selected_index:
            member_id = self.special_members_listbox.get(selected_index[0]).split()[1]  # Extract member ID from selected item
            confirm_delete = messagebox.askyesno("Delete Member", f"Are you sure you want to delete member ID '{member_id}'?")
            if confirm_delete:
                del self.special_members[member_id]
                self.update_members_listbox()
                messagebox.showinfo("Member Deleted", f"Member ID '{member_id}' deleted successfully.")

    def register_member(self):
        member_id = self.register_id_entry.get().strip().lower()
        password = self.register_password_entry.get()
        join_date = datetime.now().strftime("%Y-%m-%d")

        if member_id in self.special_members:
            messagebox.showwarning("Member already exists", f"Member ID '{member_id}' already registered as a special member.")
        else:
            # Add member with a 20% discount
            self.special_members[member_id] = {"id": member_id, "password": password, "discount": 0.8, "join_date": join_date}
            messagebox.showinfo("Registration successful", f"Member ID '{member_id}' registered as a special member with a 20% discount.")
            self.update_members_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = ComputerShop(root)
    root.mainloop()
