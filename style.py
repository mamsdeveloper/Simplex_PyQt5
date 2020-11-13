class Style:
    def __init__(self, font_size):
        font = '* {font-family: "Arial", "Helvetica", "sans-serif";   font-size: %dpx;}' % font_size
        self.style = """QMainWindow { background: #808080;}
                QMenuBar { background: #fefefe; border: 3px solid #808080; border-radius: 10px; margin: 5px 5px 0; }
                QMenuBar::item { margin: 3px 15px 0; padding: 1px 4px; background: transparent; border-radius: 4px;}
                QMenuBar::item:selected { background: #e5e5e5;}
                QMenuBar::item:pressed { background: #808080; color: #ffffff;}
                QMenu { background-color: #fefefe; border: 3px solid #808080; border-radius: 10px;}
                QMenu::item { background-color: transparent; border-radius: 10px; margin: 6px;}
                QMenu::item:selected { background-color: #e5e5e5; color: #000000;}
                QPushButton { background: #fefefe; border: 2px solid #fefefe; border-radius: 13px;}
                QPushButton:hover { border: 3px solid #808080;   }
                QPushButton:pressed { background: #808080; border: 3px solid #808080; color: #ffffff;}
                QTabWidget::pane { background: #e5e5e5; border: none;}
                QTabBar::tab { height: 30px;  min-width: 237px; border-top-left-radius: 20px; border-top-right-radius: 20px;}
                QTabBar::tab:selected { background: #e5e5e5;}QTabBar::tab:!selected { background: #fefefe;}
                QTableWidget QTableCornerButton::section { background: rgba(0, 0, 0, 0); border: none;}
                QTableWidget { background: #fefefe; border-radius: 20px; gridline-color: #fefefe; selection-background-color: rgba(0, 0, 0, 0); selection-color: black;}
                QTableWidget::item { background: #ffffff; border: 1px solid #808080; border-radius: 20px; margin: 5px; padding: 10px;}
                QTableWidget::item:selected { background: rgba(0, 0, 0, 0); border: 3px solid #808080; border-radius: 20px;}
                QLineEdit { background: #ffffff; border: 3px solid #ffffff; border-radius: 10px;}
                QHeaderView { border: none; background: rgba(0, 0, 0, 0);}
                QHeaderView::section { background: rgba(0, 0, 0, 0); border: none;}
                QHeaderView::section:horizontal {   }
                QHeaderView::section:vertical { width: 40px; padding-left: 14px;}
                QSlider::groove:vertical { background: red; position: absolute; left: 4px; right: 4px;}
                QSlider::handle:vertical { height: 18px;    background: #fefefe; border: 2px solid #808080; border-radius: 10px; margin: 0 -4px; /* expand outside the groove */}
                QSlider::add-page:vertical { background: #808080;}
                QSlider::sub-page:vertical { background: #fefefe;}
                QCheckBox { margin-left: 40px; spacing: 20px;}
                QCheckBox::indicator  { height: 15px;  width: 15px;   border-radius: 8px;}
                QCheckBox::indicator:checked { border: 3px solid #808080; background: #808080;}
                QCheckBox::indicator:unchecked { border: 3px solid #808080; background: #fefefe;}
                """

        self.style = font+self.style
