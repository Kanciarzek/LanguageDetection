import os
import random

OUPTUT_PATH = "/home/tskrzypczak/Desktop/dataset_voice/"
VALID_FOLDERNAME = "validation"


def create_validation():
    val_folder_path = os.path.join(OUPTUT_PATH, VALID_FOLDERNAME) 
    os.makedirs(val_folder_path, exist_ok=True)

    for lang_fold in os.listdir(OUPTUT_PATH):
        if lang_fold is not "VALID_FOLDERNAME":
            lang_path = os.path.join(OUPTUT_PATH, lang_fold)
            fnames = os.listdir(lang_path)
            
            random.shuffle(fnames)
            
            val_samples_no = int(len(fnames) * 0.2)
            validation_fnames = fnames[:val_samples_no]
            print(len(validation_fnames))
            
            for fname in validation_fnames:
                to_move_file = os.path.join(lang_path, fname)
                dest_path = os.path.join(val_folder_path, fname)
                os.rename(to_move_file, dest_path)
    

create_validation()