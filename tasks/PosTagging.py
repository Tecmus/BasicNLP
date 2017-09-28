
import  re
import  numpy as np
from methods.Hmm import *
class PosTagging():

    def __init__(self):

        self.term_tag_n = {}
        self.tag_tag_n = {}
        self.tags_n = {}
        self.term_list=[]
        self.states=[]

        self.hmm=Hmm()


    def  processCorpus(self,path):
        term_list=set()
        with open(file=path,mode='r',encoding='utf-8') as f:
            lines=f.readlines()
            for line in lines:
                line=re.sub("\d{8}-\d{2}-\d{3}-\d{3}/m? ","",line) #处理语料中的前一项时间信息

                sentences=line.split("/w")
                sentences=[term+'/w' for term in sentences[:-1]]       #切分句子

                for sentence in sentences:
                    terms=sentence.split( )
                    for  i in range(len(terms)):

                        if terms[i]=='':
                            continue
                        try :
                            self.term_tag_n[terms[i]]+=1
                        except KeyError:
                            self.term_tag_n[terms[i]]=1

                        word_tag=terms[i].split('/')
                        term_list.add(word_tag[0])

                        try:
                            self.tags_n[word_tag[-1]] += 1
                        except KeyError:
                            self.tags_n[word_tag[-1]] = 1

                        if i==0:
                            tag_tag='Pos'+"_"+word_tag[-1]
                        else:
                            tag_tag=terms[i-1].split('/')[-1]+'_'+word_tag[-1]

                        try:
                            self.tag_tag_n[tag_tag]+=1
                        except KeyError:
                            self.tag_tag_n[tag_tag]=1

        self.states=list(self.tags_n.keys())
        self.term_list=list(term_list)
        self.transitionProb = self.hmm.buildTransitionMat(self.tags_n, self.tag_tag_n, self.states)
        self.emissionProb = self.hmm.buildEmissionMat(self.tags_n, self.term_tag_n, self.term_list, self.states)

        self.buildInitProb()

    def buildInitProb(self):
        sum_tag=sum(list(self.tag_tag_n.values()))
        self.pi=[ self.tags_n[value]/sum_tag  for value in self.tags_n ]

    def predictTag(self,sentence):  #sentence 为分词后的数组形式

        o_seq=self.convertSentence(sentence)
        s_seq = self.hmm.viterbi(o_seq, self.transitionProb, self.emissionProb, self.pi)
        self.outPutResult(o_seq, s_seq, self.term_list, self.states)

    def convertSentence(self,sentence):
        return [self.term_list.index(word) for word in sentence]

    def outPutResult(self, o_seq, s_seq, term_list, states):
        for i in range(len(o_seq)):
            tag = states[s_seq[i]]
            print(term_list[o_seq[i]] + '/' + tag, end=' ')



