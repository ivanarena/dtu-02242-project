import pandas as pd
from src.interpreter import Interpreter
import os
from sklearn.metrics import classification_report
from scipy.stats import ttest_rel

PROGRAMS_DIRECTORY = 'programs/'


# Define the functions to get the true positives, false positives, false negatives, and true negatives
def get_true_positives(df, result_column):
    return df[(df['halting'] == True) & (df[result_column] == True)].shape[0]

def get_false_positives(df, result_column):
    return df[(df['halting'] == False) & (df[result_column] == True)].shape[0]

def get_false_negatives(df, result_column):
    return df[(df['halting'] == True) & (df[result_column] == False)].shape[0]

def get_true_negatives(df, result_column):
    return df[(df['halting'] == False) & (df[result_column] == False)].shape[0]


def test_one(filename):
    interpreter = Interpreter()
    input_data = 'hello'
    file_path = os.path.join(PROGRAMS_DIRECTORY, filename)

    row = {"program": filename}

    # Syntactic analysis
    syntactic_analysis_result = True  # Positive = halting
    try:
        interpreter(file_path, input=input_data, analysis='syntactic')
    except SystemError:
        syntactic_analysis_result = False

    row["syntactic_analysis_runtime"] = round(interpreter.analysis_runtime, 3)

    # Semantic analysis
    semantic_analysis_result = True  # Positive = halting
    try:
        interpreter(file_path, input=input_data, analysis='semantic')
    except SystemError:
        semantic_analysis_result = False

    row["semantic_analysis_runtime"] = round(interpreter.analysis_runtime, 3)

    # Halting or non-halting check
    if filename.startswith('h'):
        row["syntactic_analysis_result"] = syntactic_analysis_result
        row["semantic_analysis_result"] = semantic_analysis_result
    elif filename.startswith('nh'):
        row["syntactic_analysis_result"] = not syntactic_analysis_result
        row["semantic_analysis_result"] = not semantic_analysis_result

    return row

def test_all():
    filenames = os.listdir(PROGRAMS_DIRECTORY)
    interpreter = Interpreter()
    rows = []
    
    for filename in filenames:
        if filename.endswith('.bf'):
            halting = ''
            if filename.startswith('h'):
                halting = True
            elif filename.startswith('nh'):
                halting = False

            input = 'hello'
            file_path = os.path.join(PROGRAMS_DIRECTORY, filename)
            with open(file_path, 'r') as file:
                
                row = {"program": filename, "halting": halting}
                
                # syntactic
                syntactic_analysis_result = True 
                try:
                    interpreter(file_path, input=input, analysis='syntactic')
                except SystemError:
                    syntactic_analysis_result = False 
                
                row["syntactic_analysis_runtime"] = round(interpreter.analysis_runtime,3)

                    
                # semantic
                semantic_analysis_result = True
                try:
                    interpreter(file_path, input=input, analysis='semantic')
                except SystemError:
                    semantic_analysis_result = False
                
                row["semantic_analysis_runtime"] = round(interpreter.analysis_runtime,3)

                row["syntactic_analysis_result"] = syntactic_analysis_result 
                row["semantic_analysis_result"] = semantic_analysis_result
                

                rows.append(row)
    return rows 

if __name__ == '__main__':
    tests = test_all()
    df = pd.DataFrame(tests).sort_values(by='program')
    # Calculate metrics for syntactic analysis
    syntactic_tp = get_true_positives(df, 'syntactic_analysis_result')
    syntactic_fp = get_false_positives(df, 'syntactic_analysis_result')
    syntactic_fn = get_false_negatives(df, 'syntactic_analysis_result')
    syntactic_tn = get_true_negatives(df, 'syntactic_analysis_result')

    # Calculate metrics for semantic analysis
    semantic_tp = get_true_positives(df, 'semantic_analysis_result')
    semantic_fp = get_false_positives(df, 'semantic_analysis_result')
    semantic_fn = get_false_negatives(df, 'semantic_analysis_result')
    semantic_tn = get_true_negatives(df, 'semantic_analysis_result')

    # Print the classification report
    print("Syntactic Analysis Results:")
    print(classification_report(df['syntactic_analysis_result'], df['halting']))

    print("Semantic Analysis Results:")
    print(classification_report(df['semantic_analysis_result'], df['halting']))

    # Assuming df is your DataFrame with the given dataset
    runtime_t_statistic, runtime_p_value = ttest_rel(df['syntactic_analysis_runtime'], df['semantic_analysis_runtime'])
    result_t_statistic, result_p_value = ttest_rel(df['syntactic_analysis_result'].astype(int), df['semantic_analysis_result'].astype(int))


    print("Runtime T-Statistic:", runtime_t_statistic)
    print("Runtime P-Value:", runtime_p_value)
    print("Result T-Statistic:", result_t_statistic)
    print("Reuslt P-Value:", result_p_value)

    from scipy.stats import chi2_contingency, chi2

    # Create a contingency table
    contingency_table = pd.crosstab(df['syntactic_analysis_result'], df['semantic_analysis_result'])

    # Perform McNemar test
    chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)

    print("Chi-Square for McNemar Test:", chi2_stat)
    print("P-Value for McNemar Test:", p_value)
    
    
    print(df)