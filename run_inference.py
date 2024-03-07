

from nnunetv2.evaluation.find_best_configuration import find_best_configuration
from nnunetv2.inference.predict_from_raw_data import predict
# Use if multiple training types were run
# best_configurations = find_best_configuration(dataset_name_or_id='101')
print(f'WARNING: This script does not work at the moment because predict looks for the name of the entrypoint function '
      f'to define relative paths. The error message is very unclear.')

# nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_NAME_OR_ID -c CONFIGURATION
predict(input_folder='/data/nnUnet/raw/Dataset101_anatomic/imagesTs',
        output_folder='/data/nnUnet/predictions/Dataset101_anatomic_val',
        dataset_id='101', configuration='3d_fullres', folds_to_use=(0,))


