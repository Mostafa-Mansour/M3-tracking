import os
import argparse
import shutil


def rename_files(data_path_src:str, data_path_dest:str ):
    for file_name in os.listdir(data_path_src):
        dest_name = file_name[5:]
        src_file = os.path.join(data_path_src, file_name)
        dest_file = os.path.join(data_path_dest, dest_name)
        shutil.copyfile(src_file,dest_file)

def text_parser(input_file:str , output_file:str):
    with open(input_file) as f1, open(output_file, "a") as f2:
        lines = f1.readlines()
        for line in lines:
            stripped_line = line.strip()
            print(stripped_line)
            output_line = stripped_line[5:]+"\n"
            f2.write(output_line)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="name parser")
    parser.add_argument("--src_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--input_txt", default=None)
    parser.add_argument("--output_txt", default=None)

    args = parser.parse_args()

    src_dir = args.src_dir
    dest_dir = args.output_dir

    #rename_files(src_dir, dest_dir)
    if not (args.input_txt is None) and not (args.output_txt is None):
        text_parser(args.input_txt, args.output_txt)

