import os

msg_template = "Message no %d file %s\n"

class FileTestHelper(object):
    def get_name(self):
        return os.tempnam()
        
    def log(self, filename, message=None):
        try:
            self.counter
        except AttributeError:
            self.counter = 1
        if message is None:
            msg = msg_template % (self.counter, filename)
            self.counter+=1
        else:
            msg = message
        f = file(filename, "a")
        f.write(msg)
        f.close()

