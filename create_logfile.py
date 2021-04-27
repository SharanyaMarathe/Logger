from multiprocessing import Queue
import threading
import time
from datetime import datetime


class Singleton(type):
    
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Log_File_Creator(metaclass=Singleton):
    #to make the logger singleton object
    __metaclass__ = Singleton
    

    def __init__(self, filename):
        
        self.DefaultFileHeader = "Date\t   SystemTime   Device  Direction   Data\n"; #header for the file
        self.delim = " , "
        self._isOpen = False
        self.dataqueue = Queue()
        self.lock = threading.Lock()
        if (not self._isOpen):
            with open(filename, 'w') as file:
                file.write(self.DefaultFileHeader)
            self._isOpen = True
        self.is_run1 = False
        #to make the thread deamon so that it'll capture the data
        self.writerThread = threading.Thread(target=self.data_writer, args=(filename,))
        self.writerThread.setDaemon(True)  
        self.writerThread.start()
        self.is_run1 = self.writerThread.is_alive()

    
    def send_data(self, responses,devicename):
        self.current_time = datetime.now()
        self.time = self.current_time.strftime("%d/%m/%Y %H:%M:%S")
        results = str(self.time) + "     " + devicename +  "\t --> " + self.delim + "     " + str(responses) + "\n"
        with self.lock:
            self.dataqueue.put(results)
            
            

    def recieve_data(self, responses, devicename):
        self.current_time = datetime.now()
        self.time = self.current_time.strftime("%d/%m/%Y %H:%M:%S")
        results = str(self.time) + "     " + devicename +  "\t <-- " + self.delim  + "     " +str(responses) + "\n"
        with self.lock:
            self.dataqueue.put(results)


    def data_writer(self, filename):  # thread
        with open(filename, 'a') as file:
            while (self.is_run1):
                with self.lock:
                    if (self.dataqueue.qsize() > 0):
                        file.write(self.dataqueue.get())
                    else:
                        time.sleep(2)

    def close(self):
        #to terminate the thread
        self.is_run1 = False
        self.writerThread.join()


if __name__ == '__main__':
    log = Log_File_Creator("communication_info.log")
    log1 = Log_File_Creator("communication_info.log")
    #print object log and log1 to see that it's creating singleton object
    log.send_data("HI","COM1")
    log1.send_data("HELLO","COM2")
    log1.recieve_data("GOOD  MORNING","COM2")
    log.recieve_data("GOOD DAY IT IS","COM1")
    log.close()
    log1.close()
