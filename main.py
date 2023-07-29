import schedule
import time
import datetime
from datetime import datetime, timedelta
from dotenv import load_dotenv
import gui
import sys

load_dotenv()


def start_gui():
    app = gui.QApplication(sys.argv)
    window = gui.PodStatusGUI()
    window.show()
    sys.exit(app.exec_())


def main():
    # Schedule the alert to be sent every day at 5 PM
    time_now = (datetime.now() + timedelta(seconds=2)).strftime("%H:%M:%S")
    schedule.every().day.at(time_now).do(start_gui)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
