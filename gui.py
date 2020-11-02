
import tkinter as tk
from Observations import VALUE_KEYS
import Observations
import stringcase
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

BACKGROUND_COLOR = '#e6e6e6'  # light gray
BUTTON_FONT = ('Serif', 16)
GRAPHS = {'types': ['bar', 'barh', 'line', 'scatter'],
          'labels': ['Bar', 'Bar Horizontal', 'Line', 'Scatter']}
OPTIONS = ['Grid']


class CustomButton:
    def __init__(self, root, name, row):
        self.root = root
        self.name = name
        self.row = row


class OptionButton(CustomButton):
    def __init__(self, root, name_label, row):
        super().__init__(root, name_label, row)
        self.check_var = tk.IntVar()
        self.boolean = False
        self.button = tk.Checkbutton(self.root, text=self.name, variable=self.check_var, bg=BACKGROUND_COLOR, font=BUTTON_FONT, command=self.get_boolean)
        self.button.grid(row=self.row, column=0, pady=5, padx=15, sticky='w')

    def get_boolean(self):
        return not self.check_var.get() == 0


class GraphRadioButton(CustomButton):
    def __init__(self, root, graph_label, graph_type, row, var, value):
        super().__init__(root, graph_label, row)
        self.graph_type = graph_type
        self.button = tk.Radiobutton(self.root, text=graph_label, variable=var, value=value, bg=BACKGROUND_COLOR, font=BUTTON_FONT)
        self.button.grid(row=self.row, column=2, pady=5, padx=15, sticky='w')


class MetricsCheckButton(CustomButton):
    def __init__(self, root, metric_label, metric_type, row, command):
        super().__init__(root, metric_label, row)
        self.metric_type = metric_type
        self.check_var = tk.IntVar()
        self.button = tk.Checkbutton(self.root, text=metric_label, variable=self.check_var, state='normal', bg=BACKGROUND_COLOR, font=BUTTON_FONT, command=command)
        self.button.grid(row=self.row, column=1, pady=5, padx=15, sticky='w')


class InformationHeading:
    def __init__(self, root, text, row):
        self.label = tk.Label(root, text=text, font=('Serif', 11, 'underline'), bg=BACKGROUND_COLOR).grid(column=0, row=row, padx=15, pady=(5, 0), sticky='sw')


