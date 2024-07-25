# 7月23日更新
## 核心代码
新增RAG.py基线方法代码  

改进Tooluse，三类代码可以由partdata(kind)分别图区,kind为文件名，如'log.csv'  

依旧只用改yaml即可收集文件运行


# 7月11日更新
## 数据
已加入轨迹(trace)数据 ----- 只针对Nezha(TrainTicket)数据集；私有数据集只有部分metric


## 核心代码
分为Prompt和Agent两大类，放在各个支线  

按照数据集分类：TrainTicket和private  

按照大模型运行分类（3.5需要修剪数据，4o即为原数据）:3.5版本


## 运行方式
现加入将fault.txt读取为json数据功能，每次只需修改config.yaml文件即可


## 各支线解释
**main：** 用于4o模型、RCAgent方法  

**prompt版本：** 4o模型、prompt方法  

**gpt3.5专用：** 3.5-turbo模型、RCAgent方法、修剪过的数据  

**3.5prompt：** 3.5-turbo模型、prompt方法、使用修剪过的数据  

**private：** 暂时为RCAgent方法，模型无限制、private数据集（现仍然待完善的数据集）



# ICSE25
**关于数据转换**
整理好的数据通过CSVtomd转换为md 然后在 fault文件夹下创建fault.txt 然后把md文件放进去 目前先放入日志(log)和指标(metric)数据


**关于核心代码**
agentswokflow运行，在代码最后修改当前故障类型和描述 其他的可以下载下去尝试调试，prompt并不一定最好。
使用时注意tooluse有一个读取路径 确保读取的是你所测试的故障数据

**关于结果**
运行结果参考fault1中result的txt文件，将输出复制生成txt 禁止截图

**关于核心代码解释和尝试优化**
核心agent主要有4个
Operator负责代码执行，当前主要执行观测工程师的工具
观测工程师负责提供日志等数据
Calvin 是主要负责根因分析的工程师
John 是协助负责根因分析提出有效意见的辅助专家

**运行方式**
代码现已重构，方便运行，拉取代码后请先运行
pip install -r requirements.txt
openai_key已经在.env环境中配置，无需更改，请勿泄漏
运行方式：
你需要跑哪个错误，只需要在config.yaml中修改相应信息。
然后修改main中的初始描述，即可运行。

