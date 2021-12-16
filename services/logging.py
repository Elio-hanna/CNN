from typing import Optional
from services.timestamp import *


class log:

    def log(self, name, result, parm: Optional[str] = None):
        file_object = open('log.txt', 'a')
        day, mon, year, hour, minu, sec = timestamp.timestamp(self=timestamp)
        file_object.write(
            "[" + str(day) + "/" + str(mon) + "/" + str(year) + " " + str(hour) + ":" + str(minu) + ":" + str(
                sec) + "]: ")
        file_object.write("the user executed " + name + " with these parameters{ ")
        file_object.write(str(parm) + "}")
        file_object.write("the result is " + result + "\n")

    def log_error(self, name):
        file_object = open('log.txt', 'a')
        day, mon, year, hour, minu, sec = timestamp.timestamp(self=timestamp)
        file_object.write(
            "[" + str(day) + "/" + str(mon) + "/" + str(year) + " " + str(hour) + ":" + str(minu) + ":" + str(
                sec) + "]: ")
        file_object.write("Error while executing " + name)