class MainWindow(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.master = master
        self.master.title('Weather Data Visualizer')
        self.master.resizable(width=False, height=False)
        self.master.geometry('+500+100')
        self.master.config(bg=BACKGROUND_COLOR)

        self.graph_var = tk.IntVar()
        self.status_var = tk.StringVar(value='')
        self.postal_code_var = tk.StringVar(value='68516')
        self.postal_code_var.trace("w", lambda name, index, mode, sv=self.postal_code_var: self.input_updated())
        self.country_code_var = tk.StringVar(value='US')
        self.country_code_var.trace("w", lambda name, index, mode, sv=self.country_code_var: self.input_updated())
        self.start_var = tk.StringVar(value='2020-10-10')
        self.start_var.trace("w", lambda name, index, mode, sv=self.start_var: self.input_updated())
        self.end_var = tk.StringVar(value='2020-10-20')
        self.end_var.trace("w", lambda name, index, mode, sv=self.end_var: self.input_updated())

        # Title
        tk.Label(self.master, text="Weather Data Visualizer", font=('Serif', 32, 'bold'), bg=BACKGROUND_COLOR).grid(row=0, column=0, columnspan=4, pady=15)

        # Headers
        headers = ['Information', 'Metrics', 'Graph Type']
        for label in headers:
            tk.Label(self.master, text=label, font=('Serif', 25), bg=BACKGROUND_COLOR).grid(column=headers.index(label), row=1, padx=15, pady=5, sticky='w')

        # Information
        _ = InformationHeading(self.master, 'Postal Code', 2).label
        self.postal_code_entry = tk.Entry(self.master, textvariable=self.postal_code_var, width=15).grid(row=3, column=0, padx=15, pady=5, sticky='nw')
        _ = InformationHeading(self.master, 'Country Code', 4).label
        self.country_code_entry = tk.Entry(self.master, textvariable=self.country_code_var, width=15).grid(row=5, column=0, padx=15, pady=5, sticky='nw')
        _ = InformationHeading(self.master, 'Start Date (YYYY-MM-DD)', 6).label
        self.start_entry = tk.Entry(self.master, textvariable=self.start_var, width=15).grid(row=7, column=0, padx=15, pady=5, sticky='nw')
        _ = InformationHeading(self.master, 'End Date (YYYY-MM-DD)', 8).label
        self.end_entry = tk.Entry(self.master, textvariable=self.end_var, width=15).grid(row=9, column=0, padx=15, pady=5, sticky='nw')

        # Options Buttons
        tk.Label(self.master, text='Options', font=('Serif', 25), bg=BACKGROUND_COLOR).grid(column=0, row=11, padx=15, pady=5, sticky='w')
        self.option_buttons = [OptionButton(self.master, option, OPTIONS.index(option) + 12) for option in OPTIONS]

        # Metrics
        self.metric_buttons = [MetricsCheckButton(self.master, VALUE_KEYS['labels'][i], VALUE_KEYS['types'][i], i + 2, command=self.input_updated) for i in range(0, len(VALUE_KEYS['labels']))]

        # Graph Type Buttons
        self.graph_buttons = [GraphRadioButton(self.master, GRAPHS['labels'][i], GRAPHS['types'][i], i + 2, self.graph_var, i) for i in range(0, len(GRAPHS['types']))]

        # Status Label
        self.status_label = tk.Label(self.master, textvariable=self.status_var, bg=BACKGROUND_COLOR)
        self.status_label.grid(columnspan=4, row=len(VALUE_KEYS['types']) + 2)

        # Generate Button
        tk.Button(self.master, text='Generate Graph', command=self.generate_pressed, width=25, height=2, bg=BACKGROUND_COLOR).grid(row=len(VALUE_KEYS['types']) + 4, padx=15, pady=10, columnspan=4)

        # Footer
        tk.Label(self.master, text="Created by Adam Leppky for METR100 Assignment 2", font=('Serif', 10),
                 bg=BACKGROUND_COLOR).grid(row=len(VALUE_KEYS['types']) + 5, column=0, columnspan=4, pady=15)

    def generate_graph(self, postal_code, country_code, start, end, selected_metrics, graph_type, grid):
        observations = Observations.Observations(postal_code, country_code, start, end)
        figure(num=None, figsize=(18, 6), dpi=80, facecolor='w', edgecolor='k')
        vs_titles = ''
        for metric in selected_metrics:
            title = stringcase.titlecase(metric)
            metric_values = observations.get_values_by_key(metric)
            label = title + ' ' + metric_values['unit_code']
            if graph_type == 'bar':
                plt.bar(metric_values['timestamps'], metric_values['values'], label=label)
            elif graph_type == 'barh':
                plt.barh(metric_values['timestamps'], metric_values['values'], label=label)
            elif graph_type == 'scatter':
                plt.scatter(metric_values['timestamps'], metric_values['values'], label=label)
            else:
                plt.plot(metric_values['timestamps'], metric_values['values'], label=label)

            if vs_titles == '':
                vs_titles += title
            else:
                vs_titles += ' vs. ' + title

        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.title(f"{vs_titles}\n{postal_code}, {country_code}\nFrom {start} to {end}")
        plt.legend()
        plt.grid(grid)
        plt.show()
        self.update_status('Graph Successfully Created!', 'green')

    def generate_pressed(self):
        postal_code = self.postal_code_var.get()
        country_code = self.country_code_var.get()
        start = self.start_var.get()
        end = self.end_var.get()

        selected_metrics = [metric.metric_type for metric in self.metric_buttons if metric.check_var.get() == 1]
        graph_type = GRAPHS['types'][self.graph_var.get()]
        grid = self.option_buttons[0].get_boolean()

        if self.all_filled(selected_metrics):
            try:
                self.generate_graph(postal_code, country_code, start, end, selected_metrics, graph_type, grid)
            except Exception:
                self.update_status('Invalid information.')

    def all_filled(self, selected_metrics):
        if self.postal_code_var.get() == '':
            self.update_status('Please input a postal code.')
            return False
        elif self.country_code_var.get() == '':
            self.update_status('Please input a country code.')
            return False
        elif self.start_var.get() == '':
            self.update_status('Please input a start date.')
            return False
        elif self.end_var.get() == '':
            self.update_status('Please input an end date.')
            return False
        elif not selected_metrics:
            self.update_status('Please select at least one metric.')
            return False
        return True

    def update_status(self, message, color='red'):
        self.status_label.config(fg=color)
        self.status_var.set(message)

    def input_updated(self):
        self.status_var.set('')


def start_gui():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
