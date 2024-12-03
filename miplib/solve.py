import highspy
import gurobipy as gp
from instance import get_instance_info, get_instance_path, get_instance_names
from logger import logger
from tabulate import tabulate

def print_info(info):
    # Get all attributes that don't start with '_' (non-private attributes)
    for attr in dir(info):
        if not attr.startswith('_'):  # Skip private/magic methods
            value = getattr(info, attr)
            print(f"{attr}: {value}")

def solve(instance_name: str=None, time_limit: int=20):
    if instance_name is None:
        filter = {
            "difficulty" : "easy",
            # "n_binary_variables" : "0",
            # "n_integer_variables" : "0",
        }
        instance_names = get_instance_names(filter)
        if not len(instance_names):
            raise RuntimeError("Couldn't find any instances with the given filter")
        instance_name = instance_names.sample().values[0]
    instance_info_str = tabulate(get_instance_info(instance_name), headers='keys', tablefmt='psql', showindex=False)
    logger.info(f"Solving instance {instance_name}\n" + instance_info_str)
    instance_path = get_instance_path(instance_name)
    model = highspy.Highs()
    model.setOptionValue("time_limit", time_limit)
    model.setOptionValue("solver", "ipm")
    model.readModel(str(instance_path))
    model.run()
    highs_info = model.getInfo()
    print_info(highs_info)
    model.clear() 
    return highs_info

def solve_gurobi(instance_name: str=None, time_limit: int=20):
    if instance_name is None:
        filter = {
            "difficulty" : "easy",
            # "n_binary_variables" : "0",
            # "n_integer_variables" : "0",
        }
        instance_names = get_instance_names(filter)
        if not len(instance_names):
            raise RuntimeError("Couldn't find any instances with the given filter")
        instance_name = instance_names.sample().values[0]
    instance_info_str = tabulate(get_instance_info(instance_name), headers='keys', tablefmt='psql', showindex=False)
    logger.info(f"Solving instance {instance_name}\n" + instance_info_str)
    instance_path = get_instance_path(instance_name)
    model = gp.read(str(instance_path))
    lp_root = model.relax()
    lp_root.optimize()
