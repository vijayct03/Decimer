import subprocess
from pathlib import Path
import os
import glob
import shutil
import natsort

Project_path = os.path.dirname(__file__)


dataset_path = os.path.join(Project_path, "dataset")
train_path = os.path.join(Project_path, "Image2SMILES/Data/")
line_count = 64
Path(train_path).mkdir(parents=True)

def copy_smiles(in_smiles_path, out_smiles_path, start, end):
    print("batch smile copied")
    f = open(in_smiles_path)
    lines = f.readlines()
    with open(out_smiles_path, "w+") as in_file:
        in_file.write("".join(lines[start:end]))
    


def copy_images(in_img_path, out_img_path, start, end):
    print("batch image copied")
    in_img_path = in_img_path[start:end]
    for image_name in in_img_path:
        shutil.copy(str(image_name), str(out_img_path))


def create_batch(start_line, end_line, dataset_smiles, train_img_path, train_smile_path, images_count):
    train_img_path.mkdir()

    copy_smiles(dataset_smiles, train_smile_path, start_line, end_line)

    copy_images(images_count, train_img_path, start_line, end_line)
    try:
        training = subprocess.call(["python3", "Image2SMILES.py"],
                                   stdout=subprocess.PIPE,
                                   cwd=os.path.join(Project_path, 'Image2SMILES')
                                   )
        if training != 0:
            print("Error in training phase \n")
            
    except Exception as ex:
        print(ex)

    if train_img_path.exists():
        shutil.rmtree(str(train_img_path))

    if train_smile_path.exists():
        train_smile_path.unlink()


print("Training Started")
for dataset_name in os.listdir(dataset_path):
    dataset_images = Path(dataset_path) / dataset_name / "Images"
    dataset_smiles = Path(dataset_path) / dataset_name / "DeepSMILES.txt"
    train_img_path = Path(train_path) / "Train_Images"
    train_smile_path = Path(train_path) / "DeepSMILES.txt"

    images_count = glob.glob(str(dataset_images) + "/*.png")

    images_count = natsort.natsorted(images_count, reverse=False)

    remain_count = len(images_count) % 64

    batch_count = len(images_count) // 64

    start_line = 0
    end_line = line_count
    for i in range(batch_count):
        create_batch(start_line, end_line, dataset_smiles, train_img_path, train_smile_path, images_count)
        start_line = end_line
        if i != batch_count - 1:
            end_line = end_line + line_count
        else:
            end_line = end_line + (remain_count if remain_count != 0 else line_count)

    create_batch(start_line, end_line, dataset_smiles, train_img_path, train_smile_path, images_count)
