import gzip
import shutil

def compress_csv(input_csv_path, output_gz_path):
    """
    Compress a CSV file using gzip.

    Parameters:
    input_csv_path (str): The path to the input CSV file.
    output_gz_path (str): The path to the output compressed file (.gz).
    """
    with open(input_csv_path, 'rb') as f_in:
        with gzip.open(output_gz_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# Example usage
input_csv_path = 'planetary_angle_differences.csv'
output_gz_path = 'planetary_angle_differences_compressed.csv.gz'
compress_csv(input_csv_path, output_gz_path)
