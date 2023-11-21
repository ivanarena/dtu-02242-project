from scipy.stats import chi2_contingency
import pandas as pd
from src.interpreter import Interpreter
import os
from sklearn.metrics import classification_report
from scipy.stats import ttest_rel

PROGRAMS_DIRECTORY = 'programs/'

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

def generate_classification_report(true_labels, predicted_labels, label_name):
    report = classification_report(true_labels, predicted_labels, target_names=['False', 'True'])
    print(f"{label_name} Analysis Results:")
    print(report)

if __name__ == '__main__':
    tests = test_all()
    df = pd.DataFrame(tests).sort_values(by='program').reset_index(drop=True)

    # Round the runtime values
    df['syntactic_analysis_runtime'] = round(df['syntactic_analysis_runtime'], 3)
    df['semantic_analysis_runtime'] = round(df['semantic_analysis_runtime'], 3)

    # Print the classification reports
    generate_classification_report(df['syntactic_analysis_result'], df['halting'], 'Syntactic')
    generate_classification_report(df['semantic_analysis_result'], df['halting'], 'Semantic')

    # Perform T-test on runtime
    runtime_t_statistic, runtime_p_value = ttest_rel(df['syntactic_analysis_runtime'], df['semantic_analysis_runtime'])
    print("\nRuntime T-Statistic:", round(runtime_t_statistic, 3))
    print("Runtime P-Value:", round(runtime_p_value, 3))

    # Create a contingency table
    contingency_table = pd.crosstab(df['syntactic_analysis_result'], df['semantic_analysis_result'])

    # Perform McNemar test
    chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)
    print("\nChi-Square for McNemar Test:", round(chi2_stat, 3))
    print("P-Value for McNemar Test:", round(p_value, 3))
    
    # Display the DataFrame
    print("\nDataFrame:")
    print(df[['program','halting']])


