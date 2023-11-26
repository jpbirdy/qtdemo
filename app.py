from PyQt6 import QtCore, QtWidgets, QtGui


# import PySide6.QtCore
from datetime import datetime, timedelta

import logging
import time
# 使用apscheduler创建一个定时任务
from apscheduler.schedulers.qt import QtScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
import io
import logging
from PyQt6 import QtCore, QtWidgets

lock = QtCore.QReadWriteLock()
import sys
import os

def task1():
    lock.lockForWrite()
    print("task1 start")
    time.sleep(1)
    print("task1 end")
    lock.unlock()

def task2():
    lock.lockForWrite()
    print("task2 start")
    time.sleep(2)
    print("task2 end")
    lock.unlock()

def task3():
    lock.lockForRead()
    print("task3 start")
    time.sleep(3)
    print("task3 end")
    lock.unlock()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


from chrome import start_chrome
def global_start_chrome():
    lock.lockForRead()
    start_chrome()
    lock.unlock()


def main():
    

    class QTextEditStream(io.TextIOBase):
        def __init__(self, text_edit):
            super().__init__()
            self.text_edit = text_edit

        def write(self, s):
            self.text_edit.append(s.rstrip())

    app = QtWidgets.QApplication([])
    
    # 关闭按钮时最小化到托盘，不退出
    app.setQuitOnLastWindowClosed(False)

    w = QtWidgets.QWidget()

    # 创建一个日志显示框,与logging模块绑定，显示logging内容
    log_display = QtWidgets.QTextEdit()
    log_display.setReadOnly(True)
    # 自动滚动到底部
    log_display.textChanged.connect(lambda: log_display.moveCursor(QtGui.QTextCursor.MoveOperation.End))

    log_handler = logging.StreamHandler(QTextEditStream(log_display))
    log_handler.setLevel(logging.INFO)
    
    cmdline_handler = logging.StreamHandler()
    cmdline_handler.setLevel(logging.INFO)
    
    file_handler = logging.FileHandler('log.txt')
    file_handler.setLevel(logging.INFO)

    logging.basicConfig(level=logging.INFO, handlers=[log_handler, file_handler, cmdline_handler], format='%(asctime)s %(levelname)s %(message)s')
    logging.info('Logging test')

    # 创建一个按钮，点击后会打印一条日志
    button = QtWidgets.QPushButton('Log')
    button.clicked.connect(lambda: logging.info('Button clicked'))


    
    # 创建一个定时任务
    scheduler = QtScheduler()
    # 间隔5秒钟执行一次
    # scheduler.add_job(lambda: logging.info('Tick!'), 'interval', seconds=1)
    
    # 10s后执行，只执行一次
    run_time = datetime.now() + timedelta(seconds=10)
    scheduler.add_job(task1, 'date', run_date=run_time)
    scheduler.add_job(global_start_chrome, 'date', run_date=run_time)
    
    next_run_time = datetime.now() + timedelta(seconds=20)
    
    # 10s 后执行，每隔1s执行一次
    scheduler.add_job(task1, 'interval', seconds=5, next_run_time=next_run_time, max_instances=1)
    scheduler.add_job(task2, 'interval', seconds=5, next_run_time=next_run_time, max_instances=1)
    scheduler.add_job(task3, 'interval', seconds=5, next_run_time=next_run_time, max_instances=1)
    
    scheduler.add_job(global_start_chrome, 'interval',
                      seconds=60, max_instances=1)
    
    
    scheduler.start()

    # 如果暂停，则暂停键不可用，否则开始键不可用
    start_button = QtWidgets.QPushButton('Start')
    stop_button = QtWidgets.QPushButton('Stop')
    
    start_button.setEnabled(False)
    stop_button.setEnabled(True)
    start_button.clicked.connect(scheduler.resume)
    start_button.clicked.connect(lambda: start_button.setEnabled(False))
    start_button.clicked.connect(lambda: stop_button.setEnabled(True))
    stop_button.clicked.connect(scheduler.pause)
    stop_button.clicked.connect(lambda: start_button.setEnabled(True))
    stop_button.clicked.connect(lambda: stop_button.setEnabled(False))
    
    
    
    

    # 界面布局
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(log_display)
    layout.addWidget(button)
    layout.addWidget(start_button)
    layout.addWidget(stop_button)
    w.setLayout(layout)


    # 最小化时显示到托盘，并创建退出菜单
    a1 = QtGui.QAction("&show", triggered=w.show)
    def quit():
        # try:
        #     if scheduler.running:
        #         scheduler.shutdown()
        # except:
        #     pass
        app.quit()

    a2 = QtGui.QAction("&quit", triggered=quit)
    tpmenu = QtWidgets.QMenu()
    tpmenu.addAction(a1)
    tpmenu.addAction(a2)
    tray = QtWidgets.QSystemTrayIcon()
    tray.setIcon(QtGui.QIcon(resource_path("icon.png")))
    tray.setContextMenu(tpmenu)
    tray.show()
    tray.showMessage("提示", "程序已启动")

    w.resize(600, 800)
    w.setWindowTitle('Simple')
    w.show()
    try:
        app.exec()
    except:
        app.quit()
   

if __name__ == "__main__":
    main()
