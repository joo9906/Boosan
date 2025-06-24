# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(skills):
    tournament = [0] * len(skills)
        
    idx_person = [(i, skill) for i, skill in enumerate(skills)]

    now_round = 1

    while len(idx_person) > 1:
        nextround = []
        for i in range(0, len(idx_person), 2):
            p1 = idx_person[i]
            p2 = idx_person[i+1]
        
            if p1[1] > p2[1]:
                win = p1
                lose = p2

            elif p1[1] < p2[1]:
                win = p2
                lose = p1
            
            tournament[lose[0]] = now_round
            tournament[win[0]] = now_round
            nextround.append(win)

        idx_person = nextround
        now_round += 1
    
    return(tournament)

    print(tournament)

a = [4, 2, 7, 3, 1, 8, 6, 5]
b = [4, 2, 1, 3]
c = [3, 4, 2, 1]

solution(c)