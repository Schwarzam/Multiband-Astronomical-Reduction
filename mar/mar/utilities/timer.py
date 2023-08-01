from time import time as timer

class timeit():
    """
    A timer utility class that provides methods to measure elapsed time in minutes,
    seconds, and milliseconds. The class also has methods to reset the timer and sum
    the total elapsed time.

    Attributes:
        start (float): The timestamp when the timer was started.
        sum_timer (float): The total elapsed time since the timer was created or reset.
    """
    def __init__(self):
        """
        Initializes a new instance of the `timeit` class and starts the timer.
        """
        self.start = timer()
        self.sum_timer = 0

    def reset(self):
        """
        Resets the timer to the current timestamp.
        """
        self.start = timer()

    def reset_all(self):
        """
        Resets the timer to the current timestamp and resets the total elapsed time.
        """
        self.start = timer()
        self.sum_timer = 0

    def minutes(self, reset=False):
        """
        Calculates the elapsed time in minutes since the timer was started or reset.

        Args:
            reset (bool): If True, resets the timer to the current timestamp.

        Returns:
            float: The elapsed time in minutes, rounded to one decimal place.
        """
        val = (timer() - self.start) / 60
        if reset:
            self.start = timer()
        return round(val, 1)

    def seconds(self, reset=False):
        """
        Calculates the elapsed time in seconds since the timer was started or reset.

        Args:
            reset (bool): If True, resets the timer to the current timestamp.

        Returns:
            float: The elapsed time in seconds, rounded to three decimal places.
        """
        val = (timer() - self.start)
        if reset:
            self.start = timer()
        return round(val, 3)

    def milliseconds(self, reset=False):
        """
        Calculates the elapsed time in milliseconds since the timer was started or reset.

        Args:
            reset (bool): If True, resets the timer to the current timestamp.

        Returns:
            float: The elapsed time in milliseconds, rounded to three decimal places.
        """
        val = ((timer() - self.start) * 1000)
        if reset:
            self.start = timer()
        return round(val, 3)

    def sum_minutes(self):
        """
        Returns the total elapsed time in minutes.

        Returns:
            float: The total elapsed time in minutes, rounded to one decimal place.
        """
        return round(self.sum_timer, 1)

    def sum_timer_minutes(self, reset=True):
        """
        Calculates the elapsed time in minutes since the timer was started or reset
        and adds it to the total elapsed time.

        Args:
            reset (bool): If True, resets the timer to the current timestamp.
        """
        self.sum_timer += (timer() - self.start) / 60
        if reset:
            self.start = timer()


# Example usage
timer_t0 = timeit()
timer_t1 = timeit()