import os
import params
from easydict import EasyDict as edict
import numpy as np
from meas_utils import Measurement
class KF():

    def __init__(self):
        self.dt = params.time_step

    def predict(self, track):


        for model in params.motion_models:
            if model == 'cv':
                F = np.identity(9)
                F[0, 6] = self.dt
                F[1, 7] = self.dt
                F[2, 8] = self.dt

                dt = self.dt
                dt2 = dt ** 2
                dt3 = dt ** 3
                sigma2_vx = params.sigma_v_x ** 2
                sigma2_vy = params.sigma_v_y ** 2
                sigma2_vz = params.sigma_v_z ** 2

                Q = np.zeros((9,9))
                Q[0, 0] = dt3 * sigma2_vx/3
                Q[1, 1] = dt3 * sigma2_vy/3
                Q[2, 2] = dt3 * sigma2_vz/3

                Q[0, 6] = dt2 * sigma2_vx/2
                Q[1, 7] = dt2 * sigma2_vy/2
                Q[2, 8] = dt2 * sigma2_vz/2

                Q[6, 0] = dt * sigma2_vx
                Q[7, 1] = dt * sigma2_vy
                Q[8, 2] = dt * sigma2_vz

                Q[6, 6] = sigma2_vx
                Q[7, 7] = sigma2_vy
                Q[8, 8] = sigma2_vz

                ids_list = list(track.track_cv.ids.keys())
                for i in range(len(ids_list)):
                    idx = int(ids_list[i])
                    track.track_id[idx].cv.X = F @ track.track_id[idx].cv.X
                    track.track_id[idx].cv.P = F @ track.track_id[idx].cv.P @ F.transpose() + Q



    def update(self, track):

        for model in params.motion_models:
            if model == 'cv':
                ids_list = list(track.track_cv.ids.keys())

                for i in range(len(ids_list)):
                    idx = int(ids_list[i])
                    track_meas = track.track_id[idx].cv.meas
                    if not track_meas is None:
                        meas = Measurement(track_meas[:3], track_meas[3:])
                        H = meas.get_H(model)
                        R = meas.get_R()
                        S = H @ track.track_id[idx].cv.P @ H.transpose() + R
                        K = track.track_id[idx].cv.P @ H.transpose() @ np.linalg.inv(S)
                        track.track_id[idx].cv.X = track.track_id[idx].cv.X + K @ (meas.z - H @ track.track_id[idx].cv.X)
                        track.track_id[idx].cv.P = (np.identity(9) - K @ H) @ track.track_id[idx].cv.P
                        track.track_id[idx].cv.meas = None

    def KF_dtep(self, track):
        self.predict(track)
        self.update(track)






