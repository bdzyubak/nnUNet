import torch
import os

from nnunetv2.run.run_training_api import run_training


def run_training_entry():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_name_or_id', type=str,
                        help="Dataset name or ID to train with")
    parser.add_argument('configuration', type=str,
                        help="Configuration that should be trained")
    parser.add_argument('--fold', type=str, default=0,
                        help='Fold of the 5-fold cross-validation. Should be an int between 0 and 4.')
    parser.add_argument('-tr', type=str, required=False, default='nnUNetTrainer',
                        help='[OPTIONAL] Use this flag to specify a custom trainer. Default: nnUNetTrainer')
    parser.add_argument('-p', type=str, required=False, default='nnUNetPlans',
                        help='[OPTIONAL] Use this flag to specify a custom plans identifier. Default: nnUNetPlans')
    parser.add_argument('-pretrained_weights', type=str, required=False, default=None,
                        help='[OPTIONAL] path to nnU-Net checkpoint file to be used as pretrained model. Will only '
                             'be used when actually training. Beta. Use with caution.')
    parser.add_argument('-num_gpus', type=int, default=1, required=False,
                        help='Specify the number of GPUs to use for training')
    parser.add_argument("--use_compressed", default=False, action="store_true", required=False,
                        help="[OPTIONAL] If you set this flag the training cases will not be decompressed. Reading compressed "
                             "data is much more CPU and (potentially) RAM intensive and should only be used if you "
                             "know what you are doing")
    parser.add_argument('--npz', action='store_true', required=False,
                        help='[OPTIONAL] Save softmax predictions from final validation as npz files (in addition to predicted '
                             'segmentations). Needed for finding the best ensemble.')
    parser.add_argument('--c', action='store_true', required=False,
                        help='[OPTIONAL] Continue training from latest checkpoint')
    parser.add_argument('--val', action='store_true', required=False,
                        help='[OPTIONAL] Set this flag to only run the validation. Requires training to have finished.')
    parser.add_argument('--val_best', action='store_true', required=False,
                        help='[OPTIONAL] If set, the validation will be performed with the checkpoint_best instead '
                             'of checkpoint_final. NOT COMPATIBLE with --disable_checkpointing! '
                             'WARNING: This will use the same \'validation\' folder as the regular validation '
                             'with no way of distinguishing the two!')
    parser.add_argument('--disable_checkpointing', action='store_true', required=False,
                        help='[OPTIONAL] Set this flag to disable checkpointing. Ideal for testing things out and '
                             'you dont want to flood your hard drive with checkpoints.')
    parser.add_argument('-device', type=str, default='cuda', required=False,
                        help="Use this to set the device the training should run with. Available options are 'cuda' "
                             "(GPU), 'cpu' (CPU) and 'mps' (Apple M1/M2). Do NOT use this to set which GPU ID! "
                             "Use CUDA_VISIBLE_DEVICES=X nnUNetv2_train [...] instead!")
    parser.add_argument('--gpu_index', type=int, default=0, required=False,
                        help="Select the index of the gpu to use")
    parser.add_argument('--num_proc', type=str, default="0",
                        help="Select the number of parallel data loading processors. Use 0 for non-parallel debug.")
    parser.add_argument('--load_data_deterministically', action='store_true',
                        help="Randomly sample loading for potentially infinite number of batches, or iterate through "
                             "dataset (best for debug).")
    args = parser.parse_args()

    assert args.device in ['cpu', 'cuda', 'mps'], (f'-device must be either cpu, mps or cuda. Other devices are not '
                                                   f'tested/supported. Got: {args.device}.')
    if args.device == 'cpu':
        # let's allow torch to use hella threads
        import multiprocessing
        torch.set_num_threads(multiprocessing.cpu_count())
        device = torch.device('cpu')
    elif args.device == 'cuda':
        # multithreading in torch doesn't help nnU-Net if run on GPU
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)
        device = torch.device('cuda:' + str(args.gpu_index))
        torch.cuda.set_device(device)
    else:
        device = torch.device('mps')

    if args.num_proc is not None:
        os.environ['nnUNet_n_proc_DA'] = args.num_proc

    run_training(args.dataset_name_or_id, args.configuration, args.fold, args.tr, args.p, args.pretrained_weights,
                 args.num_gpus, args.use_compressed, args.npz, args.c, args.val, args.disable_checkpointing,
                 args.val_best, device=device, infinite=not args.load_data_deterministically)


if __name__ == '__main__':
    run_training_entry()
