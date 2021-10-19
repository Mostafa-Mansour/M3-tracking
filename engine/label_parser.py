import argparse
import os


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))
def get_file_name(file_name: str):
    file_name_num = int(file_name)
    if file_name_num < 10:
        return "00000" + file_name
    elif file_name_num >= 10 and file_name_num < 100:
        return "0000" + file_name
    else:
        return "000" + file_name

def main(label_file:str, output_dir:str)-> None:

    prev_img_id = "-1"
    file_name = None
    output_file = None
    #output_file = os.path.join(output_dir, "label.txt")

    # read file line by line
    with open(label_file) as lf:
        lines = lf.readlines()
        for line in lines:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            if not line_list[0] == prev_img_id:
                file_name_simple = get_file_name(line_list[0])
                file_name = file_name_simple + ".txt"
                output_file = os.path.join(output_dir, file_name)
                prev_img_id = line_list[0]

            with open(output_file, "a") as f:
                f.write(listToString(line_list[2:]))
                f.write("\n")









if __name__=='__main__':
    parser = argparse.ArgumentParser(description="label parser")
    parser.add_argument("--label_file", required=True)
    parser.add_argument("--output_dir", required=True)

    args = parser.parse_args()

    label_file = args.label_file
    output_dir = args.output_dir

    main(label_file, output_dir)