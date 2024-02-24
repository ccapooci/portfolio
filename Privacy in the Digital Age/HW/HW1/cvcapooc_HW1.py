import re, sys
import math, random
import numpy as np
import operator

#### BEGIN----- functions to read movie files and create db ----- ####

def add_ratings(db, chunks, num):
    if not chunks[0] in db:
        db[chunks[0]] = {}
    db[chunks[0]][num] = int(chunks[2])

def read_files(db, num):
    movie_file = "movies/"+num
    ratings = []
    fo = open(movie_file, "r")
    r = 0
    for line in fo:
        chunks = re.split(",", line)
        chunks[len(chunks)-1] = chunks[len(chunks)-1].strip()
        add_ratings(db, chunks, num)

#### END----- functions to read movie files and create db ----- ####

def score(w, p, aux, r):
    '''
    Inputs: weights of movies, maximum possible difference in rating, auxiliary information, and a record, 
    Returns the corresponding score
    '''
    #### ----- your code here ----- ####
    movie_ids = ["03124", "06315", "07242", "16944", "17113", "10935", "11977", "03276", "14199", "08191", "06004", "01292", "15267", "03768", "02137"] 
    
    supp = supp_aux(aux)
    #print(supp)
    score = 0
    score_2 = 0
    for mv_id in movie_ids:
        if mv_id in supp and mv_id in r and mv_id in aux:            
            score = score + ((w[mv_id] * T(aux[mv_id], r[mv_id], p[mv_id]))/ abs(supp[mv_id]))
    for mv_id, supp_val in supp.items():
        if mv_id in r:
            score_2 = score_2 + ((w[mv_id] * T(aux[mv_id], r[mv_id], p[mv_id]))/ abs(supp[mv_id]))
    if score != score_2:
        print("score mismatch ", score, score_2)
    return score
    


def compute_weights(db):
    '''
    Input: database of users
    Returns weights of all movies
    '''
    #### ----- your code here ----- ####
    score = {}
    supp = supp_db(db)
    w = compute_w(supp)      
        
    ## you can use 10 base log
    return w



#### BEGIN----- additional functions ----- ####

def T(aux, r, p):
    #print("A T is value is ", (1 - (abs(aux - r)/p))) 
    return 1 - (abs(aux - r)/p)


def supp_aux(aux):
    supp = {}
    for movie_id, movie_rating in aux.items(): 
        if movie_id not in supp:
            #supp[movie_id] = 1
            supp[movie_id] = 12
        else:
            #supp[movie_id] = supp[movie_id] + 1
            supp[movie_id] = 12
    return supp
    
def supp_db(db):
    supp = {}
    mov_4 = []
    mov_0 = []
    for user_id, movie_dict in db.items():
        for movie_id, movie_rating in movie_dict.items():
            if(movie_rating == 4  and movie_id not in mov_4):
                print(movie_id, movie_rating)
                mov_4.append(movie_id)
            elif(movie_rating == 0 and movie_id not in mov_0):
                print(movie_id, movie_rating)
                mov_0.append(movie_id)
            if movie_id not in supp:
                supp[movie_id] = 1
            else:
                supp[movie_id] = supp[movie_id] + 1
    return supp

def compute_w(supp):
    w = {}
    for movie_id, non_null_entries in supp.items():
        #print(movie_id, non_null_entries)
        w[movie_id] = 1/(np.log10(non_null_entries))
    return w

def compute_p(db, aux):

    p = {}
    min_p = {}
    max_p = {}
    for user_id, movie_dict in db.items():
        for movie_id, movie_rating in movie_dict.items(): 
            if movie_id not in min_p:
                min_p[movie_id] = movie_rating
            elif min_p[movie_id] > movie_rating:
                min_p[movie_id] = movie_rating

            if movie_id not in max_p:
                max_p[movie_id] = movie_rating
            elif max_p[movie_id] < movie_rating:
                max_p[movie_id] = movie_rating

    for movie_id, rating in aux.items():
        if movie_id not in min_p:
            min_p[movie_id] = rating
        elif min_p[movie_id] > rating:
            min_p[movie_id] = rating

        if movie_id not in max_p:
            max_p[movie_id] = rating
        elif max_p[movie_id] < rating:
            max_p[movie_id] = rating

    for movie_id in min_p:
        p[movie_id] = max_p[movie_id] - min_p[movie_id]

    print("A P value is ", p)

    return p

def compute_m(w, aux):
    m = 0
    supp = supp_aux(aux)
    for movie_id in supp:
        m = m + (w[movie_id] / abs(supp[movie_id]))
    return m
            
#### END----- additional functions ----- ####

if __name__ == "__main__":
    db = {}
    files = ["03124", "06315", "07242", "16944", "17113",
            "10935", "11977", "03276", "14199", "08191",
            "06004", "01292", "15267", "03768", "02137"]

    for file in files:
        read_files(db, file)

    aux =  {'03124': 4, '07242': 2, '17113': 2, '10935': 4,
           '11977': 3, '03276': 3, '14199': 2, '08191': 2, 
           '06004': 3, '01292': 2, '03768': 3, '02137': 1}

    #### ----- your code here ----- ####
    
    scores = {}
    w = compute_weights(db)
    top5_scores = {}
    highest_score_uid = ""
    second_highest_score_uid = ""
    print()
    print()
    print()
    print("1a")
    print("Movie ID | Corresponding Weight") 
    for k,v in w.items():
        print(k,"   |",v)

    p = compute_p(db, aux)
    for user_id in db:
        scores[user_id] = score(w, p, aux, db[user_id])

    #sorted_scores = 
    for k in sorted(scores, key=scores.get, reverse=True):
        if highest_score_uid == "":
            highest_score_uid = k
        elif second_highest_score_uid == "":
            second_highest_score_uid = k
        top5_scores[k] = scores[k]
        if len(top5_scores) == 5:
            break

    print()
    print()
    print()

    i = 1
    
    print("1b")
    print("Top 5 Scores")
    print("   | User ID |  Score ")
    for k in top5_scores:

        print(i, " |", k, "|", top5_scores[k])
        i = i + 1

    print()
    print()
    print()
    print("1c")
    print("The user id with the highest score is ", highest_score_uid)
    print()
    print("Comparison between ", highest_score_uid, "'s scores and the auxiliary data")
    print("Movie ID | ", highest_score_uid, "'s Rating | Auxiliary Data's Rating")
    for k, v in db[highest_score_uid].items():
        print(k, "   |", v, "                 |", aux[k])


    print()
    print()
    print()
    print("1d")
    score_diff = top5_scores[highest_score_uid] - top5_scores[second_highest_score_uid]
    print("The difference between the highest and second highest scores is ", top5_scores[highest_score_uid] - top5_scores[second_highest_score_uid])

    print()
    m = compute_m(w, aux)
    print("M is", m)
    if(score_diff > (m * 0.1)):
        print("If the the constant is .1, we would accept ", highest_score_uid, " as the top candidate.")
    else:
        print("If the the constant is .1, we would NOT accept ", highest_score_uid, " as the top candidate.")
          
    if(score_diff > (m * 0.05)):
        print("If the the constant is .05, we would accept ", highest_score_uid, " as the top candidate.")
    else:
        print("If the the constant is .05, we would NOT accept ", highest_score_uid, " as the top candidate.")
