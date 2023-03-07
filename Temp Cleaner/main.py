import threading
import win32gui
import win32con
import winshell
import logging
import shutil
import plyer
import os


class App:
    RUN_PATH = winshell.startup()
    TEMP_PATH = os.path.expandvars('%temp%')
    LOG_PATH = os.path.join(winshell.desktop(), 'Temp Cleaner.log')

    def __init__(self, hide=False):
        self.logger = logging.getLogger(App.LOG_PATH)

        if os.path.basename(os.path.dirname(__file__)) != os.path.basename(App.RUN_PATH):
            App.copy2startup()
            self.logger.info('The program moved into startup')

        if hide:
            App.hide()

    def clean(self):
        deleted_files, undeleted_files, total_size = self.delete(App.TEMP_PATH)
        msg = f"Deleted: {len(deleted_files):<6} " \
              f"Undeleted: {len(undeleted_files):<7} " \
              f"Size: {App.bytes_to_string(total_size)}"

        self.notice(msg)

    def notice(self, msg, title='Temp Cleaner', timeout=7):
        def notify():
            plyer.notification.notify(
                title=title,
                message=msg,
                timeout=timeout
            )

        self.logger.info(msg)
        threading.Thread(target=notify).run()

    @staticmethod
    def delete(path, deleted_files=[], undeleted_files=[], total_size=0):
        try:
            if os.path.isfile(path):
                file_size = os.path.getsize(path)
                os.remove(path)
                total_size += file_size
                deleted_files.append(path)

            else:
                for item in os.listdir(path):
                    deleted_files, undeleted_files, total_size = App.delete(item, deleted_files, undeleted_files, total_size)

                os.rmdir(path)

        except OSError or PermissionError:
            undeleted_files.append(path)


        return deleted_files, undeleted_files, total_size

    @staticmethod
    def copy2startup():
        filename = os.path.basename(__file__)
        destination = os.path.join(App.RUN_PATH, filename)
        shutil.copyfile(__file__, destination)

    @staticmethod
    def hide():
        pid = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(pid, win32con.SW_HIDE)

    @staticmethod
    def bytes_to_string(n, points=2):
        if n >= 1024:
            n /= 1024

            if n >= 1024:
                n /= 1024

                if n >= 1024:
                    n /= 1024

                    return f"{n:.{points}f} GB"

                return f"{n:.{points}f} MB"

            return f"{n:.{points}f} KB"

        return f"{round(n)} B"



logging.basicConfig(
    filename=App.LOG_PATH,
    format='[%(asctime)s]  %(message)s',
    level=1
)


app = App()
app.clean()
