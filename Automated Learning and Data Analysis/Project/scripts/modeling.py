from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import string
from sklearn.preprocessing import StandardScaler

# Features
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn_deltatfidf import DeltaTfidfVectorizer

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC

# Evaluation
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.metrics import roc_curve, auc, roc_auc_score

CLEANED_MAIL_FN = '../data/thresholded_2000_cleaned.csv'
#CLEANED_MAIL_FN = './data/thresholded_2000_cleaned.csv'
TRAIN_PROPORTION = 0.7
MAX_DEPTH = 20 # See RandomForestClassifier()
META_C = 10**(-3) # Causes a convergence error when c > 10^-3
BASE_C = 10**(0) # Between 10^-1 < c < 10^1, 10^0 had the largest accuracy


def load_data(mail_fn):
    """ Reads the labeled email data from csv to pandas dataframe. """
    data = pd.read_csv(mail_fn)
    return data


def split_train_test(data):
    """ Splits the data into training and testing. """
    X_train, X_test, y_train, y_test = train_test_split(data['text'], data['user'], train_size=TRAIN_PROPORTION)
    return (X_train, X_test, y_train, y_test)


def get_top_keywords(clf, vectorizer, n_classes, n_words=5):
    """
    Gets the most important words for classification of each user.
    Parameters:
        - clf: fitted classifier
        - vectorizer: fitted tf-idf vectorizer
        - n_classes: number of users we are classifying
        - n_words: number of top words we are getting
    """
    # Binary
    if n_classes == 2:
        print('\nTop keywords for', clf.classes_[0])
        print('--------------------------')
        important_tokens = pd.DataFrame(
            data=clf.coef_[0],
            index=vectorizer.get_feature_names_out(),
            columns=['tfidf']
        ).sort_values(ascending=False, by='tfidf')
        print(important_tokens.iloc[0:n_words])
        print('\nTop keywords for', clf.classes_[1])
        print('--------------------------')
        important_tokens = pd.DataFrame(
            data=-clf.coef_[0],
            index=vectorizer.get_feature_names_out(),
            columns=['tfidf']
        ).sort_values(ascending=False, by='tfidf')
        print(important_tokens.iloc[0:n_words])
    
    # Multi-class
    else:
        for i in range(n_classes):
            print('\nTop keywords for', clf.classes_[i])
            print('--------------------------')
            important_tokens = pd.DataFrame(
                data=clf.coef_[i], # Gaussian and Random Forest don't have coef
                index=vectorizer.get_feature_names_out(),
                columns=['tfidf']
            ).sort_values(ascending=False, by='tfidf')
            print(important_tokens.iloc[0:n_words])


def extract_features_tfidf(x_train, x_test):
    vectorizer = TfidfVectorizer()
    x_train = vectorizer.fit_transform(x_train)
    x_test = vectorizer.transform(x_test)
    return x_train, x_test, vectorizer


def extract_features_delta_tfidf(x_train, x_test, y_train):
    x_train = x_train.tolist()
    x_test = x_test.tolist()
    y_train = y_train.tolist()
    vectorizer = DeltaTfidfVectorizer()
    x_train = vectorizer.fit_transform(x_train, y_train)
    x_test = vectorizer.transform(x_test)
    return x_train, x_test, vectorizer


def extract_stylometric_features(X_train, X_test):
    splits = []
    for split in [X_train, X_test]:
        split = split.to_frame(name='text')

        # Add columns for features
        split['char num'] = None
        split['capital num'] = None
        split['digit num'] = None
        split['whitespace num'] = None
        split['wps'] = None     # average number of words per sentence
        split['awl'] = None     # average word length
        split['punct freq'] = None

        # Extract features
        for i, row in split.iterrows():
            email = row['text']

            row['char num'] = len(email)
            row['capital num'] = sum(1 for c in email if c.isupper())
            row['digit num'] = sum(1 for c in email if c.isdigit())
            row['whitespace num'] = sum(1 for c in email if c.isspace() or c == '\n')

            email = email.strip()

            sentences = email.split('.')
            word_num = 0
            for sentence in sentences:
                words = sentence.split(' ')
                word_num += len(words)
            row['wps'] = word_num / len(sentences)

            words = email.split(' ')
            char_num = 0
            for word in words:
                char_num += len(word)
            row['awl'] = char_num / len(words)

            row['punct freq'] = sum(1 for c in email if c in string.punctuation)

        splits.append(split)

    # Update dataframes
    X_train = splits[0]
    X_test = splits[1]
    X_train.pop('text')
    X_test.pop('text')

    return X_train, X_test


