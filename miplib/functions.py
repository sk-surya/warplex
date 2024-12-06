from download import download_if_not_exists, download_miplib_datatable
from unzip import unzip_if_empty
from solve import solve, solve_gurobi


def setup():
    download_if_not_exists()
    unzip_if_empty()
    download_miplib_datatable()


def main():
    setup()
    # solve_gurobi(instance_name="dano3_5", time_limit=10)
    solve(instance_name="dano3_5", time_limit=10)



if __name__ == "__main__":
    main()