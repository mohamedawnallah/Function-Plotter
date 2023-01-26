from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QFrame,
    QFileDialog,
    QColorDialog,
    QInputDialog,
    QScrollArea,
)
from PySide6.QtCore import Qt, QTimer
import sympy
import numpy as np
import re
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from loguru import logger
from helpers import CustomMessageBox


class FunctionPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_variables()
        self.create_widgets()
        self.create_layout()
        self.set_layout()
        self.connect_signals()

    def init_variables(self):
        self.ax = None
        self.grid_visible = False
        self.legend_visible = False

    def create_widgets(self):
        self.scroll_area = QScrollArea()
        self.function_label = QLabel("Enter a function of x:")
        self.function_input = QLineEdit()
        self.xmin_label = QLabel("Enter the minimum value of x:")
        self.xmin_input = QLineEdit()
        self.xmax_label = QLabel("Enter the maximum value of x:")
        self.xmax_input = QLineEdit()
        self.plot_button = QPushButton("Plot")
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_out_button = QPushButton("Zoom Out")
        self.reset_button = QPushButton("Reset")
        self.save_image_button = QPushButton("Save Image")
        self.derivative_button = QPushButton("Derivative")
        self.integral_button = QPushButton("Integral")
        self.change_color_button = QPushButton("Change Color")
        self.toggle_grid_button = QPushButton("Toggle Gridlines")
        self.toggle_legend_button = QPushButton("Toggle Legend")
        self.add_function_button = QPushButton("Add Function")
        self.x_label_button = QPushButton("Change x-axis label")
        self.y_label_button = QPushButton("Change y-axis label")
        self.title_button = QPushButton("Change title")
        self.cursor_label = QLabel()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(800, 420)

    def create_layout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.function_label)
        self.layout.addWidget(self.function_input)
        self.layout.addWidget(self.xmin_label)
        self.layout.addWidget(self.xmin_input)
        self.layout.addWidget(self.xmax_label)
        self.layout.addWidget(self.xmax_input)
        self.layout.addWidget(self.plot_button)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.title_button)
        self.layout.addWidget(self.x_label_button)
        self.layout.addWidget(self.y_label_button)
        self.layout.addWidget(self.zoom_in_button)
        self.layout.addWidget(self.zoom_out_button)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.save_image_button)
        self.layout.addWidget(self.derivative_button)
        self.layout.addWidget(self.integral_button)
        self.layout.addWidget(self.change_color_button)
        self.layout.addWidget(self.toggle_grid_button)
        self.layout.addWidget(self.toggle_legend_button)
        self.layout.addWidget(self.add_function_button)
        self.layout.addWidget(self.cursor_label)

    def set_layout(self):
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(central_widget)
        self.setCentralWidget(self.scroll_area)
        self.setGeometry(600, 100, 1000, 900)

    def connect_signals(self):
        self.plot_button.clicked.connect(self.plot)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.reset_button.clicked.connect(self.reset_plot)
        self.save_image_button.clicked.connect(self.save_image)
        self.derivative_button.clicked.connect(lambda: self.get_derivative(timeout_seconds=-1))
        self.integral_button.clicked.connect(lambda: self.get_integral(timeout_seconds=10))
        self.change_color_button.clicked.connect(lambda: self.change_color(timeout_seconds=10))
        self.toggle_grid_button.clicked.connect(self.toggle_grid)
        self.toggle_legend_button.clicked.connect(self.toggle_legend)
        self.add_function_button.clicked.connect(lambda: self.add_another_function(timeout_seconds=10))
        self.x_label_button.clicked.connect(self.change_x_label)
        self.y_label_button.clicked.connect(self.change_y_label)
        self.title_button.clicked.connect(self.change_title)
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def plot(self):
        # Get function and x range from user input
        function_string = self.function_input.text()
        try:
            xmin = float(self.xmin_input.text())
            xmax = float(self.xmax_input.text())
        except ValueError:
            error_message = (
                "Please enter a valid number for the minimum and maximum values of x."
            )
            logger.error(error_message)
            QMessageBox.warning(self, "Invalid input", error_message)
            return

        # Validate function input
        if not re.match("^[0-9x+\-*/^(). ]+$", function_string):
            error_message = "Please enter a valid function of x."
            logger.error(error_message)
            QMessageBox.warning(self, "Invalid input", error_message)
            return

        # Create x variable and parse function
        x = sympy.Symbol("x")
        function = sympy.parse_expr(function_string.replace("^", "**"))

        # Create x and y data
        x_data = [xmin + (xmax - xmin) * i / 100 for i in range(101)]
        y_data = [function.subs(x, xi) for xi in x_data]

        # Plot data
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(x_data, y_data, label=function_string)
        self.canvas.draw()

    def zoom_in(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(xlim[0] * 0.9, xlim[1] * 0.9)
        self.ax.set_ylim(ylim[0] * 0.9, ylim[1] * 0.9)
        self.canvas.draw()

    def zoom_out(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(xlim[0] * 1.1, xlim[1] * 1.1)
        self.ax.set_ylim(ylim[0] * 1.1, ylim[1] * 1.1)
        self.canvas.draw()

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        self.press = event.xdata, event.ydata

    def on_release(self, event):
        if self.ax:
            if event.inaxes != self.ax:
                return
            self.release = event.xdata, event.ydata
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            self.ax.set_xlim(
                xlim[0] + (self.press[0] - self.release[0]),
                xlim[1] + (self.press[0] - self.release[0]),
            )
            self.ax.set_ylim(
                ylim[0] + (self.press[1] - self.release[1]),
                ylim[1] + (self.press[1] - self.release[1]),
            )
            self.canvas.draw()

    def save_image(self, file_name=None):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "figures/",
            "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)",
            options=options,
        ) if not file_name else (file_name, None)
        if file_name:
            self.figure.savefig(file_name)

    def reset_plot(self):
        self.figure.clear()
        self.plot()

    def on_motion(self, event):
        if self.ax:
            if event.inaxes != self.ax:
                return
            x, y = event.xdata, event.ydata
            x = round(x, 2)
            y = round(y, 2)
            self.cursor_label.setText(f"x: {x}, y: {y}")

    def get_derivative(self, timeout_seconds=0.001):
        if not self.ax:
            warning_message = (
                "Please plot the function first before finding the derivative."
            )
            CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="No function plotted", message=warning_message, icon=QMessageBox.Warning)
            return
        x = sympy.Symbol("x")
        function_str = self.function_input.text()
        function = sympy.parse_expr(function_str.replace("^", "**"))
        derivative = str(function.diff(x))
        CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="Derivative", message=f"The derivative of the function is: {derivative}", icon=QMessageBox.Information)
        return derivative

    def get_integral(self, timeout_seconds=0.001):
        if not self.ax:
            warning_message = (
                "Please plot the function first before finding the integral."
            )
            CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="No function plotted", message=warning_message, icon=QMessageBox.Warning)
            return
        x = sympy.Symbol("x")
        function_str = self.function_input.text()
        function = sympy.parse_expr(function_str.replace("^", "**"))
        integral = str(function.integrate(x)) + " + C"
        CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="Integral", message=f"The integral of the function is: {integral}", icon=QMessageBox.Information)
        return integral

    def change_color(self, timeout_seconds=0.001, color_input=None):
        if not self.ax:
            warning_message = (
                "Please plot the function first before changing the color."
            )
            CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="Warning", message=warning_message, icon=QMessageBox.Warning)
            return
        color = QColorDialog.getColor() if not color_input else color_input
        for line in self.ax.lines:
            line.set_color(color.name())
        self.canvas.draw()

    def toggle_grid(self, timeout_seconds=0.001):
        if not self.ax:
            warning_message = "Please plot the function first before toggling the grid."
            CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="Warning", message=warning_message, icon=QMessageBox.Warning)
            return
        if self.grid_visible:
            self.ax.grid(False)
            self.grid_visible = False
        else:
            self.ax.grid(True)
            self.grid_visible = True
        self.canvas.draw()

    def toggle_legend(self, timeout_seconds=0.001):
        if not self.ax:
            warning_message = (
                "Please plot the function first before toggling the legend."
            )
            CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="Warning", message=warning_message, icon=QMessageBox.Warning)
            return
        if self.legend_visible:
            self.legend.remove()
            self.legend_visible = False
        else:
            self.legend = self.ax.legend()
            self.legend_visible = True
        self.canvas.draw()
        

    def add_another_function(self, timeout_seconds=0.001):
        if not self.ax:
            warning_message = (
                "Please plot the first function first before adding another function."
            )
            CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="Warning", message=warning_message, icon=QMessageBox.Warning)
            return
        function_string = self.function_input.text()
        function_string = function_string.replace("^", "**")
        try:
            xmin = float(self.xmin_input.text())
            xmax = float(self.xmax_input.text())
        except ValueError as value_error:
            error_message = "Please enter valid numbers for the x min and x max."
            logger.error(error_message + " " + str(value_error))
            CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="Error", message=error_message, icon=QMessageBox.Error)
            return
        x = np.linspace(xmin, xmax, 1000)
        y = eval(function_string)
        self.ax.plot(x, y)
        self.canvas.draw()

    def change_x_label(self, timeout_seconds=0.001, label=None, ok=None):
        if not self.ax:
            warning_message = (
                "Please plot the function first before changing the x label."
            )
            CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="Warning", message=warning_message, icon=QMessageBox.Warning)
            return
        label, ok = QInputDialog.getText(self, "Change x-axis label", "Enter new label:" ) if not (label and ok) else (label,ok)
        if ok:
            self.ax.set_xlabel(label)
            self.canvas.draw()

    def change_y_label(self, timeout_seconds=0.001, label=None, ok=None):
        if not self.ax:
            warning_message = (
                "Please plot the function first before changing the y label."
            )
            CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="Warning", message=warning_message, icon=QMessageBox.Warning)
            return
        label, ok = QInputDialog.getText(self, "Change y-axis label", "Enter new label:" ) if not (label and ok) else (label,ok)

        if ok:
            self.ax.set_ylabel(label)
            self.canvas.draw()

    def change_title(self, timeout_seconds=0.001):
        if not self.ax:
            warning_message = (
                "Please plot the function first before changing the title."
            )
            CustomMessageBox.showWithTimeout(timeout_seconds=timeout_seconds, title="Warning", message=warning_message, icon=QMessageBox.Warning)
            return
        title, ok = QInputDialog.getText(self, "Change title", "Enter new title:")
        if ok:
            self.ax.set_title(title)
            self.canvas.draw()
