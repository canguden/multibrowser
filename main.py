import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class UrlLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

        self.setPlaceholderText("Search or enter address")
        self.setStyleSheet("QLineEdit { background-color: white; border: 1px solid #ccc; border-radius: 2px; padding: 5px; }"
                            "QLineEdit:focus { border: 1px solid #4285f4; }")

    def focusInEvent(self, event):
        self.selectAll()
        super().focusInEvent(event)

    def mousePressEvent(self, event):
        self.selectAll()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.returnPressed.emit()
        super().keyPressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create four web views and toolbars
        self.webviews = []
        self.toolbars = []
        for i in range(4):
            webview = QWebEngineView()
            webview.setUrl(QUrl('http://duckduckgo.com'))
            self.webviews.append(webview)

            toolbar = QToolBar()
            self.addToolBar(toolbar)
            self.toolbars.append(toolbar)

            back_btn = QAction(QIcon("icons/back.png"), 'Back', self)
            back_btn.triggered.connect(webview.back)
            toolbar.addAction(back_btn)

            forward_btn = QAction(QIcon("icons/forward.png"), 'Forward', self)
            forward_btn.triggered.connect(webview.forward)
            toolbar.addAction(forward_btn)

            reload_btn = QAction(QIcon("icons/reload.png"), 'Reload', self)
            reload_btn.triggered.connect(webview.reload)
            toolbar.addAction(reload_btn)

            home_btn = QAction(QIcon("icons/home.png"), 'Home', self)
            home_btn.triggered.connect(lambda i=i: self.navigate_home(i))
            toolbar.addAction(home_btn)

            url_bar = UrlLineEdit()
            url_bar.returnPressed.connect(lambda i=i: self.navigate_to_url(i))
            toolbar.addWidget(url_bar)

            webview.urlChanged.connect(lambda q, url_bar=url_bar: self.update_url(q, url_bar))
            
        # Create a grid layout to arrange the web views and toolbars
        layout = QGridLayout()
        for i in range(2):
            for j in range(2):
                index = i * 2 + j
                layout.addWidget(self.toolbars[index], i * 2, j)
                layout.addWidget(self.webviews[index], i * 2 + 1, j)
        
        # Create a widget to hold the layout and set it as the central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.showMaximized()

    def navigate_home(self, index):
        self.webviews[index].setUrl(QUrl('http://duckduckgo.com'))

    def navigate_to_url(self, index):
        url = self.toolbars[index].findChild(UrlLineEdit).text()
        if url.startswith("http"):
            self.webviews[index].setUrl(QUrl(url))
        else:
            self.webviews[index].setUrl(QUrl("https://www.google.com/search?q=" + url))

    def update_url(self, q, url_bar):
        url_bar.setText(q.toString())

app = QApplication(sys.argv)
QApplication.setApplicationName('Multibrowser')
window = MainWindow()
app.exec_()
