import os
import shutil
import pandas as pd
import csv
import shutil
from nltk.tokenize import WhitespaceTokenizer

# mail directories
EMAIL_DIR = '../data/maildir/'
SENT_EMAIL_DIR = '../data/sentdir/'
THRESHOLDED_EMAIL_DIR = '../data/sentdir-thresholded_2000/'
CLEANED_EMAIL_DIR = '../data/sentdir-thresholded_2000_cleaned/'
OUTPUT_CSV_FN = '../data/thresholded_2000_cleaned.csv'

# possible folder names with sent emails
SENT_MAIL_FOLDERS = ['_sent_mail', 'sent', 'sent_items']

# threshold for filtering by number of emails (see threshold_email_num)
EMAIL_NUM_THRESHOLD = 2000

# remove emails shorter than this number of words
EMAIL_WORD_THRESHOLD = 5


def filter_sent():
    """
    Traverses original mail directory, copying sent emails to a filtered mail directory.
    """
    for user_dir in os.listdir(EMAIL_DIR):
        # create user directories for sent emails
        if not os.path.exists(SENT_EMAIL_DIR + user_dir):
            os.makedirs(SENT_EMAIL_DIR + user_dir)

        # copy sent emails to new directory
        email_num = 1
        for mail_folder in os.listdir(EMAIL_DIR + user_dir):
            if mail_folder in SENT_MAIL_FOLDERS:
                for mail in os.listdir(EMAIL_DIR + user_dir + '/' + mail_folder):
                    src = EMAIL_DIR + user_dir + '/' + mail_folder + '/' + mail
                    dst = SENT_EMAIL_DIR + user_dir + '/' + str(email_num)
                    if (os.path.isfile(src)):
                        if not os.path.exists(dst):
                            shutil.copyfile(src, dst)
                        email_num += 1


def threshold_email_num(threshold_num):
    """
    Create new dataset with only users who meet some required number of sent emails.

    Parameters:
        - threshold_num(int): number of sent emails under which is unacceptable
    """
    # Count number of emails for each user
    data = []
    for user in os.listdir(SENT_EMAIL_DIR):
        email_num = len(os.listdir(SENT_EMAIL_DIR + user))
        data.append([user, email_num])
    df = pd.DataFrame(data, columns=['user', 'email_num'])
    initial_num_users = len(df)

    # Find users who meet threshold
    df = df[df['email_num'] >= threshold_num]
    filtered_num_users = len(df)
    print('Removed', str(initial_num_users-filtered_num_users), 
        'users with number of emails <', str(threshold_num) + '.')

    # Create new thresholded dataset
    for user in os.listdir(SENT_EMAIL_DIR):
        if user in df['user'].unique():
            src = SENT_EMAIL_DIR + user
            dst = '../data/sentdir-thresholded_' + str(threshold_num) + '/' + user
            if not os.path.exists(dst):
                shutil.copytree(src, dst)


def filter_duplicate():
    """ Check for and remove duplicate emails. """
    pass


def clean_mail(mail_dir):
    """
    Clean emails for feature extraction. This includes:
        - removing text before email body (from, to, cc, etc.)
        - removing text after email (forwarded emails)

    Parameters:
        - mail_dir(string): path to data to be cleaned
    """
    for user in os.listdir(mail_dir):
        # Create new directory for cleaned data
        if os.path.exists(CLEANED_EMAIL_DIR + user):
            shutil.rmtree(CLEANED_EMAIL_DIR + user)
        os.makedirs(CLEANED_EMAIL_DIR + user)
        
        for file in os.listdir(mail_dir + '/' + user):
            mail_file = open(mail_dir + '/' + user + '/' + file)
            mail_text = mail_file.read()
            
            # Cut text before email body
            i = mail_text.find('X-FileName:')
            if (i == -1):
                print('ERROR:', mail_dir + '/' + user)
            else:
                mail_text = mail_text[i:]
                mail_text = mail_text[mail_text.find('\n') + 2:]
                
            # Cut text after email body based on common patterns
            i = mail_text.find('---------------------- Forwarded')
            if (i != -1):
                mail_text = mail_text[:i]
            i = mail_text.find('-----Original Message-----')
            if (i != -1):
                mail_text = mail_text[:i]
            i = mail_text.find('From:')
            if (i != -1):
                mail_text = mail_text[:i]
            i = mail_text.find('To:')
            if (i != -1):
                mail_text = mail_text[:i]
                i = mail_text.rfind('\n')
                if (i != -1):
                    for n in range(3):
                        mail_text = mail_text[:i - 1]
                        i = mail_text.rfind('\n')
            
            # Count number of words in email
            tk = WhitespaceTokenizer()
            word_count = len(tk.tokenize(mail_text))
            
            # Only add emails longer than word threshold to cleaned dataset
            if word_count >= EMAIL_WORD_THRESHOLD:
                with open(CLEANED_EMAIL_DIR + user + '/' + file, 'w') as f:
                    f.write(mail_text)


def data_to_csv(data_directory):
    """ 
    Converts data to a csv with text and class labels. 

    Parameters:
        - data_directory(string): path to data which csv is made from
    """
    # Open csv and write header
    f = open(OUTPUT_CSV_FN, 'w', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['text', 'user'])

    # Write mail text and user
    for user in os.listdir(data_directory):
        for file in os.listdir(data_directory + '/' + user):
            mail_file = open(data_directory + '/' + user + '/' + file)
            mail_text = mail_file.read()
            csv_writer.writerow([mail_text, user])


def main():
    #filter_sent()
    #threshold_email_num(EMAIL_NUM_THRESHOLD)
    clean_mail(THRESHOLDED_EMAIL_DIR)
    data_to_csv(CLEANED_EMAIL_DIR)


if __name__ == '__main__':
    main()