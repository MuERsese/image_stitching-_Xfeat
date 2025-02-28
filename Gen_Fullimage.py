import cv2
import numpy as np
import cal_homography
import stitching
from cal_laplacian_var import cal_laplacian_var

def Gen_Fullimage(camid):

    cameraMatrix=1.0e+03*np.array([[2.3314,0.0029,0.9733],[0,2.3270,0.4898],[0,0,0.0010]])
    distCoeffs=(0.0824,-0.0211,-0.0011,-1.0369e-04,-0.2171)
    calculate=cal_homography.cal_homography()
    
    kpts_thresh=200
    laplacian_thresh=150



    #cap=cv2.VideoCapture(camid)
    cap=cv2.VideoCapture('../../test_video_1080P0.mp4')
    if not cap.isOpened():
        print("Error: can't open camera")
        return None,None,0
    

    
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps)  
   
    
    #initialize to have the first frame
    ret,frame=cap.read()
    if not ret:
        print('Error: output initialization failed')
        return None,None,0
    img1=cv2.undistort(frame,cameraMatrix,distCoeffs)
    
    

    

    
   
    #define 2 arrays to store the key frame and corresponding homography matrix
    keyframe=[]
    homography=[]
    n=1
    H11=np.array([[1,0,0],[0,1,0],[0,0,1]]).astype(np.float32)
    keyframe.append(img1)
    homography.append(H11)
    num_kpts=kpts_thresh
    laplacian_var=laplacian_thresh
    
    while True:
        ret,current=cap.read()
        
        if not ret:
            print("Error: can't get frame")
            return None,None,0
        
        
        undistorted_img2=cv2.undistort(current,cameraMatrix,distCoeffs)
        H,num_kpts=calculate.cal_homography(img1,undistorted_img2)
        laplacian_var=cal_laplacian_var(undistorted_img2)
        
        key=cv2.waitKey(delay)
        #if the image have less keypoints and clearer than threshold
        if(num_kpts<kpts_thresh and laplacian_var>laplacian_thresh):
            keyframe.append(undistorted_img2)
            homography.append(H)
            img1=undistorted_img2.copy()
            n+=1
            print("keyframe{} added successfully".format(n),undistorted_img2.shape[0],"x",undistorted_img2.shape[1])
        
        if (key & 0xFF==ord('q')):
            break
        
        
        
        # cv2.namedWindow('current',cv2.WINDOW_NORMAL)
        cv2.imshow('current',current)
        # cv2.imshow('output',output_frame)
        
    
    
    cap.release()        
    cv2.destroyAllWindows()
    return keyframe,homography,n
    
    





if __name__=='__main__':
    stitcher=stitching.stitching()
    keyframe=[]
    homography=[]
    camid=-1
    keyframe,homography,n=Gen_Fullimage(camid)
    
    output=stitcher.stitching(keyframe,homography,n)
    if output is None:
        print("no output generated")
        
    # cv2.namedWindow('output',cv2.WINDOW_NORMAL)
    cv2.imshow('output',output)
    cv2.imwrite('./Test_images/output.png',output)
    print("image saved successfully")
    while True:
        if (cv2.waitKey(1) & 0xFF==ord('l')):
            break
    cv2.destroyAllWindows()  
            


    