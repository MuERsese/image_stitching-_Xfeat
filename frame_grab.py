import cv2
import numpy as np
import matplotlib.pyplot as plt
from modules.xfeat import XFeat
from cal_homography import stitcher

class frame_grab:
    def frame_grabber(self,camid):
        
        
        cameraMatrix=1.0e+03*np.array([[2.3314,0.0029,0.9733],[0,2.3270,0.4898],[0,0,0.0010]])
        distCoeffs=(0.0824,-0.0211,-0.0011,-1.0369e-04,-0.2171)
        cap=cv2.videoCapture(camid)

    
        
    




#if __name__=='__main__':