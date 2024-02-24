import json
import webbrowser
import time
import requests
import sys

def request_url(url, file, write_comma):
    individual_time_start = time.time()
    response = requests.get(url)
    individual_time_stop = time.time()

    write_string = str((individual_time_stop - individual_time_start) * 1000)

    if write_comma:
        write_string = write_string + ','

    file.write(write_string)

    return

def main():

    # Get the command line argument
    ip = sys.argv[1]

    # Your logic with the input goes here
    print("You entered:", ip)

    file = open("results/results.csv", "w")

    total_time_start = time.time()

    for i in range(30):
        if i == 29:
            request_url('http://' + ip + '/', file, False)
        else:
            request_url('http://' + ip + '/', file, True)

    total_time_end = time.time()

    file.write("\n")
    file.write(str((total_time_end - total_time_start) * 1000) + ',' )
    file.close()

if __name__ == "__main__":
    
     main()