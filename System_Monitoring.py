import pyautogui
import time
import os
from datetime import datetime

class SystemTool:
    def __init__(self):
        self._status = "Ready"      

    def show_status(self):
        print(f"\nTool Status : {self._status}")


#Child Class (Inheritance)
class ActivityLogger(SystemTool):

    def __init__(self, interval):
        super().__init__()

        #Encapsulation (Private Variables)
        self.__interval = interval
        self.__log_file = "activity_log.txt"
        self.__screenshot_folder = "screenshots"
        self.__count = 0

        #Create Screenshot Folder
        if not os.path.exists(self.__screenshot_folder):
            os.makedirs(self.__screenshot_folder)

    #Save Log
    def log_event(self, message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.__log_file, "a") as file:
            file.write(f"[{current_time}] {message}\n")

    def take_screenshot(self):
        self.__count += 1

        #Screenshot File Name
        filename = (f"{self.__screenshot_folder}/ screenshot_ {self.__count}.png")
        #Capture Screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)

        print(f"Screenshot Saved : {filename}")
        self.log_event(f"Screenshot Captured : {filename}")

    def start_monitoring(self, total_screenshots):
        print("\n----- Monitoring Started -----\n")

        self._status = "Monitoring"
        self.log_event("Monitoring Started")

        for i in range(total_screenshots):
            self.take_screenshot()
            time.sleep(self.__interval)

        self._status = "Completed"
        self.log_event("Monitoring Completed")

        print("\n----- Monitoring Completed -----")

def main():
    print("\n===== ACTIVITY LOGGER & SCREENSHOT SAVER =====")

    interval = int(input("\nEnter Screenshot Interval (Seconds) : "))
    total = int(input("Enter Number Of Screenshots : "))

    #Object
    logger = ActivityLogger(interval)
    logger.start_monitoring(total)
    logger.show_status()

#Final Runing Program
if __name__ == "__main__":
    main()


