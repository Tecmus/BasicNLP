import  numpy as np

class Hmm():


    def buildTransitionMat(self, states_n, state_state_n, states):
        len_status = len(states_n)
        transitionProb = np.zeros((len_status, len_status), dtype=float)

        for i in range(len_status):
            for j in range(len_status):
                s = states[i] + '_' + states[j]

                tag_i = states[i]
                try:
                    transitionProb[i, j] = state_state_n[s] / (states_n[tag_i] + 1)  # 条件概率

                except KeyError:
                    transitionProb[i, j] = 0.0

        return  transitionProb

    def buildEmissionMat(self, states_n, o_state_n, o_sequence, states):
        emissionProb = np.zeros((len(states), len(o_sequence)), dtype=float)

        for i in range(len(states)):
            for j in range(len(o_sequence)):
                s = o_sequence[j] + '/' + states[i]
                tag_i = states[i]
                try:
                    emissionProb[i, j] = o_state_n[s] / states_n[tag_i]  # 条件概率
                except KeyError:
                    emissionProb[i, j] = 0

        return  emissionProb
    '''
        维特比算法：
        input:
            o_sequence:观测序列
            :条件转移概率
            :观测概率
            pi:初始状态概率
            
        return 符合最优的状态序列
    '''
    def viterbi(self, o_sequence, A, B, pi):
        len_status = len(pi)

        status_record = {i: [[0, 0] for j in range(len(o_sequence))] for i in range(len_status)}

        for i in range(len(pi)):
            status_record[i][0][0] = pi[i] * B[i, o_sequence[0]]
            status_record[i][0][1] = 0

        for t in range(1, len(o_sequence)):
            for i in range(len_status):
                max = [-1, 0]
                for j in range(len_status):

                    tmp_prob = status_record[j][t - 1][0] * A[j, i]
                    if tmp_prob > max[0]:
                        max[0] = tmp_prob
                        max[1] = j

                status_record[i][t][0] = max[0] * B[i, o_sequence[t]]
                status_record[i][t][1] = max[1]

        return self.getStateSequence(len_status, o_sequence, status_record)


    '''
        获取最大概率的状态序列
        
    '''
    def getStateSequence(self, len_status, o_seq, status_record):
        max = 0
        max_idx = 0
        t = len(o_seq) - 1
        for i in range(len_status):
            if max < status_record[i][t][0]:
                max = status_record[i][t][0]
                max_idx = i

        state_sequence = []             #栈结构
        state_sequence.append(max_idx)
        while (t > 0):
            max_idx = status_record[max_idx][t][1]
            state_sequence.append(max_idx)
            t -= 1
        state_sequence.reverse()
        return  state_sequence




