import sys
import math
from collections import defaultdict

transition = defaultdict(float)
emission = defaultdict(float)
possible_tags = defaultdict(int)
lambda_1 = 0.95
lambda_unk = 1-lambda_1
N = 1000000

with open('model.txt') as model_file:
    for line in model_file:
        type_m,context,word,prob = line.split()
        possible_tags[context] = 1
        if type_m == "T":
            transition[context+' '+word] = float(prob)
        else:
            emission[context+' '+word] = float(prob)
with open('my_answer.pos','w') as answer:
    with open(sys.argv[1]) as read_file:
        for line in read_file:
            words = line.split()
            l = len(words)
            best_score = defaultdict(int)
            best_edge = defaultdict(str)
            best_score['0 <s>'] = 0
            best_edge['0 <s>'] = 'NULL'
            for i in range(l):
                for prev in possible_tags.keys():
                    for next_ in possible_tags.keys():
                        str_1 = str(i)+' '+prev
                        str_2 = prev+' '+next_
                        str_3 = next_+' '+words[i]
                        str_4 = str(i+1)+' '+next_
                        if str_1 in best_score and str_2 in transition:
                            score = best_score[str_1]-math.log2(transition[str_2])-math.log2(lambda_1*emission[str_3]+lambda_unk/N)
                            if str_4 not in best_score or best_score[str_4]>score:
                                best_score[str_4] = score
                                best_edge[str_4] = str_1
            for prev in possible_tags.keys():
                str_5 = str(l+1)+' </s>'
                str_6 = prev+' </s>'
                str_7 = str(l)+' '+prev
                if transition[str_6]!=0:
                    score = best_score[str_7]-math.log2(transition[str_6])
                    if str_5 not in best_score or best_score[str_5]>score:
                        best_score[str_5] = score
                        best_edge[str_5] = str_7

            tags = []
            next_edge = best_edge[str(l+1)+' </s>']
            while next_edge != '0 <s>':
#                print(next_edge)
                position,tag = next_edge.split()
                tags.append(tag)
                next_edge = best_edge[next_edge]
            tags.reverse()
            string = ' '.join(tags)
            string = string+'\n'
            answer.write(string)

