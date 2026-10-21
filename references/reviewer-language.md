# 真人审稿人的语言

模拟审稿要读起来像真实审稿人写的，才能帮你预判审稿人的反应。依据是 DISAPERE 数据集里 255 篇 ICLR 2019–2020 审稿的统计，以及逐轮积累的修改意见（文中引号里的中文是当时的原话）。

## 目录

1. 篇幅和结构
2. 常用说法
3. 不要这样写
4. 改写示例
5. 两个骨架
6. 交稿前扫一遍

## 1. 篇幅和结构

- 人类审稿的中位数约 300 词，九成在 620 词以内。把 summary、justification、rebuttal 问题分栏的表单会长一些，Weaknesses 一栏控制在 400 到 600 词。
- 宁短勿多。用户的原话（2026-10）：“现在喷的力度是足够的，但是有点话多”。力度来自开头一句直接的判断和论文自己的原话，而不是篇幅。每条弱点三到五句：一两个具体例子，一句话说明是根本性的还是可修复的、怎么改。次要的例子、背景解释，以及在开头预告各条要点，都删掉。问题列表四条左右，每条一句；结论段三四句。
- 单篇审稿提出批评的维度中位数是 2 到 3 个。没有人会把证据、方法、清晰度、可复现性、相关工作、新颖性全说一遍。挑真正影响判断的写。
- 纯文本。Markdown 加粗和破折号在真实审稿里各只出现在约 1% 的样本中。
- 约三成用编号列表，三分之一用短横线列表，其余是成段文字。带 Pros/Cons 小标题的只有 16%。
- 提问的中位数是 3 个。
- 结构不要固定。用户说过“意见条数有点僵化”。让论文决定形状：有时三条编号的问题长短不一，有时先一小段总的顾虑再接两三条，有时就是几段话。相邻两篇审稿不要长得一样。

## 2. 常用说法

统计里出现最多的句子开头和表态方式。

概述论文：
- This paper proposes / studies / builds ...
- The authors propose ... Experiments are conducted on ...

肯定：
- The paper is well written and easy to follow.
- The idea of ... is interesting. / The task is well motivated.
- I like the idea of ...
- The experiments are quite extensive.
- Fig. 3 is a nice example.

批评（最常见的开头是 It is not clear、It would be、The authors should、I think、I am not）：
- It is not clear how / why / whether ...
- I am not convinced by ...
- I don't doubt that ..., but ...
- It is hard to interpret ...
- I think part of this could simply come from ...
- This makes the comparison between models difficult.
- I understand this is common in this area, but ...

提问和请求，直接对作者说：
- Who decides whether ...? Is this done by humans or by an LLM?
- Why is it worse than Random?
- How are the baselines implemented in this setting?
- What happens if ...?
- It would be good / helpful / nice to ...
- Could the authors ...? / Please report ...

结论：
- Overall, I think this is an interesting paper.
- For these reasons I am leaning towards acceptance / rejection.
- I think the paper is below the acceptance threshold.
- It would be much stronger with ...
- I would move up if the authors ...

小词和缩写，适量使用：
a bit, quite, rather, kind of, somewhat, Honestly, By the way, A small thing:, Also, Besides, e.g., i.e., etc., don't, doesn't, I'm, 5x

连接词基本只用 However 和 Overall，偶尔 Also、Besides。Moreover、Furthermore、Additionally、Notably 很少见。

## 3. 不要这样写

每一条都是用户明确指出过的。

