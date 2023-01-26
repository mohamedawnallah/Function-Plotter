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
from utils.enums import MessageType
from utils.exceptions import ValidationError
from utils import helpers

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
        self.plot_another_function_button = QPushButton("Plot Another Function")
        self.x_label_button = QPushButton("Change x-axis label")
        self.y_label_button = QPushButton("Change y-axis label")
        self.title_button = QPushButton("Change title")
        self.cursor_label = QLabel()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(800, 420)

    def create_layout(self):
        """Create the layout for the main window."""
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
        self.layout.addWidget(self.plot_another_function_button)
        self.layout.addWidget(self.cursor_label)

    def set_layout(self):
        """Set the layout for the main window."""
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(central_widget)
        self.setCentralWidget(self.scroll_area)
        self.setGeometry(600, 100, 1000, 900)

    def connect_signals(self):
        """Connect signals to slots."""
        self.plot_button.clicked.connect(self.plot)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.reset_button.clicked.connect(self.reset_plot)
        self.save_image_button.clicked.connect(self.save_image)
        self.derivative_button.clicked.connect(self.get_derivative)
        self.integral_button.clicked.connect(self.get_integral)
        self.change_color_button.clicked.connect(self.change_color)
        self.toggle_grid_button.clicked.connect(self.toggle_grid)
        self.toggle_legend_button.clicked.connect(self.toggle_legend)
        self.plot_another_function_button.clicked.connect(self.plot_another_function)
        self.x_label_button.clicked.connect(self.change_x_label)
        self.y_label_button.clicked.connect(self.change_y_label)
        self.title_button.clicked.connect(self.change_title)
        self.canvas.mpl_connect("button_press_event", self.on_press_canvas)
        self.canvas.mpl_connect("button_release_event", self.on_release_canvas)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion_canvas)

    def on_press_canvas(self, event):
        """When the mouse is pressed, record the x and y coordinates."""
        if event.inaxes != self.ax:
            return
        self.press = event.xdata, event.ydata

    def on_release_canvas(self, event):
        """When the mouse is released, record the x and y coordinates and"""
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

    def on_motion_canvas(self, event):
        """When the mouse is moved, update the cursor label"""
        if self.ax:
            if event.inaxes != self.ax:
                return
            x, y = event.xdata, event.ydata
            x = round(x, 2)
            y = round(y, 2)
            self.cursor_label.setText(f"x: {x}, y: {y}")

    def plot(self, message_timeout_seconds=0, is_another_function=False):
        """Plot the function"""
        function_input_text = self.function_input.text()
        xmin_input, xmax_input = self.xmin_input.text(), self.xmax_input.text()
        try:
            function_parsed: sympy.core = helpers.parse_function_string(function_input_text)
            xmin, xmax = helpers.get_x_range(xmin_input, xmax_input)
            x_data, y_data = helpers.get_xy_data(function_parsed, xmin, xmax)
        except ValidationError as validation_error:
            validation_error_message = str(validation_error)
            helpers.show_message(timeout_seconds=message_timeout_seconds, title="Error", message=validation_error_message, message_type=MessageType.ERROR)
            return
        try:
            if not is_another_function:
                self.figure.clear()
                self.ax = self.figure.add_subplot(111)
            self.ax.plot(x_data, y_data, label=function_parsed)
            self.canvas.draw()
        except TypeError as type_error:
            type_error_message = "Please enter a valid function" + "-" + str(type_error)
            helpers.show_message(timeout_seconds=message_timeout_seconds, title="Error", message=type_error_message, message_type=MessageType.ERROR)
            return


    def zoom_in(self, message_timeout_seconds=0):
        """Zoom in"""
        if not self.ax:
            message = "You need to plot a function first to zoom in"
            title = "Zoom in"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return 
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(xlim[0] * 0.9, xlim[1] * 0.9)
        self.ax.set_ylim(ylim[0] * 0.9, ylim[1] * 0.9)
        self.canvas.draw()

    def zoom_out(self, message_timeout_seconds=0):
        """Zoom out"""
        if not self.ax:
            message = "You need to plot a function first to zoom out"
            title = "Zoom out"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return 
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(xlim[0] * 1.1, xlim[1] * 1.1)
        self.ax.set_ylim(ylim[0] * 1.1, ylim[1] * 1.1)
        self.canvas.draw()

    def save_image(self, file_name=None, path="figures/"):
        """Save the image"""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
             path,
            "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)",
            options=options,
        ) if not file_name else (file_name, None)
        if file_name:
            self.figure.savefig(file_name)

    def reset_plot(self, message_timeout_seconds=0):
        """Reset the plot"""
        if not self.ax:
            message = "You need to plot a function first to reset the plot"
            title = "Reset plot"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
        self.figure.clear()
        self.plot()

    def get_derivative(self, message_timeout_seconds=0):
        """Get the derivative of the function"""
        if not self.ax:
            message = "Please plot the function first before finding the derivative."
            title = "No function plotted"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return
        function_str = self.function_input.text()
        function_parsed = helpers.parse_function_string(function_str)
        x = sympy.Symbol("x")
        derivative = str(function_parsed.diff(x))
        helpers.show_message(timeout_seconds=message_timeout_seconds, title="Derivative", message=f"The derivative of the function is: {derivative}", message_type=MessageType.INFORMATION)
        return derivative

    def get_integral(self, message_timeout_seconds=0):
        """Get the integral of the function"""
        if not self.ax:
            message = "Please plot the function first before finding the integral."
            title = "No function plotted"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return
        function_str = self.function_input.text()
        function_parsed = helpers.parse_function_string(function_str)
        x = sympy.Symbol("x")
        integral = str(function_parsed.integrate(x)) + " + C"
        helpers.show_message(timeout_seconds=message_timeout_seconds, title="Integral", message=f"The integral of the function is: {integral}", message_type=MessageType.INFORMATION)
        return integral

    def change_color(self, message_timeout_seconds=0, color_input=None):
        """Change the color of the function"""
        if not self.ax:
            message = "Please plot the function first before changing the color."
            title = "Change Color"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return
        color = QColorDialog.getColor() if not color_input else color_input
        for line in self.ax.lines:
            line.set_color(color.name())
        self.canvas.draw()

    def toggle_grid(self, message_timeout_seconds=0):
        """Toggle the grid"""
        if not self.ax:
            message = "Please plot the function first before toggling the grid."
            title = "Toggle Grid"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return
        if self.grid_visible:
            self.ax.grid(False)
            self.grid_visible = False
        else:
            self.ax.grid(True)
            self.grid_visible = True
        self.canvas.draw()

    def toggle_legend(self, message_timeout_seconds=0):
        """Toggle the legend"""
        if not self.ax:
            message = "Please plot the function first before toggling the legend."
            title = "Toggle Legend"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return
        if self.legend_visible:
            self.legend.remove()
            self.legend_visible = False
        else:
            self.legend = self.ax.legend()
            self.legend_visible = True
        self.canvas.draw()
        
    def plot_another_function(self, message_timeout_seconds=0):
        """Plot another function"""
        if not self.ax:
            message = "Please plot the first function first before adding another function."
            title = "Add Another Function"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return
        self.plot(is_another_function=True)

    def change_x_label(self, message_timeout_seconds=0, label=None, ok=None):
        """Change the x label"""
        if not self.ax:
            message = "Please plot the function first before changing the x label."
            title = "Change x-axis label"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return
        label, ok = QInputDialog.getText(self, "Change x-axis label", "Enter new label:" ) if not (label and ok) else (label,ok)
        if ok:
            self.ax.set_xlabel(label)
            self.canvas.draw()

    def change_y_label(self, message_timeout_seconds=0, label=None, ok=None):
        """Change the y label"""
        if not self.ax:
            message = "Please plot the function first before changing the y label."
            title = "Change y-axis label"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return
        label, ok = QInputDialog.getText(self, "Change y-axis label", "Enter new label:" ) if not (label and ok) else (label,ok)
        if ok:
            self.ax.set_ylabel(label)
            self.canvas.draw()

    def change_title(self, message_timeout_seconds=0):
        """Change the title"""
        if not self.ax:
            message = "Please plot the function first before changing the title."
            title = "Change Title"
            helpers.show_message(timeout_seconds=message_timeout_seconds, title=title, message=message, message_type=MessageType.WARNING)
            return
        title, ok = QInputDialog.getText(self, "Change title", "Enter new title:")
        if ok:
            self.ax.set_title(title)
            self.canvas.draw()
