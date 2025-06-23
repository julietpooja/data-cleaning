#Importing raw data
raw_data = [
    ["EMP001", "Saran", 28, "female", "HR", 50000, 2018, 5, "A"],
    ["EMP002", "jeni", None, "Male", "Finance", 60000, 2017, "?", "B"],
    ["EMP003", "jagadees", 35, "", "it", "?", 2016, 8, "C"],
    ["EMP004", "Bavi", 40, "male", "HR", 55000, 2015, 10, "A"],
    ["EMP005", "Barani", 29, "FEMALE", "marketing", 58000, 2019, "?", "B"],
    ["EMP006", "Jana", "N/A", "Male", "IT", 62000, 2020, 2, "A"],
    ["EMP007", "Madhu", 32, "Female", "finance", "NA", 2018, 6, "?"],
    ["EMP008", "Guru", 27, "Female", "Marketing", 57000, "unknown", 3, "B"],
    ["EMP009", "Girish", 31, "male", "", 54000, 2019, 4, "C"],
    ["EMP010", "Akshuu", 30, "Female", "HR", 52000, 2021, 3, "B"],
    ["EMP011", "Divi", 55, "Female", "HR", 150000, 2010, 35, "A"],
    ["EMP011", "JP", 32, "Male", "IT", 230000, 2014 , 24, "A"]
]

headers = ["Employee ID", "Name", "Age", "Gender", "Department", "Salary", "Joining_Year", "Experience", "Performance_Rating"]



def to_number(val):
    try:
        return float(val)
    except:
        return None

ages, salaries, experiences, joining_years = [], [], [], []

for row in raw_data:
    # Age
    age = to_number(row[2]) if str(row[2]).lower() not in ['n/a', 'na', '?', 'none'] else None
    row[2] = age
    if age is not None:
        ages.append(age)

    # Salary
    salary = to_number(row[5]) if str(row[5]).lower() not in ['n/a', 'na', '?', 'none'] else None
    row[5] = salary
    if salary is not None:
        salaries.append(salary)

    # Joining Year
    jy = to_number(row[6]) if str(row[6]).lower() not in ['unknown', '?'] else None
    row[6] = jy
    if jy is not None:
        joining_years.append(jy)

    # Experience
    exp = to_number(row[7]) if str(row[7]).lower() not in ['?', 'na', 'none'] else None
    row[7] = exp
    if exp is not None:
        experiences.append(exp)

def mean(vals):
    return sum(vals) / len(vals)

def median(vals):
    sorted_vals = sorted(vals)
    n = len(sorted_vals)
    mid = n // 2
    return (sorted_vals[mid] if n % 2 == 1 else (sorted_vals[mid - 1] + sorted_vals[mid]) / 2)

for row in raw_data:
    row[2] = row[2] if row[2] is not None else round(mean(ages), 1)
    row[5] = row[5] if row[5] is not None else round(median(salaries), 2)
    row[6] = row[6] if row[6] is not None else round(median(joining_years))
    row[7] = row[7] if row[7] is not None else round(median(experiences))


# Normalize gender
for row in raw_data:
    row[3] = row[3].strip().lower()
    row[3] = 1 if row[3] == "male" else 0

# One-hot encode department
all_departments = set()
for row in raw_data:
    dept = row[4].strip().lower()
    dept = dept if dept else "unknown"
    row[4] = dept
    all_departments.add(dept)

all_departments = list(all_departments)

# Add one-hot columns
encoded_data = []
for row in raw_data:
    base = row[:5]  # first five columns
    for dept in all_departments:
        base.append(1 if row[4] == dept else 0)
    base += row[5:]  # rest of numerical fields
    encoded_data.append(base)

# Encode performance rating
rating_map = {"A": 3, "B": 2, "C": 1, "?": 2}
for row in encoded_data:
    last = row[-1]
    row[-1] = rating_map.get(str(last).upper(), 2)


def min_max_norm(vals):
    min_val, max_val = min(vals), max(vals)
    return [(v - min_val) / (max_val - min_val) for v in vals]

# Find columns: Age=2, Salary=5, Joining Year=6, Experience=7
age_vals = [row[2] for row in encoded_data]
salary_vals = [row[5 + len(all_departments)] for row in encoded_data]
jy_vals = [row[6 + len(all_departments)] for row in encoded_data]
exp_vals = [row[7 + len(all_departments)] for row in encoded_data]

norm_age = min_max_norm(age_vals)
norm_salary = min_max_norm(salary_vals)
norm_jy = min_max_norm(jy_vals)
norm_exp = min_max_norm(exp_vals)

for i in range(len(encoded_data)):
    encoded_data[i][2] = round(norm_age[i], 2)
    encoded_data[i][5 + len(all_departments)] = round(norm_salary[i], 2)
    encoded_data[i][6 + len(all_departments)] = round(norm_jy[i], 2)
    encoded_data[i][7 + len(all_departments)] = round(norm_exp[i], 2)


def detect_outliers(vals):
    vals_sorted = sorted(vals)
    q1 = vals_sorted[len(vals)//4]
    q3 = vals_sorted[3*len(vals)//4]
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return [i for i, v in enumerate(vals) if v < lower or v > upper]

# Example on normalized salary
outliers = detect_outliers([row[5 + len(all_departments)] for row in encoded_data])
final_data = [row for i, row in enumerate(encoded_data) if i not in outliers]

# Print final cleaned data
print("\nCleaned and Encoded Data (no outliers):\n")
for row in final_data:
    print(row)
