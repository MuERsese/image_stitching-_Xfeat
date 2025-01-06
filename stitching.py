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
        #first we need to initialize to set up the value of min and max
        init_h,init_w,_=key_frame[0].shape
        min_x=0
        max_x=init_w
        min_y=0
        max_y=init_h

        #first calculate all homography matrix
        for i in range(1,n):
            homography[i]=homography[i].dot(homography[i-1])
            
            
        #create an empty canva for output
        #first define the size of output
        h, w ,_= key_frame[0].shape
        corners = np.float32([[0, 0], [w, 0], [0, h], [w, h]]).reshape(-1, 1, 2)

        # calculate the perspective corners
        #suppose lats image is the right most image
        transformed_corners = cv2.perspectiveTransform(corners, homography[-1])
        
        
       
        
        
        output_H = max(max_x,int(np.max(transformed_corners[:, 0, 0])))
        output_W = max(max_y,int(np.max(transformed_corners[:, 0, 1])))
        output=np.zeros((output_H,output_W,3),dtype=np.uint8)
        #initialization of the first image
        output[0:key_frame[0].shape[0],0:key_frame[0].shape[1]]=key_frame[0]



        for j in range(1,n):
            # Get the original dimensions of the key frame
            

            # Define the corners of the image
            corners = np.float32([[0, 0], [w, 0], [0, h], [w, h]]).reshape(-1, 1, 2)

            # calculate the perspective corners
            transformed_corners = cv2.perspectiveTransform(corners, homography[j])

            
            min_x = min(min_x,int(np.min(transformed_corners[:, 0, 0])))
            max_x = max(max_x,int(np.max(transformed_corners[:, 0, 0])))
            min_y = min(min_y,int(np.min(transformed_corners[:, 0, 1])))
            max_y = max(max_y,int(np.max(transformed_corners[:, 0, 1])))

            # Calculate width and height of output
            width = max_x - min_x
            height = max_y - min_y
            dsize = (width, height)
            
            
            output[min_y:height+min_y,min_x:width+min_x]=cv2.warpPerspective(key_frame[i],homography[i],dsize)

        
        return output

        
            
        

