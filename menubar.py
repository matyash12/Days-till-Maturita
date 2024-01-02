import rumps
import time
from datetime import datetime, timedelta
import json


rumps.debug_mode(False)


# space to store all data
# will load on app start
# when you change something and want to save call SaveData()


class MaturitaStatusBarApp(rumps.App):
    DATA = {"target_date": "1970-01-02"}
    response = None

    def __init__(
        self, name, title=None, icon=None, template=None, menu=None, quit_button="Quit"
    ):
        super().__init__(name, title, icon, template, menu, quit_button)
        self.load()

    def load(self):
        try:
            with self.open("data.json", "r") as f:
                self.DATA = json.loads(f.read())
                print("Loaded data:", self.DATA)
        except:
            # propably file doesnot exists
            # fill with some data

            # target_date today_date + 7 days
            target_date = datetime.now().date() + timedelta(days=7)
            # Format the current date as a string in 'YYYY-MM-DD' format
            date_str = target_date.strftime("%Y-%m-%d")
            self.DATA["target_date"] = date_str
            self.save()

    def save(self):
        # saving data to disk
        with self.open("data.json", "w") as f:
            print("Saving data:", self.DATA)
            f.write(json.dumps(self.DATA))

    @rumps.clicked("Start on startup")
    def start_on_boot(self, _):
        
        rumps.alert(
            title="Start on startup",
            message="To start on startup follow apple help: https://support.apple.com/en-gb/guide/mac-help/mh15189/mac",
            icon_path='icon.icns',
        )

    @rumps.clicked("Set target date")
    def prefs(self, _):
        self.response = rumps.Window(
            title="Set target date",
            message="Format is 'year-month-day' eg: 0000-00-00. Keep the zeros",
            default_text=self.DATA["target_date"],
            dimensions=(100,20)
        ).run()

    # TODO battery? every second?
    @rumps.timer(1)
    def remaining(self, _):
        if self.response != None:
            if self.response.clicked:
                # ok
                entered_text = self.response.text
                try:
                    datetime.strptime(entered_text, "%Y-%m-%d")
                    self.DATA["target_date"] = self.response.text
                    self.save()
                except:
                    # date is invalid = user entered in wrong format
                    print("User entered wrong date (wrong format..)")
                    rumps.alert(
                        "Wrong format",
                        message="Please enter in '2023-09-03' year-month-day",
                        icon_path='icon.icns',
                    )

                # otherwise it will get here forever..
                self.response = None

            else:
                # cancel
                pass

        remaining_days = remaining_days_between_dates(
            get_current_date(), self.DATA["target_date"]
        )

        if remaining_days >= 2:
            self.title = str(remaining_days) + " days"
        elif remaining_days == 1:
            self.title = "Tomorrow"
            # self.title = str(remaining_days) + " day"
        elif remaining_days == 0:
            self.title = "Today"
        elif remaining_days == -1:
            self.title = "Yesterday"
            # self.title = str(-remaining_days) + " day late"
        elif remaining_days < -1:
            self.title = str(-remaining_days) + " days late"


def get_current_date() -> str:
    # Get the current date
    current_date = datetime.now().date()
    # Format the current date as a string in 'YYYY-MM-DD' format
    date_str = current_date.strftime("%Y-%m-%d")
    return date_str


def remaining_days_between_dates(date_str1, date_str2) -> int:
    try:
        # Convert the date strings to datetime objects
        date1 = datetime.strptime(date_str1, "%Y-%m-%d")
        date2 = datetime.strptime(date_str2, "%Y-%m-%d")

        # Calculate the remaining days and return it as an integer
        remaining_days = (date2 - date1).days

        # Check if the result is negative (date2 is before date1)
        return remaining_days
        # if remaining_days < 0:
        #    return -1  # Indicate that the second date is before the first date
        # else:
        #    return remaining_days
    except ValueError:
        return -2  # Indicate an invalid date format


# starting the app
APP = MaturitaStatusBarApp("Maturita", quit_button="Stop and exit").run()
