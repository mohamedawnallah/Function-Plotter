import sys
import numpy as np
import re
import sympy
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFrame, QFileDialog, QColorDialog, QInputDialog, QScrollArea
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        self.color_button = QPushButton("Change Color")
        self.grid_button = QPushButton("Toggle Gridlines")
        self.legend_button = QPushButton("Toggle Legend")
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
        self.layout.addWidget(self.color_button)
        self.layout.addWidget(self.grid_button)
        self.layout.addWidget(self.legend_button)
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
        self.derivative_button.clicked.connect(self.derivative)
        self.integral_button.clicked.connect(self.integrate)
        self.color_button.clicked.connect(self.change_color)
        self.grid_button.clicked.connect(self.toggle_grid)
        self.legend_button.clicked.connect(self.toggle_legend)
        self.add_function_button.clicked.connect(self.add_function)
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
            QMessageBox.warning(self, "Invalid input", "Please enter a valid number for the minimum and maximum values of x.")
            return

        # Validate function input
        if not re.match("^[0-9x+\-*/^(). ]+$", function_string):
            QMessageBox.warning(self, "Invalid input", "Please enter a valid function of x.")
            return

        # Create x variable and parse function
        x = sympy.Symbol('x')
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
            self.ax.set_xlim(xlim[0] + (self.press[0] - self.release[0]), xlim[1] + (self.press[0] - self.release[0]))
            self.ax.set_ylim(ylim[0] + (self.press[1] - self.release[1]), ylim[1] + (self.press[1] - self.release[1]))
            self.canvas.draw()
    
    def save_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "figures/", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
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
    
    def derivative(self):
        x = sympy.Symbol('x')
        function_str = self.function_input.text()
        function = sympy.parse_expr(function_str.replace("^", "**"))
        derivative = function.diff(x)
        QMessageBox.information(self, "Derivative", f"The derivative of the function is: {derivative}")
    
    def integrate(self):
        x = sympy.Symbol('x')
        function_str = self.function_input.text()
        function = sympy.parse_expr(function_str.replace("^", "**"))
        integral = function.integrate(x)
        QMessageBox.information(self, "Integral", f"The integral of the function is: {integral} + C")

    def change_color(self):
        if not self.ax:
            QMessageBox.warning(self, "Error", "Please plot the function first before changing the color.")
            return
        color = QColorDialog.getColor()
        for line in self.ax.lines:
            line.set_color(color.name())
        self.canvas.draw()
    
    def toggle_grid(self):
        if not self.ax:
            QMessageBox.warning(self, "Error", "Please plot the function first before toggling the grid.")
            return
        if self.grid_visible:
            self.ax.grid(False)
            self.grid_visible = False
        else:
            self.ax.grid(True)
            self.grid_visible = True
        self.canvas.draw()
    
    def toggle_legend(self):
        if not self.ax:
            QMessageBox.warning(self, "Error", "Please plot the function first before toggling the legend.")
            return
        if self.legend_visible:
            self.legend.remove()
            self.legend_visible = False
        else:
            self.legend = self.ax.legend()
            self.legend_visible = True
        self.canvas.draw()
            
    def add_function(self):
        function_string = self.function_input.text()
        function_string = function_string.replace("^", "**")
        try:
            xmin = float(self.xmin_input.text())
            xmax = float(self.xmax_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numbers for the x min and x max.")
            return
        x = np.linspace(xmin, xmax, 1000)
        y = eval(function_string)
        self.ax.plot(x, y)
        self.canvas.draw()
    
    def change_x_label(self):
        if not self.ax:
            QMessageBox.warning(self, "Error", "Please plot the function first before changing the x label.")
            return
        label, ok = QInputDialog.getText(self, 'Change x-axis label', 'Enter new label:')
        if ok:
            self.ax.set_xlabel(label)
            self.canvas.draw()

    def change_y_label(self):
        if not self.ax:
            QMessageBox.warning(self, "Error", "Please plot the function first before changing the y label.")
            return
        label, ok = QInputDialog.getText(self, 'Change y-axis label', 'Enter new label:')
        if ok:
            self.ax.set_ylabel(label)
            self.canvas.draw()
    
    def change_title(self):
        if not self.ax:
            QMessageBox.warning(self, "Error", "Please plot the function first before changing the title.")
            return
        title, ok = QInputDialog.getText(self, 'Change title', 'Enter new title:')
        if ok:
            self.ax.set_title(title)
            self.canvas.draw()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    plotter = FunctionPlotter()
    plotter.show()
    sys.exit(app.exec())
    
