python preprocess.py --img_glob "assets/$img_glob" --output_dir "preprocessed/" $extra_params
python inference.py --pth "$model_checkpoint" --img_glob "preprocessed/${image_file}_aligned_rgb.png" --output_dir "inferred/" --visualize --no_cuda
python layout_viewer.py --img "preprocessed/${img}_aligned_rgb.png" --layout "inferred/${img}_aligned_rgb.json" --vis $extra_params