| 写法 | 用户的原话或原因 | 改成 |
|---|---|---|
| 弱点开头一大段两百词的 main concern，还带 “(Main concern.)” 标签 | “不要每次都先写一条巨长无比的main concern” | 拆成两三条普通长度的点，不加标签 |
| 每篇都是固定五条、每条等长 | “意见条数有点僵化” | 条数和长短由论文决定 |
| 句首小标题：“Fluency. The judge ...”“Efficiency. The simulator ...” | “像这种句首简短小标题的不要” | 用正常句子开头：“For fluency, the judge ...” |
| 结尾一个 “Other comments:” 或 “Minor:” 块，里面四五条各自论证完整的小条目 | “给人感觉就像ai特别喜欢加的东西” | 只留一两条真正要紧的，写成普通条目或一句话，其余删掉。Minor 只用于错别字这类真正的琐碎 |
| 一条弱点末尾统一补一句“可以通过补实验修复，例如 A、B、C、D”，四个名词短语和前面的问题一一对应 | “后面这坨可以如何修复，看起来很ai”（2026-10-20） | 把修复建议跟在对应的问题后面，只给一两个最要紧的，用第一人称写（“至少应该……”“作者应该看一下……”），最后一句说明能不能修 |
| 代码、数据文件、浮点精度之类的取证细节 | “人类不会去细扣这些乱七八糟的代码啊，数据边边角” | 只写从论文和附录里读得出来的问题 |
| 对仗、格言式的总结句 | 读起来像文章，不像审稿 | 平铺直叙 |
| 三项并列的排比句 | 同上 | 拆成两句 |
| validation chain、evidence base 这类抽象名词 | 同上 | 说具体的东西：the human study、Table 1 |
| genuinely、comprehensive、robust、crucial、notably | AI 常用词 | interesting、nice、extensive、important |
| 面面俱到，每个维度都说一条 | 人类只说两三个维度 | 删 |
| 评价作者本人：“作者应该了解自己的论文”“作为有基本常识的研究者，我很难相信” | 不增加任何信息，还会让 AC 把整份意见当成情绪化而打折扣 | 只说论文：“从实验设计看，论文并不清楚自己要主张什么” |
| 把论文里合理的范围说明当成罪状，例如逐条罗列“只测了表层指标”“正交不代表独立” | 等于惩罚透明，而且可能和自己引用的文献冲突 | 只引用因为设计答不了问题而不得不加的限定，把这一条写成“主张和贡献不清楚” |
| 论文明确限定了研究的构念（例如只研究某个表层指标），审稿却说“指标测错了” | 作者一句“我们本来就是这么定义的”就能挡回去 | 写成“构念和动机不一致”：构念本身意义有限，而标题和引言拿更强的东西当动机 |
| 弱点后面加括号分类：(fundamental)、(fixable) | 括号标签像模板产物。但 AAAI-27 的表单确实要求说明每条弱点是根本性的还是可修复的 | 去掉括号，用一句话说，例如 “This is the main problem for me” 或 “This should be easy to fix” |

## 4. 改写示例

例子是虚构的，不对应任何真实稿件。

评测循环：

> 改前：**Evaluation circularity (fundamental).** The evaluation pipeline exhibits a structural dependence on the proposed method: the judge is conditioned on the same latent state that drives generation, rendering the reported gains partially tautological.
>
> 改后：The LLM judge is given the user profile and asked whether the outputs fit it. But this profile comes from the proposed method itself, and the baselines don't have access to it. So it is kind of expected that the method gets higher scores.

结果难以置信：

> 改前：The 4x improvement lacks a plausible causal mechanism and is likely an artifact of simulator-method coupling, which undermines the learning-efficiency claim.
>
> 改后：All the other methods are around 0.10 while the proposed method gets 0.42. Honestly I find it hard to believe that changing only this component gives 4x more. Is this an artifact of the simulator? It would be good to check with another one.

基准没有对照：

> 改前：The low scores are informative, but the high scores and the model ranking are not.
>
> 改后：I don't doubt that the reported failures are real. But it is hard to interpret the high scores, since a model that always answers "invalid" would get 100%.

结论段：

> 改前：On balance, the strengths outweigh the weaknesses, and I lean toward acceptance contingent on the clarifications enumerated above.
>
> 改后：Overall, I think this is an interesting paper. The evaluation has some issues as discussed above, but I think they can be addressed and they don't invalidate the main contribution. For these reasons I am leaning towards acceptance.

## 5. 两个骨架

只是说明形状可以不同，不要照抄。

偏接收的一篇：

```
Strengths
1. 一句。 2. 一句加一句理由。 3. 一句。 4. 两句，点出最有说服力的那个结果。

Weaknesses
一小段：我的主要顾虑在哪，并承认这在该领域常见。
- 第一个具体问题，四五句，以一句推断收尾。
- 第二个，带一个直接的提问。
- 第三个，先肯定再指出不足，以提问收尾。
最后一小段话：还有两个关于某张表的问题。

Justification
Overall ... 可以解决，不影响主要贡献 ... leaning towards acceptance ... 希望作者做的两三件事。
```

偏拒稿的一篇：

```
Strengths
一段话，三四句，具体到哪个例子好。

Weaknesses
1. 最要紧的设计问题，先承认现象是真的，再说为什么数字不好解读。
2. 对某个实验不信服，说清楚歧义在哪，附一个小的对不上的地方。
3. 另一个实验的混淆因素，两三句。
4. 一句话加一个问句。
5. 一句话。

Justification
Overall, I like the motivation ... However ... below the acceptance threshold. It would be much stronger with ...
```

## 6. 交稿前扫一遍

- 有没有哪一条明显比别的长出一倍以上。
- 有没有句首小标题或末尾的 catch-all 列表。
- 有没有加粗、破折号、括号分类标签。
- 弱点覆盖的维度是不是超过三四个。
- 提问是不是超过四五个。
- 读出声来像不像一个人在对作者说话。
