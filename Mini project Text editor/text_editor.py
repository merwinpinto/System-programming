import tkinter as tk
from tkinter import filedialog

class TextEditorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Editor")


        toolbar = tk.Frame(self.root)
        toolbar.pack(side="top", fill="x")

        cut_button = tk.Button(toolbar, text="Cut", command=self.cut_text)
        cut_button.pack(side="left")
        copy_button = tk.Button(toolbar, text="Copy", command=self.copy_text)
        copy_button.pack(side="left")
        paste_button = tk.Button(toolbar, text="Paste", command=self.paste_text)
        paste_button.pack(side="left")
        undo_button = tk.Button(toolbar, text="Undo", command=self.undo_text)
        undo_button.pack(side="left")
        redo_button = tk.Button(toolbar, text="Redo", command=self.redo_text)
        redo_button.pack(side="left")
        open_button = tk.Button(toolbar, text="Open", command=self.open_file)
        open_button.pack(side="left")
        save_button = tk.Button(toolbar, text="Save", command=self.save_file)
        save_button.pack(side="left")

        self.text_widget = tk.Text(self.root)
        self.text_widget.pack(expand="yes", fill="both")

        self.history = []
        self.history_index = -1

        self.text_widget.bind("<Key>", self.on_text_change)
        self.text_widget.bind("<Control-x>", lambda e: self.cut_text())
        self.text_widget.bind("<Control-c>", lambda e: self.copy_text())
        self.text_widget.bind("<Control-v>", lambda e: self.paste_text())
        self.text_widget.bind("<Control-z>", lambda e: self.undo_text())

    def on_text_change(self, event):
        self.record_change()

    def cut_text(self):
        selected_text = self.text_widget.get("sel.first", "sel.last")
        self.copy_to_clipboard(selected_text)
        self.text_widget.delete("sel.first", "sel.last")
        self.record_change()

    def copy_text(self):
        selected_text = self.text_widget.get("sel.first", "sel.last")
        self.copy_to_clipboard(selected_text)

    def paste_text(self):
        clipboard_text = self.get_clipboard_text()
        self.text_widget.insert("insert", clipboard_text)
        self.record_change()

    def undo_text(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", self.history[self.history_index])

    def redo_text(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", self.history[self.history_index])

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def get_clipboard_text(self):
        return self.root.clipboard_get()

    def record_change(self):
        text = self.text_widget.get("1.0", "end")
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        self.history.append(text)
        self.history_index = len(self.history) - 1

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.text_widget.delete("1.0", "end")
                self.text_widget.insert("1.0", file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.txt')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_widget.get("1.0", "end"))

if __name__ == "__main__":
    app = TextEditorApp()
    app.root.mainloop()