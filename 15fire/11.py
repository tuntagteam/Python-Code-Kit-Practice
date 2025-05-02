import pandas as pd

def solve():
    data = [
        {"employee_id": 1, "name": "Alice", "manager_id": 3},
        {"employee_id": 2, "name": "Bob", "manager_id": 3},
        {"employee_id": 3, "name": "Charlie", "manager_id": None},
        {"employee_id": 4, "name": "David", "manager_id": 3},
        {"employee_id": 5, "name": "Eva", "manager_id": 1},
    ]

    df = pd.DataFrame(data)
    df = df.merge(df[["employee_id", "name"]], left_on="manager_id", right_on="employee_id", how="left", suffixes=("", "_manager"))
    df = df[["name", "name_manager"]].rename(columns={"name_manager": "manager_name"})
    print(df)

if __name__ == "__main__":
    solve()