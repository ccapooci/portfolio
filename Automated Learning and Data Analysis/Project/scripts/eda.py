import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from nltk.tokenize import WhitespaceTokenizer

SENT_EMAIL_DIR = '../data/sentdir/'
THRESHOLDED_EMAIL_DIR = '../data/sentdir-thresholded_6000/'
CLEANED_EMAIL_DIR = '../data/sentdir-thresholded_6000_cleaned/'

def is_outlier(points, thresh=3.5):
    """
    Finds outliers in a list of data points.

    Parameters:
        - points(list[int]) : list of data points
        - thresh(float) : z-score to use as a threshold

    Return:
        - mask(list[boolean]) : boolean list with True if point is an outlier, 
                                false otherwise
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh


def plot_email_number(mail_dir):
    """
    Plot distribution of number of emails per user.
    
    Parameters:
        - mail_dir(string): name of directory with all users' emails
    """
    # Count number of emails for each user
    data = []
    for user in os.listdir(mail_dir):
        email_num = len(os.listdir(mail_dir + user))
        data.append([user, email_num])
    df = pd.DataFrame(data, columns=['user', 'email_num'])
    
    # Find min and max
    min_email_num = df['email_num'].min()
    max_email_num = df['email_num'].max()
    print(min_email_num, max_email_num)

    # Plot
    ax = sns.barplot(data=df, x='user', y='email_num')
    ax.set(xlabel='User', ylabel='Number of Emails Sent', title='Class (User) Distribution')
    ax.set(xticklabels=[])
    ax.text(0.82, 0.98, 'Min  = %d\nMax = %d' %(min_email_num,max_email_num),
            horizontalalignment='left',
            verticalalignment='top',
            transform = ax.transAxes)
    plt.show()


def plot_word_counts(mail_dir):
    """
    Plot distribution of number of words per email
    (words are defined as space separated strings).
    
    Parameters:
        - mail_dir(string): name of directory with all users' emails
    """
    # For each user...
    for user in os.listdir(mail_dir):
        # Count number of words in each email
        word_counts = []
        for file in os.listdir(mail_dir + '/' + user):
            mail_file = open(mail_dir + '/' + user + '/' + file)
            mail_text = mail_file.read()
            tk = WhitespaceTokenizer()
            words = tk.tokenize(mail_text)
            word_counts.append(len(words))

        # Remove outliers
        word_counts = np.array(word_counts)
        word_counts = word_counts[~is_outlier(word_counts)]

        # Plot 
        ax = sns.histplot(data=word_counts)
        ax.set(xlabel='Number of Words Per Email', ylabel='Frequency', title='%s Word Count Distribution' % user)
        plt.show()

def main():
    #plot_email_number(SENT_EMAIL_DIR)
    #plot_email_number(THRESHOLDED_EMAIL_DIR)
    plot_word_counts(CLEANED_EMAIL_DIR)


if __name__ == '__main__':
    main()