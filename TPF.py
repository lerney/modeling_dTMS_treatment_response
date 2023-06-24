import numpy as np
from sklearn.metrics import mean_squared_error


def TPF_classifier(X_train,y_train,X_test,y_test):
    # Calculate the mean feature distribution for each label group
    mean_distributions = []
    for label in np.unique(y_train):
        label_features = X_train.values[y_train == label]
        mean_distribution = np.mean(label_features, axis=0)
        mean_distributions.append(mean_distribution)
    # Predict the label for each test sample
    y_pred = []
    for i in range(len(y_test.values)):
        errors = []
        for mean_distribution, label in zip(mean_distributions, np.unique(y_train)):
            error = np.sqrt(mean_squared_error(X_test.iloc[i].values, mean_distribution))
            errors.append(error)
            # Assign the label with the smallest error to the test sample
        y_pred.append(np.argmin(errors))
    return y_pred


def tpf_topk_classifier(X_train, y_train, X_test, k=5):
    y_pred = []
    for i in range(len(X_test)):
        # get the probability pie chart of the current test example
        test_prob = X_test.iloc[i]
        # initialize the dictionary to store the RMSE values for each train example
        rmse_dict = {}
        # loop over all train examples
        for j in range(len(X_train)):
            # get the probability pie chart of the current train example
            train_prob = X_train.iloc[j]
            # calculate the RMSE between the probability pie charts
            rmse = mean_squared_error(test_prob, train_prob, squared=False)
            # store the RMSE value in the dictionary
            rmse_dict[j] = rmse
        # get the indices of the top K train examples with the minimum RMSE values
        topk_indices = sorted(rmse_dict, key=rmse_dict.get)[:k]
        # get the corresponding labels of the top K train examples
        topk_labels = [y_train.iloc[index] for index in topk_indices]
        # determine the label of the current test example based on the democratic majority of the top K labels
        label, count = np.unique(topk_labels, return_counts=True)
        y_pred.append(label[np.argmax(count)])
    return y_pred


