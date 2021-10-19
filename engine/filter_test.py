import os
import params
from filter_utils import *
from meas_utils import *
from track_utils import *
from decimal import Decimal
import glob

if __name__ == "__main__":
    data_folder = '/home/mansour/codes/MonoFlex/predictions/inference/kitti_train/data'
    #kf = KF()
    track = Track()
    meas_list = None
    filelist = glob.glob(os.path.join(data_folder, '*.txt'))
    counter = 0


    for file_name in sorted(filelist):
        meas_list = []
        with open(os.path.join(data_folder,file_name), 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                line = list(line.split(" "))
                dim_data = [float(line[8]), float(line[9]), float(line[10])]
                pos_data = [float(line[11]), float(line[12]), float(line[13])]
                meas = Measurement(pos_data, dim_data)
                meas_list.append(meas)
            f.close()

        track.handle_meas(meas_list)





