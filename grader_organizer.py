import csv
import os
import argparse
import warnings
import zipfile
from shutil import copy as cp


def pretty_warning(msg, *args, **kwargs):
    """
    Monkey patch for warnings.formatwarning
    """
    return str(msg) + '\n'


def create_grade_csv(target_filepath=None, target_filename="gradebook.csv", num_abc=1, input_file=None) -> str:
    """

    Creates a csv from the given directory containing student names in the first column the first row contains header
    information for the csv (for ease of manual grading/input into a dataframe)

    Supports input csv files containing student names only, or student names and respective abc123s, or (student who
    submitted the file)+all participating abc123s, or directories where you wrote in their names as folders.

    :param target_filepath: path to directory of folders containing student names or file containing student names, if
     "None", scrapes names from folders in current directory

    :param target_filename: name of the output csv file. If unmodified, defaults to "gradebook.csv"

    :param num_abc: number of abc123 columns to be included in the output file, for grading submissions from groups,
     default 1

    :param input_file: csv file to read names from, expected in the format (name,abc123_1,...[new line]) or
     (name[new line]). If "None", function scrapes directory in target_filepath for names


    :return: filename (including directory) of created csv
    """
    # move the operation to the current filepath
    if target_filepath is not None:
        os.chdir(target_filepath)
    filepath = os.getcwd() + os.path.sep  # cross platform compatibility
    filename = filepath + target_filename
    width = 1

    # generate header
    header = ["Students"]
    for i in range(num_abc):
        header.append("abc123-" + str(width))
        width += 1
    header.append("Grade")
    header.append("Comments")

    if input_file is None:
        warnings.formatwarning = pretty_warning
        warnings.warn("Using directory mode, please be sure to manually clean the output file of extraneous names",
                      UserWarning)
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            student_names = [x for x in os.listdir(filepath) if os.path.isdir(x)]
            for name in student_names:
                writer.writerow([name])
    else:
        with open(input_file, 'r', newline='') as csv_read:
            reader = csv.reader(csv_read)
            contents = []
            for row in reader:
                contents.append(row)
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            for row in contents:
                writer.writerow(row)
    return filename


def unzip_files(zipped_dir, target_filepath, allow_top_level=False):
    """
    scans a directory full of folders which contain a zipped submission (zipped_dir), then unzips them into
    target_filepath.

    :param allow_top_level: allows the copying of top level files, I.E files outside of folders, default False
    :param target_filepath: the full path to the output folder, if none, creates an output folder in current directory
    :param zipped_dir: the full path to the input folder, if none, scans current directory for folders containing zips
    :return: the output directory
    """
    # establish target dor
    output_dir = target_filepath
    if target_filepath is None:
        warnings.formatwarning = pretty_warning
        warnings.warn("no output directory given, creating one in current directory labelled \"Unzipped\" ")
        output_dir = os.getcwd() + os.path.sep + "Unzipped"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # establish input dir (ignore the confusingly named variables)
    zipped_filepath = zipped_dir
    if zipped_filepath is None:
        warnings.formatwarning = pretty_warning
        warnings.warn("no input directory given, scanning the current directory for folders containing zipped files ")
        zipped_filepath = os.getcwd()
    os.chdir(zipped_filepath)
    # read zips and extract
    exclude = {'venv', '.idea'}
    exclude_files = {'.gitignore', "grader_organizer.py", '.idea'}
    for root, dirs, files in os.walk(zipped_filepath):  # recursively copy over files and directories into the output
        if str(root).startswith(output_dir):
            break
        dirs[:] = [d for d in dirs if d not in exclude]
        files[:] = [d for d in files if d not in exclude_files]
        dir_prefix = str(root).replace(zipped_filepath + os.path.sep, '', 1)
        new_dir = os.path.join(output_dir, dir_prefix)
        if zipped_filepath == str(root):
            new_dir = output_dir  # this allows top level files to be copied over
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        for name in files:
            if zipped_filepath == str(root) and not allow_top_level:
                continue
            if str(name).endswith(".zip") and zipfile.is_zipfile(os.path.join(root, name)):
                with zipfile.ZipFile(os.path.join(root, name), 'r') as zip_file:
                    zip_file.extractall(os.path.join(new_dir, name))
                    zip_file.close()
            else:
                cp(os.path.join(root, name), os.path.join(new_dir, name))
    return output_dir


def create_folders(input_file, target_directory):  # TODO: COMPLETE THIS FUNCTION AND MAKE IT ROBUST
    if target_directory is None:
        warnings.formatwarning = pretty_warning
        warnings.warn("no output directory given, creating one in current directory labelled \"Students\" ")
        output_dir = os.getcwd() + os.path.sep + "Students"
    else:
        output_dir = target_directory
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    with open(input_file, 'r', newline='') as file_in:
        # read the first word on each line, assuming its a name
        for line in file_in:
            new_path = output_dir + os.path.sep + (line.split(',')[0].strip())
            if not os.path.exists(new_path):
                os.mkdir(new_path)

    return output_dir


parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["csv", "zip", "folder"], help="csv - create grade book; zip - mass unzip; " +
                                                                   " folder - generate name folders from file")
parser.add_argument("-d", "--directory", help="csv mode - directory that student information is stored in;" +
                                              "zip mode - target directory to copy unzipped folders into" +
                                              "; folder mode - directory to write student folders into")
parser.add_argument("-o", "--output",
                    help="name of csv file to be created, do not include directory info here, will be placed in " +
                         "target directory")
parser.add_argument("-n", "--numcollaborators", help="maximum number of collaborators for the assignment")
parser.add_argument("-i", "--inputfile", help="csv mode - filename of student input file, include directory info if "
                                              + "relevant; zip mode - directory containing zip files in student folders"
                    )
parser.add_argument("-tl", "--toplevel", help="allow copying of top level files in zip mode", action='store_true')
parser.set_defaults(toplevel=False, directory=None, inputfile=None, numcollaborators=1, output="gradebook.csv")

args = parser.parse_args()

fun_args = {"target_filepath": args.directory,
            "target_filename": args.output,
            "num_abc": args.numcollaborators,
            "input_file": args.inputfile}
zip_args = {"zipped_dir": args.inputfile,
            "target_filepath": args.directory,
            "allow_top_level": args.toplevel}
folder_args = {"input_file": args.inputfile,
               "target_directory": args.directory}
if int(args.numcollaborators) < 1:
    fun_args["num_abc"] = 1
if str(args.output).split('.')[-1] != ".csv":
    fun_args["target_filename"] = args.output + ".csv"
if args.mode == "csv":
    create_grade_csv(**fun_args)
elif args.mode == "zip":
    unzip_files(**zip_args)
elif args.mode == "folder":
    create_folders(**folder_args)
