from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score
from scipy.stats import ttest_rel

from src.interpreter import Interpreter
import os

PROGRAMS_DIRECTORY = 'programs/'


def calculate_metrics(test_results):
    true_labels = []
    syntactic_results = []
    semantic_results = []

    for result in test_results:
        if result["program"].startswith('h'):
            true_labels.append(True)
        elif result["program"].startswith('nh'):
            true_labels.append(False)

        syntactic_results.append(result["syntactic_analysis_result"])
        semantic_results.append(result["semantic_analysis_result"])

    syntactic_confusion_matrix = confusion_matrix(true_labels, syntactic_results)
    semantic_confusion_matrix = confusion_matrix(true_labels, semantic_results)

    syntactic_precision = precision_score(true_labels, syntactic_results)
    syntactic_recall = recall_score(true_labels, syntactic_results)
    syntactic_f1 = f1_score(true_labels, syntactic_results)

    semantic_precision = precision_score(true_labels, semantic_results)
    semantic_recall = recall_score(true_labels, semantic_results)
    semantic_f1 = f1_score(true_labels, semantic_results)

    return {
        "syntactic_confusion_matrix": syntactic_confusion_matrix,
        "syntactic_precision": syntactic_precision,
        "syntactic_recall": syntactic_recall,
        "syntactic_f1": syntactic_f1,

        "semantic_confusion_matrix": semantic_confusion_matrix,
        "semantic_precision": semantic_precision,
        "semantic_recall": semantic_recall,
        "semantic_f1": semantic_f1,
    }

def calculate_ttest(test_results):
    syntactic_runtimes = [result["syntactic_analysis_runtime"] for result in test_results]
    semantic_runtimes = [result["semantic_analysis_runtime"] for result in test_results]

    _, ttest_p_value = ttest_rel(syntactic_runtimes, semantic_runtimes)
    return ttest_p_value


def test_all():
    filenames = os.listdir(PROGRAMS_DIRECTORY)
    interpreter = Interpreter()
    rows = []
    
    for filename in filenames:
        if filename.endswith('.bf'):
            input = 'hello'
            file_path = os.path.join(PROGRAMS_DIRECTORY, filename)
            with open(file_path, 'r') as file:
                
                row = {"program": filename}
                
                # syntactic
                syntactic_analysis_result = True # = positive = halting 
                try:
                    interpreter(file_path, input=input, analysis='syntactic')
                except SystemError:
                    syntactic_analysis_result = False 
                
                row["syntactic_analysis_runtime"] = round(interpreter.analysis_runtime,3)

                    
                # semantic
                semantic_analysis_result = True # = positive = halting 
                try:
                    interpreter(file_path, input=input, analysis='semantic')
                except SystemError:
                    semantic_analysis_result = False
                
                row["semantic_analysis_runtime"] = round(interpreter.analysis_runtime,3)
                
                if filename.startswith('h'): # halting = must be true
                    if syntactic_analysis_result:
                        row["syntactic_analysis_result"] = syntactic_analysis_result # correct
                    else:
                        row["syntactic_analysis_result"] = False
                    if semantic_analysis_result:
                        row["semantic_analysis_result"] = semantic_analysis_result # correct
                    else:
                        row["semantic_analysis_result"] = False

                if filename.startswith('nh'): # non-halting = must be false
                    if not syntactic_analysis_result:
                        row["syntactic_analysis_result"] = syntactic_analysis_result # correct
                    else:
                        row["syntactic_analysis_result"] = False
                    if not semantic_analysis_result:
                        row["semantic_analysis_result"] = semantic_analysis_result # correct
                    else:
                        row["semantic_analysis_result"] = False
                
                rows.append(row)
    return rows 

if __name__ == '__main__':
    tests = test_all()
    print(len(tests))
    metrics = calculate_metrics(tests)
    ttest_p_value = calculate_ttest(tests)

    print("Syntactic Confusion Matrix:")
    print(metrics["syntactic_confusion_matrix"])
    print("Syntactic Precision:", metrics["syntactic_precision"])
    print("Syntactic Recall:", metrics["syntactic_recall"])
    print("Syntactic F1 Score:", round(metrics["syntactic_f1"],3))

    print("\nSemantic Confusion Matrix:")
    print(metrics["semantic_confusion_matrix"])
    print("Semantic Precision:", metrics["semantic_precision"])
    print("Semantic Recall:", metrics["semantic_recall"])
    print("Semantic F1 Score:", round(metrics["semantic_f1"],3))

    print("\nT-test p-value:", round(ttest_p_value,3))