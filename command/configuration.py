import numpy as np

tickTime=1.0
miniTickTime=0.1
maxMoveTime=5.0

imageWidth=320
imageHeight=240

camera_matrix=np.array([[320.,   0., 160.],
                [  0., 320., 120.],
                [  0.,   0.,   1.]])

dist_coefs=np.zeros((4,1))


cTr=np.array([[ 2.82151473e-02, -9.99566606e-01,  8.39674170e-03, -1.91238966e+00],
              [-1.92662456e-01, -1.36805574e-02, -9.81169720e-01,  1.73301875e+01],
             [ 9.80859360e-01,  2.60661113e-02, -1.92964956e-01,  1.47707319e+01],
[ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])
