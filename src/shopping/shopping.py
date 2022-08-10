import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence_list = []
    labels_list = []
    interger_index = [0, 2, 4, 11, 12, 13, 14]
    floating_index = [1, 3, 5, 6, 7, 8, 9]
    month_index = 10
    bool_index = [15 ,16]
    month = {"Jan": 0, "Feb": 1, "Mar": 3, "Apr": 4, "May": 5, "June": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    value = {"New_Visitor": 0, "Returning_Visitor": 1, "FALSE": 0, "TRUE": 1, "Other": 0}
    with open(filename) as file:
        data_reader = csv.reader(file)
        next(data_reader)
        for data in data_reader:
            evidence = []
            for i in range(17):
                if i in interger_index:
                    evidence.append(int(data[i]))
                elif i in floating_index:
                    evidence.append(float(data[i]))
                elif i == month_index:
                    evidence.append(month[data[i]])
                elif i in bool_index:
                    evidence.append(value[data[i]])
            evidence_list.append(evidence)
            labels_list.append(value[data[17]])
    
    return (evidence_list, labels_list)
                

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_labels_count = 0
    false_labels_count = 0
    true_predict_count = 0
    false_predict_count = 0
    for actual, predict in zip(labels, predictions):
        true_labels_count = true_labels_count + (1 if actual == 1 else 0)
        false_labels_count = false_labels_count + (1 if actual == 0 else 0)
        if actual == predict == 1:
            true_predict_count += 1
        if actual == predict == 0:
            false_predict_count += 1
    sensitivity = true_predict_count / true_labels_count
    specificity = false_predict_count / false_labels_count
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
