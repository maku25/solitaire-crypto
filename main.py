import sys
from PyQt5.QtWidgets import QApplication
from interface import Fenetre

def main():
    app = QApplication(sys.argv)
    
    fenetre = Fenetre()
    fenetre.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()