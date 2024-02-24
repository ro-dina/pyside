import layout as l
import sys
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
from layout import MainWindow
# 本体 
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  main_window = MainWindow(app)
  main_window.show()
  sys.exit(app.exec())