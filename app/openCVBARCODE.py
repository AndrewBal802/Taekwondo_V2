import imutils

class BarCodeReader(object):

    def __init__(self):
        self.video = = VideoStream(src=0).start() #src=-1 for linux system (default camera)
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
       return 
   