def extract_linguistic_features(X_train, X_test):
    splits = []

    for split in [X_train, X_test]:
        split = split.to_frame(name='text')

        # Add columns for features
        split['contains exclamation point'] = None
        split['contains ellipses'] = None
        split['contains capitalization'] = None
        split['contains double quote'] = None
        split['contains emoji'] = None
        split['chained question marks'] = None
        split['forward'] = None
        split['common greeting'] = None
        split['numbered lists'] = None

        # Extract features
        for i, row in split.iterrows():
            email = row['text']
            num_capitals = sum(1 for c in email if c.isupper())
            
            if num_capitals > 0:
                row['contains capitalization'] = 1
            else:
                row['contains capitalization'] = 0

            if '!' in email:
                row['contains exclamation point'] = 1
            else:
                row['contains exclamation point'] = 0
                
            if "..." in email:
                row['contains ellipses'] = 1
            else:
                row['contains ellipses'] = 0

            if '"' in email:
                row['contains double quote'] = 1
            else:
                row['contains double quote'] = 0

            if ':)' in email or ':(' in email or ':-)' in email or ':-(' in email:
                row['contains emoji'] = 1
            else:
                row['contains emoji'] = 0

            if '??' in email:
                row['chained question marks'] = 1
            else:
                row['chained question marks'] = 0

            if 'Forwarded' in email:
                row['forward'] = 1
            else: 
                row['forward'] = 0

            lower_email = email.lower()
            if ' hi ' in lower_email or 'hello' in lower_email or ' hey ' in lower_email or 'greetings' in lower_email:
                row['common greeting'] = 1
            else:
                row['common greeting'] = 0

            if '1.' in email and '2.' in email:
                row['numbered lists'] = 1
            else: 
                row['numbered lists'] = 0
            
            email = email.strip()

        splits.append(split)

    # Update dataframes
    X_train = splits[0]
    X_test = splits[1]
    X_train.pop('text')
    X_test.pop('text')

    return X_train, X_test

def analyze_linguistic_features(X_train, X_test, y_train, y_test):
    splits = []
    emails_w_m1_unique_feature = 0
    emails_w_1_unique_feature = 0
    emails_no_cap = 0
    emails_exclamation_point = 0
    emails_ellipses = 0
    emails_double_quote = 0
    emails_emoji = 0
    emails_chained_question_marks = 0
    emails_forward = 0
    emails_common_greeting = 0
    emails_numbered_lists = 0
    emails_w_no_features = 0
    user_unique_feature_count = {}

    train = X_train.to_frame(name='text')
    train['user'] = y_train
    test = X_test.to_frame(name='text')
    test['user'] = y_test

    for split in [train, test]:

        # Extract features
        for i, row in split.iterrows():
            email = row['text']
            user = row['user']
            num_capitals = sum(1 for c in email if c.isupper())
            unique_feature = 0
            if not user in user_unique_feature_count:
                user_unique_feature_count[user] = 0
            
            if num_capitals <= 0:
                unique_feature = unique_feature + 1
                emails_no_cap = emails_no_cap + 1

            if '!' in email:
                unique_feature = unique_feature + 1
                emails_exclamation_point = emails_exclamation_point + 1
                
            if "..." in email:
                unique_feature = unique_feature + 1 
                emails_ellipses = emails_ellipses + 1

            if '"' in email:
                emails_double_quote = emails_double_quote + 1
                unique_feature = unique_feature + 1

            if ':)' in email or ':(' in email or ':-)' in email or ':-(' in email:
                unique_feature = unique_feature + 1
                emails_emoji = emails_emoji + 1

            if '??' in email:
                unique_feature = unique_feature + 1
                emails_chained_question_marks = emails_chained_question_marks + 1

            if 'Forwarded' in email:
                unique_feature = unique_feature + 1
                emails_forward = emails_forward + 1

            lower_email = email.lower()
            if ' hi ' in lower_email or 'hello' in lower_email or ' hey ' in lower_email or 'greetings' in lower_email:
                unique_feature = unique_feature + 1
                emails_common_greeting = emails_common_greeting + 1

            if '1.' in email and '2.' in email:
                unique_feature = unique_feature + 1
                emails_numbered_lists = emails_numbered_lists + 1
            
            if unique_feature == 1: 
                emails_w_1_unique_feature = emails_w_1_unique_feature + 1
                user_unique_feature_count[user] = user_unique_feature_count[user] + 1
            elif unique_feature > 1: 
                emails_w_m1_unique_feature = emails_w_m1_unique_feature + 1
                user_unique_feature_count[user] = user_unique_feature_count[user] + 1
            else: 
                emails_w_no_features = emails_w_no_features + 1

            email = email.strip()

        splits.append(split)

    print("Emails with more than 1 feature.    " + str(emails_w_m1_unique_feature))
    print("Emails with 1 feature               " + str(emails_w_1_unique_feature))
    print("Emails with no features             " + str(emails_w_no_features))
    print()
    print("Emails with no capitalization       " + str(emails_no_cap))
    print("Emails with exclamation point       " + str(emails_exclamation_point))
    print("Emails with ellipses                " + str(emails_ellipses))
    print("Emails with double quote            " + str(emails_double_quote))
    print("Emails with emojis                  " + str(emails_emoji))
    print("Emails with chained question marks  " + str(emails_chained_question_marks))
    print("Emails that are forwarded           " + str(emails_forward))
    print("Emails with common greetings        " + str(emails_common_greeting))
    print("Emails with numbered lists          " + str(emails_numbered_lists))
    print()
    print("Number of emails with features per user ")
    for k in user_unique_feature_count:
        print(str(k) + "  " + str(user_unique_feature_count[k]))


