import sys
from PyQt5.QtWidgets import QApplication
from integrated_app import IntegratedApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IntegratedApp()
    window.setGeometry(250, 100, 1400, 800)
    window.show()
    sys.exit(app.exec_())
