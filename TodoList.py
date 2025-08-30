import tkinter as tk
from tkinter import simpledialog, messagebox, Menu
import json
import os

DATA_FILE = "tasks.json"


# ------------- Data Persistence Layer ----------------
def load_data():
    """Load task lists from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    """Save task lists to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ------------------ Main GUI Class -------------------
class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("✅ Task Manager")
        self.task_lists = load_data()

        # Layout Setup
        self._setup_left_panel()
        self._setup_right_panel()
        self._setup_task_context_menu()

        self.refresh_lists()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ---------------- UI Setup Methods ----------------
    def _setup_left_panel(self):
        """Create the left side panel with task lists."""
        frame_left = tk.Frame(self.root, padx=10, pady=10)
        frame_left.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(frame_left, text="📂 Task Lists").pack()
        self.listbox_lists = tk.Listbox(frame_left, width=25, exportselection=False)
        self.listbox_lists.pack(fill=tk.Y, expand=True)
        self.listbox_lists.bind("<<ListboxSelect>>", self.on_list_select)

        button_frame = tk.Frame(frame_left)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="➕ Add List", command=self.add_list).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="🗑 Delete List", command=self.delete_list).pack(side=tk.LEFT, padx=2)

    def _setup_right_panel(self):
        """Create the right side panel with tasks inside selected list."""
        frame_right = tk.Frame(self.root, padx=10, pady=10)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(frame_right, text="📝 Tasks").pack()
        self.listbox_tasks = tk.Listbox(frame_right, width=50, exportselection=False)
        self.listbox_tasks.pack(fill=tk.BOTH, expand=True)

        # Event bindings
        self.listbox_tasks.bind("<Button-1>", self.on_task_left_click)
        self.listbox_tasks.bind("<Button-2>", self.show_task_menu)  # macOS
        self.listbox_tasks.bind("<Button-3>", self.show_task_menu)  # Windows/Linux

        # Task buttons
        task_btn_frame = tk.Frame(frame_right)
        task_btn_frame.pack(pady=5)
        tk.Button(task_btn_frame, text="➕ Add Task", command=self.add_task).pack(side=tk.LEFT, padx=2)
        tk.Button(task_btn_frame, text="✏️ Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=2)
        tk.Button(task_btn_frame, text="🗑 Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=2)
        tk.Button(task_btn_frame, text="✔ Toggle Complete", command=self.toggle_task_complete).pack(side=tk.LEFT, padx=2)

    def _setup_task_context_menu(self):
        """Create right-click context menu for tasks."""
        self.task_menu = Menu(self.root, tearoff=0)
        self.task_menu.add_command(label="Edit Task ✏️", command=self.edit_task)
        self.task_menu.add_command(label="Delete Task 🗑", command=self.delete_task)
        self.task_menu.add_command(label="Mark Complete/Incomplete ✔", command=self.toggle_task_complete)

    # ---------------- Refresh UI ----------------
    def refresh_lists(self):
        """Reload task lists in the UI."""
        self.listbox_lists.delete(0, tk.END)
        for list_name in self.task_lists.keys():
            self.listbox_lists.insert(tk.END, list_name)
        self.refresh_tasks(clear_selection=True)

    def refresh_tasks(self, clear_selection=False):
        """Reload tasks for the currently selected list."""
        selection = self.listbox_lists.curselection()
        old_task_selection = self.listbox_tasks.curselection()
        self.listbox_tasks.delete(0, tk.END)

        if selection:
            list_name = self.listbox_lists.get(selection[0])
            tasks = self.task_lists.get(list_name, [])
            for task in tasks:
                display = ("✅ " if task.get("done") else "⬜ ") + task["text"]
                self.listbox_tasks.insert(tk.END, display)

            if not clear_selection and old_task_selection and 0 <= old_task_selection[0] < len(tasks):
                self.listbox_tasks.select_set(old_task_selection[0])

    # ---------------- Event Handlers ----------------
    def on_list_select(self, _event=None):
        self.refresh_tasks(clear_selection=True)

    def on_task_left_click(self, event):
        """Ensure correct task selection with mouse click."""
        idx = self.listbox_tasks.nearest(event.y)
        self.listbox_tasks.select_clear(0, tk.END)
        self.listbox_tasks.select_set(idx)
        self.listbox_tasks.activate(idx)
        return "break"

    def show_task_menu(self, event):
        """Show context menu on right-click."""
        idx = self.listbox_tasks.nearest(event.y)
        self.listbox_tasks.select_clear(0, tk.END)
        self.listbox_tasks.select_set(idx)
        self.listbox_tasks.activate(idx)
        try:
            self.task_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.task_menu.grab_release()
        return "break"

    # ---------------- Task/List Management ----------------
    def _get_selected_list(self):
        """Return currently selected list name, or None with error message."""
        selection = self.listbox_lists.curselection()
        if not selection:
            messagebox.showerror("Error", "❌ Please select a list first.")
            return None
        return self.listbox_lists.get(selection[0])

    def _get_selected_task(self):
        """Return (list_name, index) of selected task, or None if invalid."""
        list_name = self._get_selected_list()
        if not list_name:
            return None, None
        selection = self.listbox_tasks.curselection()
        if not selection:
            messagebox.showerror("Error", "❌ Please select a task first.")
            return None, None
        return list_name, selection[0]

    def add_list(self):
        list_name = simpledialog.askstring("Add List", "Enter new list name:")
        if list_name:
            if list_name in self.task_lists:
                messagebox.showerror("Error", f"List '{list_name}' already exists.")
            else:
                self.task_lists[list_name] = []
                self.refresh_lists()

    def delete_list(self):
        list_name = self._get_selected_list()
        if list_name:
            confirm = messagebox.askyesno("Confirm", f"Delete list '{list_name}' and all tasks?")
            if confirm:
                del self.task_lists[list_name]
                self.refresh_lists()

    def add_task(self):
        list_name = self._get_selected_list()
        if list_name:
            task_text = simpledialog.askstring("Add Task", f"New task for '{list_name}':")
            if task_text:
                self.task_lists[list_name].append({"text": task_text, "done": False})
                self.refresh_tasks()

    def delete_task(self):
        list_name, idx = self._get_selected_task()
        if list_name:
            task_text = self.task_lists[list_name][idx]["text"]
            confirm = messagebox.askyesno("Confirm", f"Delete task: '{task_text}'?")
            if confirm:
                del self.task_lists[list_name][idx]
                self.refresh_tasks()

    def edit_task(self):
        list_name, idx = self._get_selected_task()
        if list_name:
            old_text = self.task_lists[list_name][idx]["text"]
            new_text = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=old_text)
            if new_text:
                self.task_lists[list_name][idx]["text"] = new_text
                self.refresh_tasks()

    def toggle_task_complete(self):
        list_name, idx = self._get_selected_task()
        if list_name:
            task = self.task_lists[list_name][idx]
            task["done"] = not task.get("done", False)
            self.refresh_tasks()

    # ---------------- Closing ----------------
    def on_closing(self):
        save_data(self.task_lists)
        self.root.destroy()


# ---------------- Run App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
