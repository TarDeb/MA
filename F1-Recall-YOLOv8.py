import numpy as np



# Normalized confusion matrix values extracted from the image

matrix = np.array([

    [0.89, 0.03, 0.07, 0.0, 0.0],

    [0.03, 0.90, 0.02, 0.03, 0.0],

    [0.08, 0.07, 0.82, 0.03, 0.0],

    [0.03, 0.0, 0.03, 0.91, 0.0],

    [0.0, 0.0, 0.03, 0.0, 0.94]

])



# precision, recall, and F1 score for all classes

def calculate_metrics(matrix):

    # Precision, Recall, and F1 Score lists

    precision = []

    recall = []

    f1_score = []

    

    # Calculate metrics for each class

    for i in range(len(matrix)):

        TP = matrix[i, i]

        FP = np.sum(matrix[:, i]) - TP

        FN = np.sum(matrix[i, :]) - TP

        prec = TP / (TP + FP) if (TP + FP) > 0 else 0

        rec = TP / (TP + FN) if (TP + FN) > 0 else 0

        f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0

        

        precision.append(prec)

        recall.append(rec)

        f1_score.append(f1)

    

    return precision, recall, f1_score



# Calculate metrics

precision, recall, f1_score = calculate_metrics(matrix)

precision, recall, f1_score
