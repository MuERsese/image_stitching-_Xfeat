#Based on ORB
import cv2
import numpy as np
import matplotlib.pyplot as plt
from modules.xfeat import XFeat

def stitching(img1,img2):
    
    #img1=img1[10:,20:]
    #img2=img2[10:,20:]
    h1,w1,_=img1.shape
    h2,w2,_=img2.shape
    
    gray1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)    
    gray2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

    #create ORB object
    orb=cv2.ORB_create()
    
    #compute kpoints and their descriptors
    kpts1,des1=orb.detectAndCompute(gray1,None)
    kpts2,des2=orb.detectAndCompute(gray2,None)
    
    #use brute force method to do matching 

    #create a brute force matcher
    bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
    
    #output the matching result
    matches=bf.match(des1,des2)
    
    #only use front half of matches
    matches=sorted(matches,key=lambda x:x.distance)
    num_matches=int(len(matches)/4)
    good_matches=matches[:num_matches]
    #draw_Matches=cv2.drawMatches(img1,kpts1,img2,kpts2,good_matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    #calculate the homography matrix
    img1_pts=np.float32([kpts1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
    img2_pts=np.float32([kpts2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)
    H,_=cv2.findHomography(img2_pts,img1_pts,cv2.RANSAC)

    #get the projection of img2 to img1
    
    #get the corners of two images
    corner1=np.float32([[0,0],[0,h1],[w1,h1],[w1,0]]).reshape(-1,1,2)
    corner2=np.float32([[0,0],[0,h2],[w2,h2],[w2,0]]).reshape(-1,1,2)
    #transform corner points of image2
    corner2_perspective=cv2.perspectiveTransform(corner2,H)
    
    pts=np.concatenate((corner1,corner2_perspective),axis=0)

    #calculate the size of output image
    [xmin,ymin]=np.int32(pts.min(axis=0).ravel())
    [xmax,ymax]=np.int32(pts.max(axis=0).ravel())

    #calculate new homography matrix to transform the image to positive coordinate
    #first applying shifting and the apply transformation
    new_H=np.array([[1,0,-xmin],[0,1,-ymin],[0,0,1]]).dot(H)
    result=cv2.warpPerspective(img2,new_H,(xmax-xmin,ymax-ymin))



    #stitching 2 images
    #result[-ymin:h1-ymin, -xmin:w1-xmin] = img1
    #return result
    

    
    
    cv2.imshow('image2',img2)
    cv2.imshow('image1',img1)
    #cv2.imshow('matches',draw_Matches)
    cv2.imshow('result',result)
    key=cv2.waitKey(0)
    if(key==ord('q')):
        cv2.destroyAllWindows()    
    






if __name__=='__main__':
    img1=cv2.imread('./figs/fig0.jpg')
    img2=cv2.imread('./figs/fig1.jpg')
    if img1 is None or img2 is None:
        print("Error: can't read images.")
    stitching(img1,img2)


