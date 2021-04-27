# Logger

This is a simple python script which uses singleton property to create multiple objects which ill refer to single object.
The send and recieve functions have queue which will be open as a thread. (can be merged into single method)
After all the communication or the messages when the thread is closed the whole data in the queue is dumbed into the respective file.
