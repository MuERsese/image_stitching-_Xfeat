import cv2


#this program using laplacian transform to detect motion blur

def cal_laplacian_var(frame):
    frame_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    laplacian_var=cv2.Laplacian(frame_gray,cv2.CV_64F).var()
    print("laplacian_var is:", laplacian_var)
    return laplacian_var








# if __name__=='__main__':
    