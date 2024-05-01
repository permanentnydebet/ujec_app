import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from data.data_processor import DataProcessor

class App:
    def __init__(self):
        self.data_processor = DataProcessor()

        # window
        self.root = tk.Tk()
        self.root.title("Ujec App")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # #sets of checkboxes
        self.checkboxes = []
        self.create_widgets()

    def on_checkbox_change():
    # This function will be called whenever a checkbox is clicked
        pass

    def on_scroll(self, *args):
        self.canvas.yview(*args)

    def create_widgets(self):
        # GUI elements
        self.load_button = tk.Button(self.root, text="Wczytaj plik", command=self.load_file)
        self.load_button.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        self.canvas = tk.Canvas(self.root, width=700)
        self.canvas.grid(column=0, row=1, sticky="nsew")

        self.canvas2 = tk.Canvas(self.root, height=700)
        self.canvas2.grid(column=1, row=1, sticky="nsew")

        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.on_scroll)
        scrollbar.grid(column=0, row=1, sticky="nse")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # # Create a frame inside the canvas
        self.frame_checkbox = tk.Frame(self.canvas, width=100, height=100)
        self.canvas.create_window((5, 5), window=self.frame_checkbox, anchor='nw')

        frame_temp = tk.Frame(self.canvas2, height=600)
        self.canvas2.create_window((5, 5), window=frame_temp, anchor='nw')

        #################### Try ##########################3

        self.file_name_var = tk.StringVar()
        self.file_name_label = tk.Label(frame_temp, textvariable=self.file_name_var)
        self.file_name_label.grid(column=0, row=0, sticky="we", padx=5, pady=5)

        # settings
        self.settings_label = tk.Label(frame_temp, text="Ustawienia:")
        self.settings_label.grid(column=0, row=1, sticky="we", padx=5, pady=5)

        # min time
        self.min_time_label_var = tk.StringVar()
        self.min_time_label_var.set('Min time:')
        self.min_time_label = tk.Label(frame_temp, textvariable=self.min_time_label_var)
        self.min_time_label.grid(column=0, row=2, sticky="we", padx=5, pady=5)

        self.min_time_entry_var = tk.StringVar()
        self.min_time_entry = tk.Entry(frame_temp, textvariable=self.min_time_entry_var, state="disabled")
        self.min_time_entry.grid(column=0, row=3, sticky="we", padx=5, pady=5)

        # max time
        self.max_time_label_var = tk.StringVar()
        self.max_time_label_var.set('Max time:')
        self.max_time_label = tk.Label(frame_temp, textvariable=self.max_time_label_var)
        self.max_time_label.grid(column=0, row=4, sticky="we", padx=5, pady=5)

        self.max_time_entry_var = tk.StringVar()
        self.max_time_entry = tk.Entry(frame_temp, textvariable=self.max_time_entry_var, state="disabled")
        self.max_time_entry.grid(column=0, row=5, sticky="we", padx=5, pady=5)

        # average time
        self.avg_time_label = tk.Label(frame_temp, text="Czas uśredniania: [Sekundy]")
        self.avg_time_label.grid(column=0, row=6, sticky="we", padx=5, pady=5)

        self.avg_time_entry_var = tk.StringVar()
        self.avg_time_entry = tk.Entry(frame_temp, textvariable=self.avg_time_entry_var, state="disabled")
        self.avg_time_entry.grid(column=0, row=7, sticky="we", padx=5, pady=5)

        # save button
        self.save_button = tk.Button(frame_temp, text="Zapisz", command=self.save_time, state="disabled")
        self.save_button.grid(column=0, row=8, padx=5, pady=5)

        self.plot_button = tk.Button(frame_temp, text="Rysuj", command=self.plot, state="disabled")
        self.plot_button.grid(column=0, row=9, padx=5, pady=5)

        self.unselect = tk.Button(frame_temp, text="Odznacz wszystkie", command=self.deselect_all, state="disabled")
        self.unselect.grid(column=0, row=10, padx=5, pady=5)

        self.frame_settings = frame_temp

        ################# end try ###############

        # self.populate_frame(frame)

        self.frame_checkbox.update_idletasks()
        self.frame_settings.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save_time(self):
        new_start_time = self.min_time_entry.get()
        new_stop_time = self.max_time_entry.get()

        new_average_time = self.avg_time_entry.get()

        if self.data_processor.change_start_time(new_start_time) is not True:
            self._show_warning("Podano zły czas początku!")
            return

        if self.data_processor.change_stop_time(new_stop_time) is not True:
            self._show_warning("Podano zły czas końca!")
            return

        if new_average_time == "":
            new_average_time = 0

        if self.data_processor.change_resample(int(new_average_time)) is not True:
            self._show_warning("Czas uśredniania nie może być ujemny!!")
            return

        self._show_info("Zapisano!")

    def clear_default_text(self, event):
        # Get the widget that currently has focus
        focused_widget = self.root.focus_get()

        if focused_widget == self.start_text:
            print("Start Text is focused")
            # Your logic for Start Text focus
        elif focused_widget == self.stop_text:
            print("Stop Text is focused")
            # Your logic for Stop Text focus

    def on_focus_out(self, event):
        # Get the widget that currently has focus
        focused_widget = self.root.focus_get()

        if focused_widget == self.start_text:
            print("Start Text is focused out")
            # Your logic for Start Text focus
        elif focused_widget == self.stop_text:
            print("Stop Text is focused out")
            # Your logic for Stop Text focus

    def _show_warning(self, text):
        messagebox.showwarning("Error", text)

    def _show_info(self, text):
        messagebox.showinfo("Info", text)

    def create_checkboxes(self, frame, labels):
        num_checkboxes = len(labels)
        print("num=", num_checkboxes)

        self.frame_checkbox.config(width=100, height=25*num_checkboxes)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Create specified number of Checkbuttons with labels and add them to the list
        for i in range(num_checkboxes):
            checkbox_var = tk.BooleanVar()
            checkbox = tk.Checkbutton(frame, text=labels[i], variable=checkbox_var, command=lambda i=i: self.checkbox_changed(i), )
            checkbox.grid(row=i, column=0, sticky="w")
            self.checkboxes.append((checkbox, checkbox_var))
        return num_checkboxes

    def checkbox_changed(self, index):
        # This function will be called when a checkbox state changes
        checkbox, checkbox_var = self.checkboxes[index]
        if checkbox_var.get():
            print(f"{checkbox['text']} selected!")
        else:
            print(f"{checkbox['text']} deselected.")

    def clear_checkboxes(self):
        self.checkboxes = []

        for widget in self.frame_checkbox.winfo_children():
            widget.destroy()

        self.frame_settings.update_idletasks()


    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data_processor.process_file(file_path)
            # Pobierz nazwę pliku i pomiary
            file_name = file_path.split("/")[-1]
            measurements_names = self.data_processor.get_measuement_name()

            self.clear_checkboxes()

            self.create_checkboxes(self.frame_checkbox, measurements_names)  # Specify the number of checkboxes

            self.min_time_entry.config(state="normal")
            self.max_time_entry.config(state="normal")
            self.avg_time_entry.config(state="normal")

            self.save_button.config(state="active")
            self.plot_button.config(state="active")
            self.unselect.config(state="active")

            start, stop = self.data_processor.get_time()

            self.file_name_var.set(file_name)
            self.min_time_label_var.set("Min time:" + str(start))
            self.max_time_label_var.set("Max time:" + str(stop))

            self.min_time_entry_var.set(str(start))
            self.max_time_entry_var.set(str(stop))
            self.frame_settings.update_idletasks()

    def plot(self):
        to_plot = []

        for check in self.checkboxes:
            checkbox, checkbox_var = check
            if checkbox_var.get():
                to_plot.append(checkbox['text'])

        if len(to_plot) == 0:
            self._show_warning("Wybierz pomiar do wyrysowania!")
            return


        print("to plot list: ", to_plot)
        self.data_processor.plot(to_plot)

    def deselect_all(self):
        for check in self.checkboxes:
            checkbox, checkbox_var = check
            checkbox_var.set(0)


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()