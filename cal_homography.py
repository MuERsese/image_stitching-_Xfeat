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
        inliers = inliers.flatten() > 0

        #find good matches
        kp1 = [cv2.KeyPoint(p[0],p[1], 5) for p in points1[inliers]]
        kp2 = [cv2.KeyPoint(p[0],p[1], 5) for p in points2[inliers]]
        good_matches = [cv2.DMatch(i,i,0) for i in range(len(kp1))]
        #matches = cv2.drawMatches(img1, kp1,img2, kp2, good_matches, None, matchColor=(0, 200, 0), flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    
    
        
        
        #get the projection of img2 to img1
        # #get the corners of two images
        corner1=np.float32([[0,0],[0,h1],[w1,h1],[w1,0]]).reshape(-1,1,2)
        corner2=np.float32([[0,0],[0,h2],[w2,h2],[w2,0]]).reshape(-1,1,2)
        #transform corner points of image2
        corner2_perspective=cv2.perspectiveTransform(corner2,H)
        
        pts=np.concatenate((corner2_perspective,corner1),axis=0)

        #calculate the size of output image
        [xmin,ymin]=np.int32(pts.min(axis=0).ravel())
        [xmax,ymax]=np.int32(pts.max(axis=0).ravel())

        #calculate new homography matrix to transform the image to positive coordinate
        new_H=np.array([[1,0,-xmin],[0,1,-ymin],[0,0,1]]).dot(H)
        
        #return result H21
        return H
        
        
        
        # img2_perspective=cv2.warpPerspective(img2,new_H,(xmax-xmin,ymax-ymin))
        # img2_perspective_1=cv2.warpPerspective(img2,H,(xmax-xmin,ymax-ymin))

       
      
        


        
        
        #return result
        
        
        # # #cv2.imshow('matched image',matches)
        # cv2.namedWindow('image1',cv2.WINDOW_NORMAL)
        # cv2.imshow('image1',img1)
        # # cv2.imshow('image2',img2)
        # cv2.namedWindow('image2_perspective',cv2.WINDOW_NORMAL)
        # cv2.imshow('image2_perspective',img2_perspective)
        # cv2.namedWindow('image2_perspective_1',cv2.WINDOW_NORMAL)
        # cv2.imshow('image2_perspective_1',img2_perspective)
        # # #cv2.imshow('stitched_output',stitched_output)
        
        
        # key=cv2.waitKey(0)
        # if(key==ord('q')):
        #     cv2.destroyAllWindows()    
        






if __name__=='__main__':
    stitcher=cal_homography()
    img1=cv2.imread('./figs/fig0.jpg')
    img2=cv2.imread('./figs/fig1.jpg')
    stitcher.cal_homography(img1,img2)
    #print(H)
    if img1 is None or img2 is None:
        print("Error: can't read images.")
    


