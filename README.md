# presubmission-review

一个 Claude Code skill：投稿前，按目标会议真实审稿人的标准给自己的论文做一次盲审，得到一份口吻和打分尺度都接近真人审稿人的模拟审稿意见。

A Claude Code skill for pre-submission self-assessment: it reviews your own paper once, blind, the way a careful reviewer at your target venue would, and gives a calibrated score. The skill files are written in Chinese.

> **适用范围：只用于投稿前对自己的论文做自测，不用于替别人的投稿写审稿意见。** 审稿意见应当来自审稿人本人读完论文后的判断。
>
> **Intended use: pre-submission self-assessment of your own papers only. Do not use it to write reviews of other people's submissions.** A review should come from the reviewer's own reading of the paper.

## 它解决什么

让 AI 做模拟审稿时，常见两个毛病：

1. **审成审计报告。** 把能找到的每个问题都当成扣分理由，什么论文都打到线下，你分不清哪些问题真会导致拒稿。
2. **审成客套话。** 只说优点，或者把真正会导致拒稿的问题写得轻描淡写。

这个 skill 用三样东西把模拟审稿拉回到真实审稿人的水平：

- **打分校准**：按 ACL Rolling Review 的标准区分根本性缺陷和待澄清的问题，参照分数锚点和真实审稿的分数分布定分；同时列出真实审稿人一定会守住的情形，例如稿子没有完成、数字互相矛盾。
- **审稿人的视角**：真实审稿人读论文时会盯的地方（消融那一行到底测了什么、评测是否依赖方法自己的输出、统计口径有没有挑过……），以及“这是真方法还是工程细节”的判断。
- **真人审稿的语言**：基于 DISAPERE 数据集中 ICLR 审稿的统计（篇幅、结构、常用说法、提问数量），让模拟审稿读起来像真人写的。

## 用法

1. 把稿子做成投稿包：只放会议会收到的材料（正文 PDF、补充材料、代码包）。
2. 在一个新对话里让 Claude 审这个投稿包，并说明目标会议。它会先查这个会议当年的规则和审稿表单，扫描投稿包里的隐藏文字，然后读论文、定分、写模拟审稿。
3. 每个对话只审一个版本。改完之后开新对话重新审，不在同一个对话里比较新旧版本，否则前一次的意见会带偏判断。

## 安装

```bash
git clone https://github.com/YL1N/presubmission-review.git ~/.claude/skills/presubmission-review
pip install pymupdf
```

读 PDF 时还会用到 poppler 的 `pdftotext`（macOS：`brew install poppler`）。

## 文件

| 文件 | 内容 |
|---|---|
| `SKILL.md` | 主流程：只审一次的规则、动手前的检查、审稿步骤、自查清单、审稿人会盯的地方 |
| `references/score-calibration.md` | 缺陷分级、分数锚点、基准分布、容易判重和必须守住的情形 |
| `references/reviewer-language.md` | 真人审稿的统计特征、篇幅、常用说法、改写示例 |
| `references/venue-forms.md` | 怎样查目标会议的规则和审稿表单，以及投稿前对照征稿要求的检查 |
| `scripts/scan_pdf_notices.py` | 检查投稿包里的白字、极小字、页面外文字、元数据，以及写给审稿人或 AI 的提示 |

## 参考

- ACL Rolling Review Reviewer Guidelines: https://aclrollingreview.org/reviewerguidelines
- NeurIPS Reviewer Guidelines: https://neurips.cc/Conferences/2025/ReviewerGuidelines
- DISAPERE dataset: https://github.com/nnkennard/DISAPERE
- PeerRead dataset: https://github.com/allenai/PeerRead

## 许可证

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。使用或改编时请注明出处。
