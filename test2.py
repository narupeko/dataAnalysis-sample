import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#3項演算子
dayMean = 1.56
i =2
x = dayMean if i == 1 else dayMean*2 if i==2 else 5
print(x)

#変数選択
kakoDailyTextDic = {1:"{}の天気は{}です",2:["{}の降雨量は{}です"]}
#x = "hogehoge"
stateText = kakoDailyTextDic[1] .format("昨日の","晴れ")
print(stateText)


mix = lambda x,y: x +"。"+y
print(mix("hoge", "taro"))