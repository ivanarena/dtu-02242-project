def f_score(tp, fp, fn): # tp - true positive, fp - false positive, fn - false negative
    precision = tp/(tp + fp)
    recall = tp/(tp + fn)
    f1 = 2*(precision*recall)/(precision + recall)
    return f1
