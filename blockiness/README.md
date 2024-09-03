# Blockiness Distribution

## Calculate blockiness measure
You can caluculate blockiness measure per image.
```sh
python calculate_blockiness.py --root /path/to/your_dataset --output /path/to/blockiness_results.txt --suffix your_suffix
```
Example Usage:
```sh
python calculate_blockiness.py --root datasets/my_images --output results/blockiness_results.txt --suffix jpg
```
## Estimate blockiness distribution
You can estimate blockiness distribution per dataset from a text file.
```sh
python estimate_blokiness_distribution_from_text.py --visualize --config_target_dataset /path/to/target_blockiness.yml --config_basis_dataset /path/to/basis_blokiness.yml
```
Example Usage:
```sh
python estimate_blokiness_distribution_from_text.py --visualize --config_target_dataset target_dataset_paths.yml --config_basis_dataset basis_dataset_paths.yml
```
