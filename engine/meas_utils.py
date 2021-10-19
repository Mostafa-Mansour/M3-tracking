import os
import numpy as np
import params
from scipy.stats.distributions import chi2


class Assotiations():
    def __init__(self):
        self.association_matrix = None
        self.unassigned_tracks = []
        self.unassigned_meas = []

    def MHD(self, meas, track, motion_model):
        # temp = meas.get_H() @ track.P
        S = meas.get_H(motion_model) @ track.P @ meas.get_H(motion_model).transpose() + meas.R
        return (meas.z - meas.get_H(motion_model) @ track.X).transpose() @ np.linalg.inv(S) @ (
                    meas.z - meas.get_H(motion_model) @ track.X)

    def gatting(self, meas, MHD):
        dim = meas.z.shape[0]
        return MHD <= chi2.ppf(0.995, df=dim)

    def set_association_matrix(self, track, list_meas, motion_model):
        if motion_model == 'cv':
            N = len(track.track_cv.ids)
            M = len(list_meas)
            ids = list(track.track_cv.ids.keys())
            association_matrix = np.inf * np.ones((N, M))
            for i in range(N):
                track_data = track.track_data(ids[i], motion_model)
                for j in range(M):
                    MHD = self.MHD(list_meas[j], track_data, motion_model)
                    if self.gatting(list_meas[j], MHD[0]):
                        association_matrix[i, j] = MHD[0]
            return association_matrix

    def get_closest_track_meas(self, A):

        if np.min(A) == np.inf or A.size == 0:
            return np.nan, np.nan, np.array([])
        ij_min = np.unravel_index(np.argmin(A, axis=None), A.shape)
        idx_track = ij_min[0]
        idx_meas = ij_min[1]

        A = np.delete(A, idx_track, 0)
        A = np.delete(A, idx_meas, 1)



        return idx_track, idx_meas, A

    def get_associatives(self, track, list_meas, motion_model):

        if motion_model == 'cv':
            ids = list(track.track_cv.ids.keys())
            unassigned_measurements = list_meas
            A = track.track_cv.association_matrix

            while A.shape[0] > 0 and A.shape[1] > 0:

                idx_track, idx_meas, A = self.get_closest_track_meas(A)
                if idx_track is np.nan:
                    track.add_obj(unassigned_measurements)
                    track.update_meas_counter(ids)
                    break
                else:
                    track.track_id[int(ids[idx_track])].cv.meas = unassigned_measurements[idx_meas].z
                    track.track_cv.ids[ids[idx_track]] = 0
                    #ids.remove(idx_track)
                    #unassigned_measurements.remove(idx_meas)
                    del ids[idx_track]
                    del unassigned_measurements[idx_meas]



        elif motion_model == 'ca':
            ids = list(track.track_cv.ids.keys())
            unassigned_measurements = list_meas
            A = track.track_cv.association_matrix

            while A:
                idx_track, idx_meas = self.get_closest_track_meas(A)
                if idx_track is np.nan:
                    track.add_obj(unassigned_measurements)
                    track.update_meas_counter(ids)

                track.track_id[ids[idx_track]].cv.meas = unassigned_measurements[idx_meas]
                ids.remove(idx_track)
                unassigned_measurements.remove(idx_meas)
        else:
            ids = list(track.track_cv.ids.keys())
            unassigned_measurements = list_meas
            A = track.track_cv.association_matrix

            while A:
                idx_track, idx_meas = self.get_closest_track_meas(A)
                if idx_track is np.nan:
                    track.add_obj(unassigned_measurements)
                    track.update_meas_counter(ids)

                track.track_id[ids[idx_track]].cv.meas = unassigned_measurements[idx_meas]
                ids.remove(idx_track)
                unassigned_measurements.remove(idx_meas)


class Measurement():

    def __init__(self, pos_data, dim_data):
        self.z = np.zeros((6, 1))
        self.z[0] = pos_data[0]
        self.z[1] = pos_data[1]
        self.z[2] = pos_data[2]
        self.z[3] = dim_data[0]
        self.z[4] = dim_data[1]
        self.z[5] = dim_data[2]

        sigma_meas_h = params.sigma_meas_h_perc * dim_data[0]
        sigma_meas_w = params.sigma_meas_w_perc * dim_data[1]
        sigma_meas_l = params.sigma_meas_l_perc * dim_data[2]
        self.R = np.zeros((6, 6))
        self.R[0, 0] = params.sigma_meas_x ** 2
        self.R[1, 1] = params.sigma_meas_y ** 2
        self.R[2, 2] = params.sigma_meas_z ** 2
        self.R[3, 3] = sigma_meas_h ** 2
        self.R[4, 4] = sigma_meas_w ** 2
        self.R[5, 5] = sigma_meas_l ** 2

    def get_R(self):
        return self.R

    def get_H(self, motion_model='cv'):

        if motion_model == 'cv':
            self.H = np.zeros((6, 9))
        elif motion_model == 'ca':
            self.H = np.zeros((6, 12))
        elif motion_model == 'stationary':
            self.H = np.zeros((6, 6))
        else:
            raise
        self.H[:6, :6] = np.identity(6)
        return self.H
