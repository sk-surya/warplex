from pathlib import Path
from instance import get_instance_path


def read_mps(file_path: str | Path=None):
    if file_path is None:
        file_path = get_instance_path("sing326")
    with open(file_path, "r") as f:
        lines = f.readlines()
    return lines

def append_to_dict(dict, key, val):
    if key in dict:
        dict[key].append(val)
    else:
        dict[key] = [val]

def get_rows(mps_dict):
    row_dict = {}
    for row in mps_dict["ROWS"]:
        row_items = row.split()
        # print(row_items)
        # assert len(row_items) % 2 == 0
        assert len(row_items) == 2       # per cplex format
        # num_items = int(len(row_items)/2)
        # for i in range(num_items):
        sense, name = row_items[0], row_items[1]
        append_to_dict(row_dict, sense, name)

    # validations
    assert len(row_dict["N"]) == 1              # TODO: if more than one, then take the first one as objective
    assert len(row_dict["L"]) == len(set(row_dict["L"]))
    assert len(row_dict["G"]) == len(set(row_dict["G"]))
    assert len(row_dict["E"]) == len(set(row_dict["E"]))
    assert len(row_dict["N"]) + len(row_dict["L"]) + len(row_dict["G"]) + len(row_dict["E"]) == len(mps_dict["ROWS"])
    return row_dict

def get_column_fields(column_data):
    col_items = column_data.split()
    num_items = len(col_items)
    assert 3 <= num_items <= 5
    col_data_dict = {}

    # FIELD 1: blank
    for i in range(num_items):
        if i == 0:              # FIELD 2: col_name
            col_data_dict["col_name"] = col_items[i]
        elif i == 1:            # FIELD 3: row_1_name
            col_data_dict["row_1_name"] = col_items[i]
        elif i == 2:            # FIELD 4: coefficient for field 2 and 3
            col_data_dict["coefficient_for_col_and_row_1"] = col_items[i]
        elif i == 3:            # FIELD 5: row_2_name
            col_data_dict["row_2_name"] = col_items[i]
        elif i == 4:            # FIELD 6: coefficient for field 2 and 5
            col_data_dict["coefficient_for_col_and_row_2"] = col_items[i]
    return col_data_dict

def get_rhs_fields(rhs_data):
    rhs_items = rhs_data.split()
    num_items = len(rhs_items)
    assert 3 <= num_items <= 6
    rhs_data_dict = {}

    # FIELD 1: blank
    for i in range(num_items):
        if i == 0:              # FIELD 2: rhs_name     ex- 'B' vector (several vectors can be there)
            rhs_data_dict["rhs_name"] = rhs_items[i]
        elif i == 1:            # FIELD 3: row_1_name
            rhs_data_dict["row_1_name"] = rhs_items[i]
        elif i == 2:            # FIELD 4: RHS coefficient for field 2 and 3
            rhs_data_dict["coefficient_for_rhs_and_row_1"] = rhs_items[i]
        elif i == 3:            # FIELD 5: row_2_name
            rhs_data_dict["row_2_name"] = rhs_items[i]
        elif i == 4:            # FIELD 6: RHS coefficient for field 2 and 5
            rhs_data_dict["coefficient_for_rhs_and_row_2"] = rhs_items[i]
    return rhs_data_dict

def get_bounds_fields(bounds_data):
    bounds_items = bounds_data.split()
    num_items = len(bounds_items)
    assert num_items == 4
    bounds_data_dict = {}

    for i in range(num_items):
        if i == 0:              # FIELD 1: type of bound     one of {LO, UP, FX: fixed, FR: free, MI: minus_inf, PL: plus_inf}
            bounds_data_dict["type"] = bounds_items[i]
        elif i == 1:            # FIELD 2: bound idientifier   ex- 'BOUND'
            bounds_data_dict["name"] = bounds_items[i]
        elif i == 2:            # FIELD 3: column (variable) name
            bounds_data_dict["col_name"] = bounds_items[i]
        elif i == 3:            # FIELD 4: value of bound
            bounds_data_dict["value"] = bounds_items[i]
        #FIELD 5: blank
        #FIELD 6: blank
    return bounds_data_dict

def get_ranges_fields(ranges_data):
    ranges_items = ranges_data.split()
    num_items = len(ranges_items)
    assert 3 <= num_items <= 5
    ranges_data_dict = {}

    # FIELD 1: blank
    for i in range(num_items):
        if i == 0:              # FIELD 2: range name     ex- 'RANGE'
            ranges_data_dict["name"] = ranges_items[i]
        elif i == 1:            # FIELD 3: row identifier
            ranges_data_dict["row_1_name"] = ranges_items[i]
        elif i == 2:            # FIELD 4: range value for row 1
            ranges_data_dict["value"] = ranges_items[i]
        elif i == 3:            # FIELD 5: row 2 identifier
            ranges_data_dict["row_2_name"] = ranges_items[i]
        elif i == 4:            # FIELD 5: range value for row 2
            ranges_data_dict["value"] = ranges_items[i]

        #FIELD 5: blank
        #FIELD 6: blank
    return ranges_data_dict

def get_cols(mps_dict):
    col_dict = {}
    for col in mps_dict["COLUMNS"]:
        col_data = get_column_fields(col)
        col_name = col_data["col_name"]
        if col_name == "INT1END":           # TODO -  handle INTEGER VARIABLE 'MARKER'
            continue
        append_to_dict(col_dict, col_name, col_data)

    return col_dict
    
def get_rhs(mps_dict):
    rhs_dict = {}
    for rhs in mps_dict["RHS"]:
        rhs_data = get_rhs_fields(rhs)
        rhs_name = rhs_data["rhs_name"]
        append_to_dict(rhs_dict, rhs_name, rhs_data)

    # if not specified, then cplex assumes 0
    return rhs_dict
    
def get_bounds(mps_dict):
    if "BOUNDS" not in mps_dict:
        return
    bounds_dict = {}
    for bound in mps_dict["BOUNDS"]:
        bounds_data = get_bounds_fields(bound)
        bound_name = bounds_data["name"]
        append_to_dict(bounds_dict, bound_name, bounds_data)

    return bounds_dict

def get_ranges(mps_dict):
    if "RANGES" not in mps_dict:
        return
    ranges_dict = {}
    for ranges in mps_dict["RANGES"]:
        ranges_data = get_ranges_fields(ranges)
        ranges_name = ranges_data["name"]
        append_to_dict(ranges_dict, ranges_name, ranges_data)

    return ranges_dict


if __name__ == "__main__":
    mps_dict = {}
    lines = read_mps()
    indicator = None
    for line in lines:
        if not line[0].isspace():
            indicator = line.split()[0]
            if indicator == "NAME":
                mps_dict[indicator] = line.split()[1]
            else:
                continue
        else:
            append_to_dict(mps_dict, indicator, line)
    
    for k,v in mps_dict.items():
        print(k, len(v))

    print(get_rows(mps_dict))
    print(len(get_cols(mps_dict)))
    print(get_rhs(mps_dict))
    print(get_bounds(mps_dict))
    print(get_ranges(mps_dict))





