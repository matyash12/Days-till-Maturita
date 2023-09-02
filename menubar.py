import rumps
import time
from datetime import datetime

FINISH_DATE = "2024-05-02"

class MaturitaStatusBarApp(rumps.App):
    test = 0
    @rumps.timer(1)
    def remaining(self, _):
        # Get the current date
        current_date = datetime.now().date()
        # Format the current date as a string in 'YYYY-MM-DD' format
        date_str = current_date.strftime("%Y-%m-%d")
        
        remaining_days = remaining_days_between_dates(date_str,FINISH_DATE)
        self.title = str(remaining_days) + ' days'


def remaining_days_between_dates(date_str1, date_str2):
    try:
        # Convert the date strings to datetime objects
        date1 = datetime.strptime(date_str1, "%Y-%m-%d")
        date2 = datetime.strptime(date_str2, "%Y-%m-%d")

        # Calculate the remaining days and return it as an integer
        remaining_days = (date2 - date1).days

        # Check if the result is negative (date2 is before date1)
        if remaining_days < 0:
            return -1  # Indicate that the second date is before the first date
        else:
            return remaining_days
    except ValueError:
        return -2  # Indicate an invalid date format



if __name__ == "__main__":
    status = MaturitaStatusBarApp("Maturita").run()