
import tkinter as tk
from Observations import VALUE_KEYS

BACKGROUND_COLOR = '#e6e6e6'  # light gray
BUTTON_FONT = ('Serif', 10)
GRAPHS = {'types': ['line', 'bar', 'barh', 'box', 'scatter', 'hist', 'density', 'area'],
          'labels': ['Line', 'Bar', 'Bar Horizontal', 'Box and Whisker', 'Scatter', 'Histogram', 'Density', 'Area']}
OPTIONS = ['Subplots', 'Grid']


class CustomButton:
    def __init__(self, root, name, row):
        self.root = root
        self.name = name
        self.name_label = name.replace('_', ' ')
        self.row = row


class OptionButton(CustomButton):
    def __init__(self, root, name, row):
        super().__init__(root, name, row)
        self.check_var = tk.IntVar()
        self.boolean = False
        self.button = tk.Checkbutton(self.root, text=self.name, variable=self.check_var, bg=BACKGROUND_COLOR, font=BUTTON_FONT, command=self.get_boolean)
        self.button.grid(row=self.row, column=2, pady=5, padx=15, sticky='w')

    def get_boolean(self):
        return not self.check_var.get() == 0


class GraphRadioButton(CustomButton):
    def __init__(self, root, name, name_label, row, var, value):
        super().__init__(root, name, row)
        self.button = tk.Radiobutton(self.root, text=name_label, variable=var, value=value, bg=BACKGROUND_COLOR, font=BUTTON_FONT)
        self.button.grid(row=self.row, column=1, pady=5, padx=15, sticky='w')


class MetricsRadioButton(CustomButton):
    def __init__(self, root, name, row):
        super().__init__(root, name, row)
        self.check_var = tk.IntVar()
        self.button = tk.Checkbutton(self.root, text=self.name_label, variable=self.check_var, state='normal', bg=BACKGROUND_COLOR, font=BUTTON_FONT)
        self.button.grid(row=self.row, column=0, pady=5, padx=15, sticky='w')


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

        # Title
        tk.Label(self.master, text="Weather Data Visualizer", font=('Serif', 26), bg=BACKGROUND_COLOR).grid(row=0, column=0, columnspan=3, pady=15)

        # Headers
        headers = ['Metrics', 'Graph Type', 'Options']
        for label in headers:
            tk.Label(self.master, text=label, font=('Serif', 13), bg=BACKGROUND_COLOR).grid(column=headers.index(label), row=1, padx=15, pady=5, sticky='w')

        # Metrics
        self.metric_buttons = [MetricsRadioButton(self.master, x, VALUE_KEYS['labels'].index(x) + 2) for x in VALUE_KEYS['labels']]

        # Graph Type Buttons
        self.graph_buttons = [GraphRadioButton(self.master, GRAPHS['types'][i], GRAPHS['labels'][i], i + 2, self.graph_var, i) for i in range(0, len(GRAPHS['types']))]

        # Options Buttons
        self.option_buttons = [OptionButton(self.master, option,  OPTIONS.index(option) + 2) for option in OPTIONS]

        # Status Label
        self.status_label = tk.Label(self.master, textvariable=self.status_var, bg=BACKGROUND_COLOR).grid(columnspan=4, row=len(VALUE_KEYS['types']) + 2)

        # Generate Button
        tk.Button(self.master, text='Generate Graph', command=self.generate_pressed, width=25, height=2).grid(row=len(VALUE_KEYS['types']) + 4, padx=15, pady=10, columnspan=4)

        # Footer
        tk.Label(self.master, text="Created by Adam Leppky for METR100 Assignment 2", font=('Serif', 10),
                 bg=BACKGROUND_COLOR).grid(row=len(VALUE_KEYS['types']) + 5, column=0, columnspan=3, pady=15)

    def generate_pressed(self):
        selected_metrics = [metric.name for metric in self.metric_buttons if metric.check_var.get() == 1]
        graph_type = GRAPHS['types'][self.graph_var.get()]
        subplots = self.option_buttons[0].get_boolean()
        grid = self.option_buttons[1].get_boolean()
        print(selected_metrics, graph_type, subplots, grid)


def start_gui():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
