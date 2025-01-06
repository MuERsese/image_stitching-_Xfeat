import cv2
import numpy as np

class stitching:
    def __init__(self):
        pass
    def stitching(self,key_frame,homography,n):
        if(n==0):
            print("no keyframes detected")
            return None

        key_frame_homo=[]
        key_frame_homo.append(key_frame[0])

        #we assume that all images have the same shape, so their corners are the same
        h,w,_=key_frame[0].shape
        
        transformed_corners=[]
        corners = np.float32([[0, 0], [w, 0], [0, h], [w, h]]).reshape(-1, 1, 2)
        

        #first calculate all homography matrix,and store the transformed corners
        for i in range(1,n):
            homography[i]=homography[i].dot(homography[i-1])
            transformed_corners.append(cv2.perspectiveTransform(corners, homography[i]))
            
        #now we need to find xmin,xmax,ymin,ymax
       
        xmin_output=int(np.min(np.array(transformed_corners)[:,:,:,0]))
        xmax_output=int(np.max(np.array(transformed_corners)[:,:,:,0]))
        ymin_output=int(np.min(np.array(transformed_corners)[:,:,:,1]))
        ymax_output=int(np.max(np.array(transformed_corners)[:,:,:,1]))

        #now calculate the coordinate homography matrix
        coor_homo=np.array([[1,0,xmin_output],[0,1,ymin_output],[0,0,1]])

        for j in range (n):
            homography[i]=coor_homo.dot(homography[i])
        
        #create an empty canva for the output
        output=np.zeros((ymax_output-ymin_output,xmax_output-xmin_output),dtype=np.uint8)

        #clculate the perspective image and then stitch them to the output
        # for k in range(1,n):
        #     #we need to decide dsize(the w and h of the output frame)


        #     key_frame_homo=cv2.warpPerspective(key_frame[i],homography[i],dsize)






           

        
        return output

        
            
        

