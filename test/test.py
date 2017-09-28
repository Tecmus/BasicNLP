#coding:utf-8
from  tasks.CNSegmentation import *
from  tasks.PosTagging import *
if __name__=="__main__":
    # pt = PosTagging()
    # pt.processCorpus("../corpus/199801.txt")
    #
    # pt.predictTag(['我', '的', '爱', '就是', '爱', '你', '。'])
    #
    # seg = CNSegmentation()
    # seg.processCorpus('../corpus/199801.txt')

    s1 = '中华人民共和国今天成立了。'

    s3 = '(二○○○年十二月三十一日)(附图片1张)'
    s3 = '当选总统布什方面对克林顿访朝心存芥蒂。克林顿在记者招待会上说,日前布什造访白宫时,他曾与布什讨论访朝一事。他称,布什不反对这一访问。克林顿善于辞令。他没有说布什支持他访朝。但美国国会众院国际关系委员会副主席兼东亚小组委员会主席贝莱特2000年12月21日明确表示,克林顿在任期行将结束之时访朝是不明智的,甚至是危险的。'
    s3 = '但美国国会众院国际关系委员会副主席兼东亚小组委员会主席贝莱特2000年12月21日明确'
    s3 = '爱情从来没什么道理。'
    # seg.saveModel('abc.model')
    s2 = '代表北大的人大代表，代表人大的北大博士'
    seg=CNSegmentation()

    seg.loadModel('../model/Seg.model')
    s2 = '乒乓球拍卖啦！'
    s2 = '研究生开始研究生物了'
    print(seg.cutSentence(s2))
    s2 = '吉林省长春药店'
