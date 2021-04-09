from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from about import AboutDialog

import os
import sys
import pathlib




class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(18,18))
        navtb.setAllowedAreas(Qt.TopToolBarArea)
        navtb.setFloatable(False)
        navtb.setMovable(False)
        self.addToolBar(navtb)


        '''
        menutb = QToolBar("Tools bar")
        menutb.setIconSize(QSize(32,32))
        menutb.setFloatable(False)
        menutb.setMovable(False)
        self.addToolBar(QtCore.Qt.RightToolBarArea, menutb)
        '''

        navtb.setStyleSheet("""
            QToolButton {
                border: 2px;
                padding: 1px 4px;
                background: transparent;
                border-radius: 4px;
            }

            QToolButton:selected { /* when selected using mouse or keyboard */
                background: #a8a8a8;
            }

            QToolButton:pressed {
                background: #888888;
            }
        """)


        back_btn = QAction(QIcon(os.path.join('data/images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('data/images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('data/images', 'arrow-circle-315.png')), "reload", self)
        reload_btn.setStatusTip("reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)


        stop_btn = QAction(QIcon(os.path.join('data/images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        navtb.addSeparator()
        
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('data/images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)
        
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        #self.urlbar.setStyleSheet('border-radius: 4px; border-width: 3px;')
        self.urlbar.setStyleSheet("""
            border: 2px solid gray;
            border-radius: 10px;
            padding: 3;
            background: #fff;
            selection-background-color: darkgray;
            left: 5px;
            right: 5px;
            font: 12px/14px sans-serif
        """)

        
        home_btn = QAction(QIcon(os.path.join('data/images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go Home")
        home_btn.triggered.connect(lambda: self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        # Right menubar

        self.menu_bar = QMenuBar()
        
        self.menu_bar.setMinimumSize(18,18)
        self.menu_bar.setStyleSheet("""
            QMenuBar {
                border: 2px;
                padding: 10px 2px;
                max-width: 40px;
            }

            QMenuBar::item {
                border: 2px;
                padding: 1px 4px;
                background: transparent;
                border-radius: 4px;
                height: 24px;
            }

            QMenuBar::item:selected { /* when selected using mouse or keyboard */
                background: #a8a8a8;
            }

            QMenuBar::item:pressed {
                background: #888888;
            }
        """)
        self.file_menu = QMenu('MENU', self)
        self.file_menu.setIcon(QIcon(os.path.join('data/images', 'menu.png')))

        bookmarks_action = QAction(QIcon(os.path.join('data/images', 'bookmark.png')), "Bookmarks", self)
        bookmarks_action.setStatusTip("Open all bookmarks")
        bookmarks_action.triggered.connect(lambda _: self.bookmarks())
        self.file_menu.addAction(bookmarks_action)

        new_tab_action = QAction(QIcon(os.path.join('data/images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        self.file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('data/images', 'disk--arrow.png')), "Open file", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        self.file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('data/images', 'disk--pencil.png')), "Save page to file", self)
        save_file_action.setStatusTip("Open from file")
        save_file_action.triggered.connect(self.save_file)
        self.file_menu.addAction(save_file_action)
        
        about_action = QAction(QIcon(os.path.join('data/images', 'question.png')), "About CoderLog Browser", self)
        about_action.setStatusTip("Find out more about CoderLog")
        about_action.triggered.connect(self.about)
        self.file_menu.addAction(about_action)
        
        self.menu_bar.addMenu(self.file_menu)
    
        navtb.addWidget(self.menu_bar)
        
        self.add_new_tab(QUrl('https://coderlog.top'), 'Homepage')

        '''Shortcuts'''

        self.shortcut_open = QShortcut(QKeySequence('F5'), self)
        self.shortcut_open.activated.connect(lambda: self.tabs.currentWidget().reload())

        self.show()

        self.setWindowIcon(QIcon(os.path.join('data/images', 'icon.png')))
    
    
    @QtCore.pyqtSlot("QWebEngineDownloadItem*")
    def on_downloadRequested(self, download):
        old_path = download.url().path()  # download.path()
        suffix = QtCore.QFileInfo(old_path).suffix()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", old_path, "*." + suffix
        )
        if path:
            download.setPath(path)
            download.accept()


    def bookmarks(self):
        pass
        
    def mycontextMenuEvent(self, event):
        url = 'view-source:' + self.urlbar.text()
        menu = QtWidgets.QMenu(self)
        reloadAction = menu.addAction(QIcon(os.path.join('data/images', 'arrow-circle-315.png')), "Reload page")
        reloadAction.triggered.connect(lambda: self.tabs.currentWidget().reload())
        
        innewtabAction = menu.addAction("O&pen in New Window")
        innewtabAction.triggered.connect(lambda: self.add_new_tab())
        
        sourceAction = menu.addAction("View source")
        sourceAction.triggered.connect(lambda: self.add_new_tab(qurl=QUrl(url)))
        menu.exec_(event.globalPos())

    def actionClicked(self, checked):
        action = self.sender()
        print(action.text())
        print(action.data())

    def add_new_tab(self, qurl=None, label="Blank"):
        
        if qurl is None:
            qurl = QUrl.fromLocalFile(os.path.dirname(os.path.realpath(__file__)) + '/data/files/blank/index.html')

        browser = QWebEngineView()
        browser.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        browser.page().fullScreenRequested.connect(lambda request: request.accept())
        browser.setUrl(qurl)
        QtWebEngineWidgets.QWebEngineProfile.defaultProfile().downloadRequested.connect(
            self.on_downloadRequested
        )

        browser.contextMenuEvent = self.mycontextMenuEvent
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                    self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                    self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()
    
    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        
        self.tabs.removeTab(i)

    def view(self):
        url =self.urlbar.text()
        url=f"view-source:{url}"
        self.tabs.currentWidget().setUrl(QUrl(url))


    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s CoderLog Browser" % title)

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                        "*.htm *.html"
                                                        "All files (*.*)")
        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "save page as", "",
                                                        "*.htm *.html"
                                                        "All files (*.*)")
        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, 'w') as f:
                f.write(html)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://coderlog.top"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        
        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('data/images', 'lock-ssl.png')))
        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('data/images', 'lock-nossl.png')))
        
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(999)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("CoderLog Browser")
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_()) 