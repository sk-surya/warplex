
import pandas as pd
# from miplib.logger import logger
from path import get_miplib_benchmark_dir
from pathlib import Path


def get_instances_metadata_path() -> Path:
    """Get the path to the instances metadata CSV file."""
    return get_miplib_benchmark_dir() / "data" / "instances.csv"

def process_instances_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "Instance": "instance_name",
        "Status": "difficulty",
        "Variables.": "n_variables",
        "Binaries": "n_binary_variables",
        "Integers": "n_integer_variables",
        "Continuous": "n_continuous_variables",
        "Constraints": "n_constraints",
        "Nonz.": "n_nonzero_coefficients",
        "Submitter": "submitter",
        "Group": "group",
        "Objective": "best_known_objective_value",
        "Tags": "tags",
    })
    df['tags'] = df['tags'].replace(r"\n", " ", regex=True)
    return df

def load_instances_metadata():
    return pd.read_csv(get_instances_metadata_path())