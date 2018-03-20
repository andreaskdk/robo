import numpy as np

tickTime=1.0
miniTickTime=0.1
maxMoveTime=5.0

camera_matrix=np.array([[320.,   0., 160.],
                [  0., 320., 120.],
                [  0.,   0.,   1.]])

dist_coefs=np.zeros((4,1))