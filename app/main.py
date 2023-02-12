import sys
from PySide6.QtWidgets import QApplication
from function_plotter import FunctionPlotter

if __name__ == "__main__":
    app = QApplication(sys.argv)
    plotter = FunctionPlotter()
    plotter.setWindowTitle("Function Plotter")
    plotter.show()
    sys.exit(app.exec())
