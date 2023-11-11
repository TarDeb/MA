import sys
from PyQt5.QtWidgets import QApplication
from ui import IntegratedApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IntegratedApp()
    window.show()
    sys.exit(app.exec_())