def classify(clf, X_train, X_test, y_train, y_test, type = 'LogRegress', ShowImportantWords=False):
    """ Classify emails by authorship. """
    # Extract features
    X_train, X_test, vectorizer = extract_features_tfidf(X_train, X_test)

    if type == 'GNB':
        X_train = X_train.toarray()
        X_test = X_test.toarray()

    # Fit model
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)
    report = classification_report(y_test, y_pred_test)
    print(report)

    # Show most important words for each class
    if ShowImportantWords:
        n_classes = len(y_train.unique())
        get_top_keywords(clf, vectorizer, n_classes)

    # Visualize confusion matrix
    """
    conf_mat = confusion_matrix(y_test, y_pred)
    fig = plt.figure()
    fig.set_size_inches(8, 8, forward=True)
    plot_confusion_matrix(conf_mat, classes=clf.classes_, normalize=True)
    plt.show()
    """

    return (y_pred_train, y_pred_test)
    
   
def classify_linguistic(clf, X_train, X_test, y_train, y_test, type = 'LogRegress', ShowImportantWords=False):
    """ Classify emails by authorship. """

    if type == 'GNB':
        X_train = X_train.toarray()
        X_test = X_test.toarray()

    # Fit model
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)
    report = classification_report(y_test, y_pred_test)
    print(report)

    """
    conf_mat = confusion_matrix(y_test, y_pred)
    fig = plt.figure()
    fig.set_size_inches(8, 8, forward=True)
    plot_confusion_matrix(conf_mat, classes=clf.classes_, normalize=True)
    plt.show()
    """

    return (y_pred_train, y_pred_test)


def classification_comparison(X_train, X_test, y_train, y_test):
    # Models
    print('---Logistic Regression---')
    classify(LogisticRegression(), X_train, X_test, y_train, y_test)
    print('---Random Forest Classification---') # Does not work with get_top_keywords; bool MUST be false to run
    classify(RandomForestClassifier(max_depth=MAX_DEPTH), X_train, X_test, y_train, y_test, False)
    print('---Gaussian Naive Bayers---') # Does not work with get_top_keywords; bool MUST be false to run
    classify(GaussianNB(), X_train.toarray(), X_test.toarray(), y_train, y_test, False)
    print('---Linear Support Vector Classification---')
    classify(LinearSVC(), X_train, X_test, y_train, y_test)


def classification_linguistic_comparison(X_train, X_test, y_train, y_test):
    # Models
    print('---Logistic Regression---')
    classify_linguistic(LogisticRegression(max_iter = 200), X_train, X_test, y_train, y_test)
    print('---Random Forest Classification---') # Does not work with get_top_keywords; bool MUST be false to run
    classify_linguistic(RandomForestClassifier(max_depth=MAX_DEPTH), X_train, X_test, y_train, y_test, False)
    print('---Gaussian Naive Bayers---') # Does not work with get_top_keywords; bool MUST be false to run
    classify_linguistic(GaussianNB(), X_train, X_test, y_train, y_test, False)
    print('---Linear Support Vector Classification---')
    classify_linguistic(LinearSVC(C = META_C), X_train, X_test, y_train, y_test)

