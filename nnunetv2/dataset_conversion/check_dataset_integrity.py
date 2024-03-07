import os
from pathlib import Path
import numpy as np

from nnunetv2.training.dataloading.nnunet_dataset import nnUNetDataset
from batchgenerators.utilities.file_and_folder_operations import load_json


def qc_data_loading(preprocessed_dataset_folder, splits_file):
    if isinstance(preprocessed_dataset_folder, str):
        preprocessed_dataset_folder = Path(preprocessed_dataset_folder)
    splits = load_json(splits_file)
    tr_cases = splits[0]['train']
    val_cases = splits[0]['val']
    case_identifiers = tr_cases + val_cases

    dataset = nnUNetDataset(preprocessed_dataset_folder, case_identifiers=case_identifiers,
                                        num_images_properties_loading_threshold=0,
                                        folder_with_segs_from_previous_stage=None)
    ids_actual_images = [name for name in preprocessed_dataset_folder.glob('*.npy') if
                               not str(name).endswith('_seg.npy')]
    ids_actual_labels = [name for name in preprocessed_dataset_folder.glob('*.npy') if
                               str(name).endswith('_seg.npy')]
    ids_actual_properties = [name for name in preprocessed_dataset_folder.glob('*.pkl')]

    assert len(ids_actual_images) == len(ids_actual_labels) == len(ids_actual_properties), ('Some files have incomplete '
                                                                                            'triplets')

    for j, current_key in enumerate(case_identifiers):
        try:
            data, seg, properties = dataset.load_case(current_key)
            # print(f"Loaded case {current_key}")
        except:
            print(f"Failed to load case {current_key}")


if __name__ == '__main__':
    preprocessed_dataset_folder = r'D:\data\nnUnet\nnUNet_preprocessed\Dataset501_BloodVesselSegmentation\nnUNetPlans_2d'
    splits_file = r"D:\data\nnUnet\nnUNet_preprocessed\Dataset501_BloodVesselSegmentation\splits_final.json"
    qc_data_loading(preprocessed_dataset_folder=preprocessed_dataset_folder, splits_file=splits_file)
