import numpy as np
from easydict import EasyDict as edict
import params
from collections import OrderedDict
from meas_utils import *
from filter_utils import *
from output_export import OutputExport


class Track(Assotiations):

    def __init__(self):
        super(Track, self).__init__()
        self.frame_counter = 0

        self.track_list = set()
        self.untracked_list = None
        self.track_id = OrderedDict()
        self.track_cv = edict()
        self.track_cv.ids = {}
        self.track_cv.association_matrix = None
        self.track_cv.id_counter = 0
        self.track_ca = edict()
        self.track_ca.association_matrix = None
        self.track_ca.ids = []
        self.track_ca.id_counter = 0
        self.track_stationary = edict()
        self.track_stationary.association_matrix = None
        self.track_stationary.ids = []
        self.track_stationary.id_counter = 0
        self.id_counter = 0
        self.kf = KF()
        self.data_association = Assotiations()
        self.output_export = OutputExport('/home/mansour/data/results')

    def track_data(self, id, motion_model):
        id = int(id)
        if motion_model == 'cv':
            return self.track_id[id].cv
        elif motion_model == 'ca':
            return self.track_id[id].ca
        elif motion_model == 'stationary':
            return self.track_id[id].stationary
        else:
            raise
    def add_obj(self, list_meas):
        for i in range(len(list_meas)):


            #self.track_id[self.track_] = edict()
            #self.track_id[i].meas = None

            for item in params.motion_models:

                if item == 'cv':

                    self.track_id[self.track_cv.id_counter] = edict()
                    self.track_id[self.track_cv.id_counter].cv = edict()
                    _X = np.zeros((9, 1))
                    _P = np.zeros((9, 9))
                    _P[:6, :6] = list_meas[i].get_R()
                    _P[6, 6] = params.sigma_v_x ** 2
                    _P[7, 7] = params.sigma_v_y ** 2
                    _P[8, 8] = params.sigma_v_z ** 2
                    _X[:6] = list_meas[i].z
                    self.track_id[self.track_cv.id_counter].cv.X = _X
                    self.track_id[self.track_cv.id_counter].cv.P = _P
                    self.track_id[self.track_cv.id_counter].cv.model = 'cv'
                    self.track_id[self.track_cv.id_counter].cv.meas = None
                    self.track_cv.ids[str(self.track_cv.id_counter)] = 0
                    self.track_cv.id_counter += 1


                elif item == 'ca':
                    self.track_id[i].ca = edict()
                    _X = np.zeros((12, 1))
                    _P = np.zeros((12, 12))
                    _P[:6, :6] = list_meas[i].get_R()
                    _P[6, 6] = params.sigma_v_x ** 2
                    _P[7, 7] = params.sigma_v_y ** 2
                    _P[8, 8] = params.sigma_v_z ** 2
                    _P[9, 9] = params.sigma_a_x ** 2
                    _P[10, 10] = params.sigma_a_y ** 2
                    _P[11, 11] = params.sigma_a_z ** 2
                    _X[:6] = list_meas[i].z
                    self.track_id[i].ca.X = _X
                    self.track_id[i].ca.P = _P
                    self.track_id[i].ca.model = 'ca'
                    self.track_ca.ids.append[str(self.track_ca.id_counter)] = 0
                    self.track_ca.id_counter += 1

                else:
                    self.track_id[i].stationary = edict()
                    _X = np.zeros((6, 1))
                    _P = np.zeros((6, 6))
                    _P = list_meas[i].get_R()
                    _X = list_meas[i].z
                    self.track_id[i].stationary.X = _X
                    self.track_id[i].stationary.P = _P
                    self.track_id[i].stationary.model = 'stationary'
                    self.track_stationary.ids.append[str(self.track_stationary.id_counter)] = 0
                    self.track_stationary.id_counter += 1

    def initialize_tracker(self, list_meas):

        for i in range(len(list_meas)):


            self.track_id[i] = edict()
            #self.track_id[i].meas = None

            for item in params.motion_models:

                if item == 'cv':
                    self.track_id[i].cv = edict()
                    _X = np.zeros((9, 1))
                    _P = np.zeros((9, 9))
                    _P[:6, :6] = list_meas[i].get_R()
                    _P[6, 6] = params.sigma_v_x ** 2
                    _P[7, 7] = params.sigma_v_y ** 2
                    _P[8, 8] = params.sigma_v_z ** 2
                    _X[:6] = list_meas[i].z
                    self.track_id[i].cv.X = _X
                    self.track_id[i].cv.P = _P
                    self.track_id[i].cv.model = 'cv'
                    self.track_id[i].cv.meas = None
                    self.track_cv.ids[str(self.track_cv.id_counter)] = 0
                    self.track_cv.id_counter += 1



                elif item == 'ca':
                    self.track_id[i].ca = edict()
                    _X = np.zeros((12, 1))
                    _P = np.zeros((12, 12))
                    _P[:6, :6] = list_meas[i].get_R()
                    _P[6, 6] = params.sigma_v_x ** 2
                    _P[7, 7] = params.sigma_v_y ** 2
                    _P[8, 8] = params.sigma_v_z ** 2
                    _P[9, 9] = params.sigma_a_x ** 2
                    _P[10, 10] = params.sigma_a_y ** 2
                    _P[11, 11] = params.sigma_a_z ** 2
                    _X[:6] = list_meas[i].z
                    self.track_id[i].ca.X = _X
                    self.track_id[i].ca.P = _P
                    self.track_id[i].ca.model = 'ca'
                    self.track_ca.ids.append[str(self.track_ca.id_counter)] = 0
                    self.track_ca.id_counter += 1

                else:
                    self.track_id[i].stationary = edict()
                    _X = np.zeros((6, 1))
                    _P = np.zeros((6, 6))
                    _P = list_meas[i].get_R()
                    _X = list_meas[i].z
                    self.track_id[i].stationary.X = _X
                    self.track_id[i].stationary.P = _P
                    self.track_id[i].stationary.model = 'stationary'
                    self.track_stationary.ids.append[str(self.track_stationary.id_counter)] = 0
                    self.track_stationary.id_counter += 1
            self.track_list.add(i)


    def update_meas_counter(self, list_ids, delete_after = params.delete_after):
        for id in list_ids:
            for model in params.motion_models:
                if model == 'cv':
                    if self.track_cv.ids[id] >= delete_after: #or self.track_ca.ids[id] >= delete_after or self.track_stationary.ids[id] >= delete_after:
                        del self.track_cv.ids[id]
                        #del self.track_ca.ids[str(id)]
                        #del self.track_stationary.ids[str(id)]
                        del self.track_id[int(id)]
                    else:
                        self.track_cv.ids[id] = self.track_cv.ids[id] + 1
                        self.track_id[int(id)].cv.meas = None
                        #self.track_ca.ids[str(id)] = self.track_ca.ids[str(id)] + 1
                        #self.track_stationary.ids[str(id)] = self.track_stationary.ids[str(id)] + 1




    def handle_meas(self, list_meas):

        if not self.track_list:  # list is empty
            self.initialize_tracker(list_meas)
            self.output_export.export_output(self)
            return

        # handle data association
        for model in params.motion_models:
            #self.set_association_matrix(self, list_meas, model)
            if model == 'cv':
                self.track_cv.association_matrix = self.set_association_matrix(self, list_meas, 'cv')
                self.get_associatives(self, list_meas,model)
                self.kf.KF_dtep(self)

            elif model == 'ca':
                self.track_ca.association_matrix = self.set_association_matrix(self, list_meas, 'ca')
                self.get_associatives(self, list_meas,model)

            elif model == 'stationary':
                self.track_stationary.association_matrix = self.set_association_matrix(self, list_meas, 'stationary')
                self.get_associatives(self, list_meas,model)

            else:
                raise
        self.output_export.export_output(self)