def classify_ensemble(X_train, X_test, y_train, y_test):
    base_clf = LinearSVC(C = BASE_C) 
    meta_clf = LinearSVC(C = META_C) 

    # Get base learner's predictions
    y_pred_train, y_pred_test = classify(base_clf, X_train, X_test, y_train, y_test)

    # Extract stylometric features
    X_train, X_test = extract_stylometric_features(X_train, X_test)

    # Append base learner's predictions as additional feature
    X_train['tf-idf'] = y_pred_train
    X_test['tf-idf'] = y_pred_test
    dummies_train = pd.get_dummies(X_train['tf-idf'])
    dummies_test = pd.get_dummies(X_test['tf-idf'])
    X_train = pd.concat([X_train, dummies_train], axis=1).reindex(X_train.index)
    X_test = pd.concat([X_test, dummies_test], axis=1).reindex(X_test.index)
    X_train.drop('tf-idf', axis=1, inplace=True)
    X_test.drop('tf-idf', axis=1, inplace=True)

    # Scale new features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train, y=y_train)
    X_test = scaler.transform(X_test)
    meta_clf.fit(X_train, y_train) # Causes convergence error if META_C is too high

    # Final predictions
    y_pred_test = meta_clf.predict(X_test)
    report = classification_report(y_test, y_pred_test)
    print(report)


def classify_linguistic_features(X_train, X_test, y_train, y_test):
    # analyze the data
    print() 
    print("Simple analysis of linguistic features.")
    print()
    analyze_linguistic_features(X_train, X_test, y_train, y_test);

    # Extract linguistic features
    X_train, X_test = extract_linguistic_features(X_train, X_test)

    # Scale new features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train, y=y_train)
    X_test = scaler.transform(X_test)

    print()
    print("Compare different classifiers with the linguistic features.")
    print()
    classification_linguistic_comparison(X_train, X_test, y_train, y_test)


def classify_linguistic_w_tf_idf_features(X_train, X_test, y_train, y_test):
    base_clf = LinearSVC(C = BASE_C) 
    meta_clf = LinearSVC(C = META_C) 

    # Get base learner's predictions
    print("Baseline classification with TF-IDF Features")
    print()
    y_pred_train, y_pred_test = classify(base_clf, X_train, X_test, y_train, y_test)

    # Extract linguistic features
    X_train, X_test = extract_linguistic_features(X_train, X_test)

    # Append base learner's predictions as additional feature
    X_train['tf-idf'] = y_pred_train
    X_test['tf-idf'] = y_pred_test
    dummies_train = pd.get_dummies(X_train['tf-idf'])
    dummies_test = pd.get_dummies(X_test['tf-idf'])
    X_train = pd.concat([X_train, dummies_train], axis=1).reindex(X_train.index)
    X_test = pd.concat([X_test, dummies_test], axis=1).reindex(X_test.index)
    X_train.drop('tf-idf', axis=1, inplace=True)
    X_test.drop('tf-idf', axis=1, inplace=True)

    # Scale new features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train, y=y_train)
    X_test = scaler.transform(X_test)
    meta_clf.fit(X_train, y_train) # Causes convergence error if META_C is too high

    print("Classification with Linguistic Features and TF-IDF Features")
    print()
    # Final predictions
    y_pred_test = meta_clf.predict(X_test)
    report = classification_report(y_test, y_pred_test)
    print(report)

def main():
    data = load_data(CLEANED_MAIL_FN)
    X_train, X_test, y_train, y_test = split_train_test(data)
    X_lin_train = X_train
    X_lin_test = X_test
    y_lin_train = y_train
    y_lin_test = y_test
    X_lin2_train = X_train
    X_lin2_test = X_test
    y_lin2_train = y_train
    y_lin2_test = y_test

    # classification_comparison(X_train, X_test, y_train, y_test)
    classify_ensemble(X_train, X_test, y_train, y_test)

    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()

    print("Linguistic Feature Analysis")
    print()
    print("Use Only Linguistic Features to Conduct Authorship Attribution")
    print()
    classify_linguistic_features(X_lin_train, X_lin_test, y_lin_train, y_lin_test)
    # add it in with the tdif stuff too.
    print("Use Linguistic Features with TF-IDF Features to Conduct Authorship Attribution")
    print()
    classify_linguistic_w_tf_idf_features(X_lin2_train, X_lin2_test, y_lin2_train, y_lin2_test)


if __name__ == '__main__':
    main()