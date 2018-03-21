import requests
import time
import base64
import numpy as np
import cv2
import glob


def store_images(n=10):
    for i in range(n):
        r = requests.get('http://robo:5000/getdata')
        data=r.json()["data"]["mostRecentImageData"]["image"]
        with open("chessboardimages/image"+str(i)+".png", "wb") as fh:
            fh.write(data.decode('base64'))
        print(data)
        time.sleep(1)


def calibrate():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    chessboard_size=[7,9]
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboard_size[0]*chessboard_size[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboard_size[0],0:chessboard_size[1]].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob('chessboardimages/*.png')

    for fname in images[1:2]:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (chessboard_size[1],chessboard_size[0]),None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(5,5),(-1,-1),criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (chessboard_size[1],chessboard_size[0]), corners2,ret)
            cv2.imshow('img',img)
            cv2.waitKey(500)

        cv2.destroyAllWindows()

    camera_matrix=np.array([[320.,   0., 160.],
                            [  0., 320., 120.],
                            [  0.,   0.,   1.]])

    dist_coefs=np.zeros((4,1))
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (320, 240),camera_matrix,dist_coefs)
    print(ret)
    print(mtx)
    print(dist)
    print(rvecs)
    print(tvecs)


if __name__=="__main__":
    #store_images(n=60)
    calibrate()