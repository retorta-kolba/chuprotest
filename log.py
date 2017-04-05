# -*- coding: cp1251 -*-
import time


class Log:
    """
    simple Log class for easy use
    """
    __logsfile = list()
    __logs = list()

    def force_set_file(self, log):
        self.__logsfile.append(str(log))
        self.__logs.append(log)

    def set_file(self, logfile="log.txt"):
        self.__logsfile.append(logfile)
        self.__logs.append(open(logfile, 'a', encoding='cp1251'))

    def __init__(self, log="log.txt", forceset=False):
        if forceset:
            self.force_set_file(log)
        else:
            self.set_file(log)

    def write(self, str=""):
        for log in self.__logs:
            log.write(str)

    def write_time(self):
        self.writeln(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    def writeln(self, str=""):
        self.write(str+'\n')

    def close_file(self):
        for log in self.__logs:
            if log is not None:
                log.close()

    def __del__(self):
        self.close_file()


def log(info):
    f = open('log.txt', 'a', encoding='cp1251')
    f.write(time.strftime('%Y-%m-%d %H:%M:%S',
                          time.localtime()) + " " + str(info) + "\n")
    f.close()
