
import os
import params
class OutputExport():
    def __init__(self, output_folder):
        self.output_folder = output_folder




    def export_output(self, track):

        for model in params.motion_models:
            output_file_name = "output_" + model + ".txt"
            output_file_path = os.path.join(self.output_folder, output_file_name)
            if model == 'cv':
                with open(output_file_path, "a+") as f:
                    ids_list = list(track.track_cv.ids.keys())
                    for i in range(len(ids_list)):
                        idx = int(ids_list[i])
                        line = str(track.frame_counter) + " : " + str(idx) + " : " + str(track.track_id[idx].cv.X.ravel()) + "\n"
                        f.write(line)
                    f.write("------------------------------------------------ \n")

            track.frame_counter += 1

