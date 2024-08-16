import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm
import statistics
import os
import argparse
import yaml
import numpy as np
from scipy.stats import gaussian_kde
from scipy.special import kl_div
from scipy.spatial.distance import jensenshannon
import math

def load_dataset_paths_from_yaml(yaml_path):
    """Function to load dataset paths from a YAML file"""
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['dataset_paths']

def get_b_values_from_text(file_path):
    """Function to extract blockiness values from a file"""
    values = []
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return values

    try:
        with open(file_path, 'r') as file:
            for line in tqdm(file):
                parts = line.strip().split('\t')
                if len(parts) > 1:
                    try:
                        values.append(float(parts[1]))
                    except ValueError:
                        print(f"Error in converting a value to float in file {file_path}.")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return values

def filter_blockiness_values(values, threshold=300):
    """Function to filter outlier blockiness values"""
    return [x for x in values if x < threshold]

def calculate_median_and_print(dataset_name, values):
    """Function to calculate and print the median"""
    if values:
        median_val = statistics.median(values)
        print(f"{dataset_name}: Median = {median_val}, len = {len(values)}")
    else:
        print(f"{dataset_name}: No valid data found.")

def process_datasets(dataset_paths):
    """Function to process all datasets and store the results in a dictionary"""
    all_data = {}
    for dataset_name, path in dataset_paths.items():
        values = get_b_values_from_text(path)
        calculate_median_and_print(dataset_name, values)
        all_data[dataset_name] = values
    return all_data

def visualize_data(all_data, threshold):
    """Function to visualize the data"""
    plt.rcParams['font.size'] = 12

    for dataset_name in all_data:
        all_data[dataset_name] = filter_blockiness_values(all_data[dataset_name], threshold)

    data = {
        'Datasets': [dataset for dataset, values in all_data.items() for _ in range(len(values))],
        'Blockiness': [value for values in all_data.values() for value in values]
    }

    df = pd.DataFrame(data)

    plt.figure(figsize=(8, 6))
    sns.violinplot(x='Datasets', y='Blockiness', data=df, palette=['#FF0000'])
    plt.ylim(0, threshold)
    plt.savefig("blockiness_comparison.png")

def calculate_average_blockiness(target_blockiness_dict, basis_blockiness_dict, jpeg_quality, threshold=300):
    """Function to calculate KL divergence between datasets"""
    for target_dataset_name, target_blockiness_list in target_blockiness_dict.items():
        kl_list = []
        for (basis_dataset_name, basis_blockiness_list), jpeg in zip(basis_blockiness_dict.items(), jpeg_quality):
            target_dataset_filtered = [x for x in target_blockiness_list if x < threshold]
            target_blockiness_list = target_dataset_filtered

            # Kernel Density Estimation (KDE) to estimate the PDF
            target_blockiness_kde = gaussian_kde(target_blockiness_list)
            basis_blockiness_kde = gaussian_kde(basis_blockiness_list)

            # Common support for PDF evaluation
            x = np.linspace(min(np.min(target_blockiness_list), np.min(basis_blockiness_list)), max(np.max(target_blockiness_list), np.max(basis_blockiness_list)), 3450)

            # Compute the PDFs
            target_blockiness_pdf = target_blockiness_kde(x)
            basis_blockiness_pdf = basis_blockiness_kde(x)

            epsilon = 1e-10
            target_blockiness_pdf += epsilon
            basis_blockiness_pdf += epsilon

            # Calculate Kullback-Leibler (KL) divergence
            kl_divergence = np.sum(kl_div(target_blockiness_pdf, basis_blockiness_pdf))
            print(f'KL Divergence from {target_dataset_name} to {basis_dataset_name} ({jpeg}): {kl_divergence}')
            kl_list.append(kl_divergence)

        df100, df95, df85, df75, df50 = kl_list
        df_sum = sum(math.exp(-1*df) for df in kl_list)
        weighted_sum = (1*math.exp(-1*df100) + 
                        0.95*math.exp(-1*df95) + 
                        0.85*math.exp(-1*df85) + 
                        0.75*math.exp(-1*df75) + 
                        0.5*math.exp(-1*df50)) / df_sum

        print(f'Average Blockiness for {target_dataset_name}: {weighted_sum}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blockiness analysis and visualization")
    parser.add_argument('--visualize', action='store_true', help="Enable visualization of the blockiness data")
    parser.add_argument('--threshold', type=int, default=300, help="Threshold for filtering blockiness values")
    parser.add_argument('--config_target_dataset', type=str, required=True, help="Path to the YAML configuration target datasets file")
    parser.add_argument('--config_basis_dataset', type=str, required=True, help="Path to the YAML configuration basis datasets file")
    
    args = parser.parse_args()

    # Load dataset paths from the YAML configuration file
    target_dataset_paths = load_dataset_paths_from_yaml(args.config_target_dataset)
    basis_dataset_paths = load_dataset_paths_from_yaml(args.config_basis_dataset)
    
    # Process all datasets and calculate the median values
    target_blockiness_dict = process_datasets(target_dataset_paths)
    basis_blockiness_dict = process_datasets(basis_dataset_paths)

    # Perform visualization if the visualize flag is set
    if args.visualize:
        visualize_data(target_blockiness_dict, args.threshold)
        # visualize_data(basis_blockiness_dict, args.threshold)

    # Example of how to call KL divergence calculation

    jpeg_quality = [100, 95, 85, 75, 50]

    calculate_average_blockiness(target_blockiness_dict, basis_blockiness_dict, jpeg_quality, args.threshold)
