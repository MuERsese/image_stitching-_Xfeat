#Based on ORB
import cv2
import numpy as np
import matplotlib.pyplot as plt
from modules.xfeat import XFeat

class cal_homography:
    def __init__(self):
        pass
    def cal_homography(self,img1,img2):
        
        #img1=img1[10:,20:]
        #img2=img2[10:,20:]
        h1,w1,_=img1.shape
        h2,w2,_=img2.shape
        
        
        good_matches = []
        kp1, kp2 = [], []
        points1, points2 = [], []
        xfeat=XFeat()
       
        #compute kpoints and their descriptors
        #param1,param2: dict(keypoints:,scores:,descriptors,)
        param1=xfeat.detectAndCompute(x=img1,top_k=500)
        param2=xfeat.detectAndCompute(x=img2,top_k=500)
        
        
        #get the keypoints and descriptors of both images
        kpts1, descs1 = param1[0]['keypoints'],param1[0]['descriptors']
        kpts2, descs2 = param2[0]['keypoints'], param2[0]['descriptors']
        
        #idx0,idx1 are the indices of the matched points
        idx0, idx1 = xfeat.match(descs1, descs2, 0.82)
        points1 = kpts1[idx0].numpy()
        points2 = kpts2[idx1].numpy()

        #calculate homography matrix
        H, inliers = cv2.findHomography(points2, points1, cv2.USAC_MAGSAC,maxIters=700, confidence=0.995)
        
        return H

        

    
    
        
        
       

    

      




if __name__=='__main__':
    stitcher=cal_homography()
    img1=cv2.imread('./figs/fig0.jpg')
    img2=cv2.imread('./figs/fig1.jpg')
    stitcher.cal_homography(img1,img2)
    #print(H)
    if img1 is None or img2 is None:
        print("Error: can't read images.")
    


