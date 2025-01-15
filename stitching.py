import cv2
import numpy as np



class stitching:
    def __init__(self):
        pass
    def stitching(self,key_frame,homography,n):
        if(n==0):
            print("no keyframes detected")
            return None

    

        #we assume that all images have the same shape, so their corners are the same
        h,w,_=key_frame[0].shape
        
        transformed_corners=[]
        corners = np.float32([[0, 0], [w-1, 0], [0, h-1], [w-1, h-1]]).reshape(-1, 1, 2)
        transformed_corners.append(corners)
        

        #first calculate all homography matrix,and store the transformed corners
        for i in range(1,n):
            homography[i]=homography[i].dot(homography[i-1])
            transformed_corners.append(cv2.perspectiveTransform(corners, homography[i]))
            
        #now we need to find xmin,xmax,ymin,ymax
       
        xmin_output=int(np.min(np.array(transformed_corners)[:,:,:,0]))
        xmax_output=int(np.max(np.array(transformed_corners)[:,:,:,0]))
        ymin_output=int(np.min(np.array(transformed_corners)[:,:,:,1]))
        ymax_output=int(np.max(np.array(transformed_corners)[:,:,:,1]))

        #create an empty canva for the output
        output=np.zeros((ymax_output-ymin_output,xmax_output-xmin_output,3),dtype=np.uint8)
        weight_map = np.zeros((ymax_output-ymin_output, xmax_output-xmin_output), dtype=np.float32)
        
        #now calculate the coordinate homography matrix,make the point go to (0,0)
        #this won't change the size of output canva

        
        coor_homo=np.array([[1,0,-xmin_output],[0,1,-ymin_output],[0,0,1]],dtype=np.float32)

    
        #clculate the perspective image and then stitch them to the output
        
        for k in range(n-1,-1,-1):
            #we need to decide dsize(the w and h of the output frame)
            #we need to recalculate all corners,because the homography changed
            
            
            
            
            # [xmin,ymin]=np.int32(corners_cur.min(axis=0).ravel())
            # [xmax,ymax]=np.int32(corners_cur.max(axis=0).ravel())
            # dsize=(xmax - xmin , ymax - ymin)
            dsize=(xmax_output-xmin_output,ymax_output-ymin_output)
            key_frame_homo_=cv2.warpPerspective(key_frame[k],coor_homo.dot(homography[k]),dsize)
             # Create masks for blending
           

            # Blend using masks,full opacity
            mask = cv2.warpPerspective(np.ones((h, w), dtype=np.float32), homography[k], dsize)

            # Blend the current image with the existing canvas
            output = output + key_frame_homo_ * mask[:, :, None]  # Add weighted image
            weight_map += mask  # Accumulate weights

            print(f"Frame {k} added successfully, size: {key_frame_homo_.shape}")

        # Normalize the output by the weight map to handle overlaps
        weight_map[weight_map == 0] = 1  # Avoid division by zero
        output = (output / weight_map[:, :, None]).astype(np.uint8)
        

        return output

        
            
        

