​        简单的实现了HMM模型同时做了词性标注和分词方面的任务,效果达到了期望水平，但还是远远不够，后面有时间会做出改进。这个项目有两部分内容:词性标注和分词。利用了北京大学提供的人民日报语料库作为训练集，进行训练。

**词性标注**

使用：

```python
 	
    pt = PosTagging()
    pt.processCorpus("../corpus/199801.txt") #训练部分
    pt.saveModel(model_name)
    pt.loadModel(model_name)
    pt.predictTag(['我', '的', '爱', '就是', '爱', '你', '。']) #预测部分
    
```

​	有监督学习能很好地处理一些歧义。

​	比如：

> 我的爱就是爱你
>
> 我/r 的/u 爱/vn 就是/d 爱/v 你/r 。/w 

可以同时区分开两个具有不同词性的‘爱’。

**分词**

使用:

```python
    
    seg = CNSegmentation()
    seg.processCorpus('../corpus/199801.txt')
    seg.saveModel(model_name)
    seg.loadModel(model_name)
    seg.cutSentence('代表北大的人大代表，代表人大的北大博士')
    
```

也可以hold住一些歧义。

> 研究生开始研究生物了
>
> 研究生 开始 研究 生物 了

> 乒乓球拍卖啦！
>
> 乒乓球 拍卖 啦 ！

**评测结果:**

词性标注暂时未作评测,主要针对分词进行测评。测评数据集来自SIGHAN提供的Bakeoff 2005的数据。地址:https://github.com/yuikns/icwb2-data

结果如下:

- === SUMMARY:

- === TOTAL INSERTIONS:	2824
- === TOTAL DELETIONS:	11587
- === TOTAL SUBSTITUTIONS:	17204
- === TOTAL NCHANGE:	31615
- === TOTAL TRUE WORD COUNT:	104372
- === TOTAL TEST WORD COUNT:	95609
- === TOTAL TRUE WORDS RECALL:	0.724
- === TOTAL TEST WORDS PRECISION:	0.791
- === F MEASURE:	0.756
- === OOV Rate:	0.138
- === OOV Recall Rate:	0.765
- === IV Recall Rate:	0.718

​	准确度在80%左右，召回率偏低，对于没有加入词表的情况来说，这个结果还算可以，因为发现大部分分错的语句，是由于训练集中没有这些语料，如果加入词表判断会改善这种情况，后期有很大提升空间，可以试着加一些技巧还有多个模型结合去做，也需要进一步增加训练集。









