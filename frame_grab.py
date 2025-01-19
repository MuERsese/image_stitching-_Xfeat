import cv2
import numpy as np
import matplotlib.pyplot as plt
from modules.xfeat import XFeat


#criteria
#1.low motion blur(for the threshold, we will take the first image as a reference, which is alwasy sharp)
#2.link between the adjacent frame

class frame_grabber:
    #this function is using fast fourier transform to
    #size is a parameter which used to describe the mask area refer to the center of the image, which are low frequency part
    #blurred image usually has higher energy in high frequency part
    def frame_grab(self,frame,size,thresh):
        Gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        (height,width)=Gray_frame.shape
        cX,cY=(int(width/2.0),int(height/2.0))
        fft=np.fft.fft2(frame)
        fft_shift=np.fft.fftshift(fft)
        fft_shift[cY-size:cY+size,cX-size:cX+size]=0
        fft_shift=np.fft.ifftshift(fft_shift)
        recovered_image=np.fft.ifft2(fft_shift)
        magnitude_spectrum=20*np.log(np.abs(recovered_image))
        mean=np.mean(magnitude_spectrum)
        # print("mean of magnitude spectrum is", mean)
        result=thresh<=mean
        return result
        
        #fft_shift=np.fft.fftshift(fft)




        
        
        
        # cameraMatrix=1.0e+03*np.array([[2.3314,0.0029,0.9733],[0,2.3270,0.4898],[0,0,0.0010]])
        # distCoeffs=(0.0824,-0.0211,-0.0011,-1.0369e-04,-0.2171)
        # cap=cv2.videoCapture(camid)

    
        
    




if __name__=='__main__':
    frame_grabber=frame_grabber()
    
    frame=cv2.imread('./figs/fig_blurred0.jpg')
    size=300
    thresh=10
    frame_grabber.frame_grab(frame,size,thresh)
    