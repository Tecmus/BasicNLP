import re
import numpy as np
import  pickle

from methods.Hmm import *
class CNSegmentation():
    def __init__(self):

        self.states = ['b', 'B', 'M', 'E', 'S', 'e']
        self.tags_n = {tag: 1 for tag in self.states}
        self.tag_tag_n = {'b_S': 0, 'b_B': 0, 'S_S': 0, 'S_B': 0, 'S_M': 0, 'S_E': 0, 'B_E': 0, 'B_M': 0,'M_M': 0, 'M_E': 0,
                          'E_B': 0, 'E_e': 0, 'E_S':0,'S_e': 0}

        self.word_tag_n = {}
        self.word_list = []
        self.transitionProb=[[]] #矩阵形式
        self.emissionProb=[[]]
        self.hmm=Hmm()

    def buildInitProb(self):
        self.pi = []
        sum_tag = sum(list(self.tag_tag_n.values()))

        idx_s = self.states.index('b')

        for value in self.tags_n:
            idx = self.states.index(value)
            self.pi.append(self.transitionProb[idx_s, idx] * self.tags_n[value] / sum_tag)

    def processCorpus(self, path):
        word_list = set()

        with open(file=path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            sum_sentence=0
            for line in lines:
                line = re.sub("\d{8}-\d{2}-\d{3}-\d{3}/m? ", "", line)  # 去除语料中的第一个词组

                sentences = line.split("/w")
                sentences = [term for term in sentences[:-1]]  # 切分句子

                for sentence in sentences:
                    terms = sentence.split()
                    prev_tag = 'b'  # 句首标志
                    for i in range(len(terms)):

                        if terms[i] == '':
                            continue
                        terms[i] = terms[i].split('/')[0]
                        terms[i] = self.fullToHalf(terms[i])  # 全角转半角

                        len_term = len(terms[i])

                        prev_tag=self.processTerm(i, len_term, prev_tag, terms, word_list)

                    self.tag_tag_n[prev_tag+'_e']+=1

                sum_sentence+=len(sentences)

            self.tags_n['b']=sum_sentence*2
            self.tags_n['e']=sum_sentence*2

        self.word_list = list(word_list)
        self.transitionProb=self.hmm.buildTransitionMat(self.tags_n,self.tag_tag_n,self.states)
        self.emissionProb=self.hmm.buildEmissionMat(self.tags_n,self.word_tag_n,self.word_list,self.states)

        self.buildInitProb()

    def processTerm(self, i, len_term, prev_tag, terms, word_list):

        if len_term == 1:
            if i==0:
                self.tag_tag_n['b_S']+=1
            word_list.add(terms[i][0])
            self.tags_n['S'] += 1

            try:
                self.word_tag_n[terms[i] + '/S'] += 1
            except KeyError:
                self.word_tag_n[terms[i] + '/S'] = 1

            self.tag_tag_n[prev_tag + '_S'] += 1
            prev_tag = 'S'

        if len_term == 2:

            if i==0:
                self.tag_tag_n['b_B']+=1

            word_list.add(terms[i][0])
            word_list.add(terms[i][1])


            self.tags_n['B'] += 1
            self.tags_n['E'] += 1

            try:
                self.word_tag_n[terms[i][0] + '/B'] += 1
            except KeyError:
                self.word_tag_n[terms[i][0] + '/B'] = 1

            try:
                self.word_tag_n[terms[i][1] + '/E'] += 1
            except KeyError:
                self.word_tag_n[terms[i][1] + '/E'] = 1

            self.tag_tag_n[prev_tag + '_B'] += 1

            self.tag_tag_n['B_E'] += 1

            prev_tag = 'E'


        if len_term > 2:
            if i==0:
                self.tag_tag_n['b_B']+=1

            for word in terms[i]:
                word_list.add(word)

            self.tags_n['B'] += 1
            self.tags_n['M'] += len_term-2
            self.tags_n['E'] += 1

            try:
                self.word_tag_n[terms[i][0] + '/B'] += 1
            except KeyError:
                self.word_tag_n[terms[i][0] + '/B'] = 1

            for j in range(1, len_term - 1):
                try:
                    self.word_tag_n[terms[i][j] + '/M'] += 1
                except KeyError:
                    self.word_tag_n[terms[i][j] + '/M'] = 1

            try:
                self.word_tag_n[terms[i][-1] + '/E'] += 1
            except KeyError:
                self.word_tag_n[terms[i][-1] + '/E'] = 1

            j = 0
            self.tag_tag_n[prev_tag + '_B'] += 1
            self.tag_tag_n['B_M'] += 1

            while j < len_term - 3:
                self.tag_tag_n['M_M'] += 1
                j += 1

            self.tag_tag_n['M_E'] += 1

            prev_tag = 'E'
        return  prev_tag

    def outPutResult(self, sentence, s_seq, term_list, states):
        s=''

        for i in range(len(sentence)):
            tag = states[s_seq[i]]
            if tag == 'E' or tag == 'S':
                # print(term_list[o_seq[i]], end=' ')
                s+= sentence[i] + " "
            else:
                # print(term_list[o_seq[i]], end='')
                s+=sentence[i]
        return  s

    def catchStr(self,sentence):
        l=[]
        l=re.split('(,|。|、|———|/|●)', sentence)
        values = l[::2]
        delimiters = l[1::2] + ['']

        return [v + d for v, d in zip(values, delimiters)]

    def cutSentence(self, sentence,sep='。'):  # sentence 为分词后的数组形式
        s=''

        windows = self.catchStr(sentence)
        # print(windows)
        for s_window in windows:

            if s_window=='':
                continue
            o_seq = self.convertSentence(s_window+"。")
            s_seq=self.hmm.viterbi(o_seq, self.transitionProb, self.emissionProb, self.pi)
            s+=self.outPutResult(s_window,s_seq,self.word_list,self.states)
        return  s
    def convertSentence(self, sentence):
        l=[]
        for word in  sentence:
            try:
                l.append(self.word_list.index(word))
            except ValueError:
                l.append(self.word_list.index('。'))

        return l

    def loadModel(self,path):
        model = open(path, 'rb')
        self.transitionProb=pickle.load(model)
        self.emissionProb=pickle.load(model)
        self.word_list=pickle.load(model)
        self.pi=pickle.load(model)
        self.states=pickle.load(model)

    def saveModel(self,path):
        output = open(path, 'wb')
        pickle.dump(self.transitionProb, output)
        pickle.dump(self.emissionProb, output)
        pickle.dump(self.word_list, output)
        pickle.dump(self.pi, output)
        pickle.dump(self.states, output)
        print('Save Success!')

    # def test(self,path):
    #     self.loadModel('abc.model')
    #     with open(path,encoding='utf-8',mode='r') as f:
    #         lines = f.read().splitlines()
    #         with open('./segR.txt', mode='w') as f1:
    #             for line in lines:
    #                 if line=='':
    #                     continue
    #                 f1.write(self.predictTag(line)+'\r\n')
    def fullToHalf(self,s):
        n = []
        for char in s:
            num = ord(char)
            if num == 0x3000:
                num = 32
            elif 0xFF01 <= num <= 0xFF5E:
                num -= 0xfee0
            num = chr(num)
            n.append(num)
        return ''.join(n)






