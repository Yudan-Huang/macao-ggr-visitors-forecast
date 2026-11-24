# 可读性声明 / Readability Statement

**项目**：CISC7204 Assignment 02 — Macao Gross Gaming Revenue and Inbound Visitor Arrivals  
**版本**：84-month extension（2019-01 至 2025-12）  
**作者**：MC653633 Huang Yudan · MC655401 Chen Yuhan  
**日期**：2026-11-02

---

## 1. 这份声明是什么

这不是结果摘要，而是一份**阅读契约**：告诉读者这个项目按什么顺序读、每个文件负责什么、关键术语怎么理解、数字如何核对、哪些结论不能过度解读。

项目的核心问题只有一个：

> 澳门月度入境游客量与博彩毛收入（GGR）之间有什么关系；把样本从 48 个月扩展到 84 个月后，这种关系是否稳定？

答案不是“R² 越高越好”，而是：

> 84 个月把 **pre-COVID / pandemic / reopening** 三个 regime 暴露出来；把它们混在一起会让所有模型在 2025 年失效。最终模型用最近 24 个月的复常期窗口做 10 个月预测，测试 R² = 0.658，和原 48 个月 Model 4 的 0.666 基本持平。

---

## 2. 建议阅读顺序

| 读者 | 建议路径 | 重点 |
|---|---|---|
| 老师 / 评审 | 第 1-2 节 → Module 5 → Module 6 → Findings | 研究问题、断点证据、最终模型、局限 |
| 组员 / 接手者 | Module 2 → Module 4 → Module 6 → Module 7 → Module 8 | 数据字典、模型设定、验证选择、评估口径 |
| 复现者 | Instructions → Module 0-2 → 最后一节 | 原始文件、运行顺序、输出位置 |
| 只想看结论 | 顶部 Revision note → Findings | 三句话结论与边界 |

Notebook 是**从上到下**设计的，不建议跳着读；每一节都依赖前一节清洗出的 `df`。

---

## 3. 文件地图

| 文件/目录 | 作用 | 是否由 notebook 生成 |
|---|---|---|
| `CISC7204_Assignment02_84m.ipynb` | 主分析 notebook；含数据清洗、EDA、模型、诊断、结论 | 否（手写叙事 + 代码） |
| `data/raw/income_2019_2025.csv` | DICJ 月度 GGR，2019-01..2025-12 | 否（官方原始数据） |
| `data/raw/visitors_total_2019_2025.csv` | MGTO 月度总入境游客 | 否（官方原始数据） |
| `data/raw/visitors_by_market_2019_2025.csv` | MGTO 28 个客源市场月度数据 | 否（官方原始数据） |
| `data/processed/panel_84m.csv` | 预构建的 84 个月清洗面板，便于快速检查 | 是（与根目录 CSV 同步） |
| `gambling_visitors_cleaned.csv` | notebook 最终输出的清洗面板 | 是 |
| `data_dictionary_84m.csv` | 变量定义、单位、来源 | 是 |
| `figures/fig1_trend_84m.png` | 84 个月 GGR/游客趋势 + regime 阴影 | 是 |
| `figures/fig2_seasonal_84m.png` | 复常期月份剖面 | 是 |
| `figures/fig3_market_84m.png` | 复常期客源结构 | 是 |
| `figures/fig4_corr_84m.png` | 84 个月相关矩阵 | 是 |
| `figures/fig5_window_compare.png` | 训练窗口敏感性（post-hoc，不用于选模型） | 是 |
| `figures/fig6_model_comparison.png` | 基线/修订模型/基准对比 | 是 |
| `figures/fig7_pred_vs_actual.png` | 修订模型预测 vs 实际 | 是 |
| `figures/fig8_residuals.png` | 残差分布与残差-预测图 | 是 |
| `CISC7204_Assignment02_84m_FinalReport.docx` / `.pdf` | 5 页最终报告：数据扩展、regime 诊断、2024 validation、2025 holdout、rolling backtest | 否 |
| `cisc7204-Class_L-Team_02-PPT.pptx` | 20 页最终 presentation（Class L · Team 02） | 否 |
| `PRESENTATION_PLAN.md` | M1/M2/M3 的 13 分钟 presentation 分工与逐页讲稿 | 否 |
| `dash_app.py` / `README_DASH.md` | Dash 现场演示；读取同一份 cleaned panel 和 24m 模型 | 否 |
| `READABILITY_STATEMENT.md` | 本文件 | 否 |

> 只提交 `figures/` 中这 8 张由 notebook 生成的图；旧版/探索性图片不要混入最终包。

---

## 4. 关键术语

| 术语 | 含义 | 读的时候注意 |
|---|---|---|
| **GGR** | 博彩毛收入，million MOP | 是“收入”不是“利润”；含 VIP/中场等不同业务 |
| **Arrivals** | 入境游客，10,000 persons | 是“人次”不是“人数”；与 GGR 统计口径不同 |
| **Regime** | `pre_covid` 2019-01..2020-01；`pandemic` 2020-02..2022-12；`reopening` 2023-01..2025-12 | 这是分析框架，不是官方分类 |
| **Test window** | 2025-03..2025-12，共 10 个月 | 所有模型共用，保证可比 |
| **R²** | 解释/预测的方差比例 | **可以为负**；负值 = 比“测试期均值”还差 |
| **RMSE** | 均方根误差，million MOP | 对大误差更敏感 |
| **MAE** | 平均绝对误差，million MOP | 更容易直观解释 |
| **Naive mean** | 用训练期均值预测所有测试月 | 最弱基准 |
| **Seasonal naive** | 用去年同月预测 | 捕捉季节但不捕捉趋势 |
| **Last value** | 用上月值预测本月 | 捕捉短期水平 |
| **24m window** | 2023-03..2025-02，两个完整季节周期 | 由 **2024 validation** 选出（最低 RMSE），不是用 2025 测试集挑的 |

---

## 5. 数据来源与校验

**数据集数量说明（满足“至少两个数据集”）**：项目使用 **3 个主数据集 + 1 个校验来源**——
(1) DICJ 月度 GGR；(2) MGTO 月度总游客；(3) MGTO 28 个客源市场游客；
(4) DSEC/DICJ 年度总量仅用于交叉核对校验。主数据集来自 **DICJ 与 MGTO 两个独立官方机构**，
合并成一个分析面板是正常的数据整合，不是把“多个数据集”变成“一个数据集”。

数据链接：DICJ <https://www.dicj.gov.mo/web/en/information/DadosEstat_mensal/index.html>；
MGTO Data+ <https://dataplus.macaotourism.gov.mo/?lang=E>；
DSEC <https://www.dsec.gov.mo/en-US/Statistic?id=401>。

- **GGR**：DICJ 月度统计（2019-2025 XML）。
- **游客**：MGTO Macao Tourism Data+，28 个客源市场。
- **交叉核对**：DSEC 公布的年度总量（2019: 39,406,181；2020: 5,896,848；2021: 7,705,943）与 DICJ 年度 GGR（2019: 292,455；2020: 60,441 million MOP）。
- **校验结果**：84 个月无重复、无缺失；三客源市场之和 = 总数；份额和 = 1；2019-2021 年度总量与官方一致。
- **口径提醒**：2019 与 2023 后的游客统计/市场分类可能不同；GGR 的业务结构（VIP/中场）也变化很大。这些是 regime 差异的一部分，不应假装数据是同质的。

---

## 6. 模型与结果怎么读

1. **先看 Module 5，不要先看 R²。** 84 个月 pooled 模型训练 R² 很高（0.94-0.98），但测试 R² 全为负；这正是“时间趋势 + regime 混杂”的典型症状。
2. **Chow 检验**在 2020-02 和 2023-01 拒绝“同一条回归线”，说明 pooling 不是好主意。
3. **修订模型是 24 个月窗口**，不是“84 个月模型”。它的作用是：在复常期内做 10 个月预测；不是拿 84 个月去外推。
4. **24m 的测试 R² 0.658 略低于 48m Model 4 的 0.666，RMSE/MAE 也略差**。所以正确说法是“基本持平”，不是“84 个月显著更好”。
5. **五窗口对比是 post-hoc sensitivity，不是模型选择**。它使用了 2025 测试集；如果拿它挑窗口，测试 R² 会偏乐观。24 个月是 2024 validation 按最低 RMSE 选出的。
6. **系数不要过度解读**：24 个月、13 个参数，游客系数 p≈0.33；模型是预测工具，不是游客弹性/因果估计。

---

## 6b. Validation 选窗口与 rolling backtest

- **2024 validation**：候选长度 18/24/30/36/42/48/60 个月；训练到 2023-12，预测 2024-01..2024-12。
- **选择规则**：最低 validation RMSE；24m 的 RMSE 约 **1,888.7**，60m 约 **1,930.5**，24m 以微弱优势胜出。
- **2025 test**：窗口固定后才用 2025-03..2025-12，得到 R² **0.658** / RMSE **941.6** / MAE **832.9**。
- **Rolling one-step 2024-2025**：每月用前 24 个月训练、预测下一个月；RMSE **1,967.6**、MAE **1,430.5**。优于 seasonal naive（RMSE 3,520.6，DM p≈0.037），但与 last value（RMSE 2,098.8）差异不显著（DM p≈0.821）。
- **解释**：validation 选出 24m，但 24m 与 60m 的差距很小，信号偏弱；rolling 结果比 2025 单次 holdout 差，说明 0.658 不是普遍精度。

---

## 7. 可复现性检查表

- [ ] 从项目根目录打开 notebook（不要从别的目录运行，`BASE_DIR = Path.cwd()`）。
- [ ] `data/raw/` 三个文件存在且未改名。
- [ ] `Kernel → Restart & Run All` 能无报错跑完。
- [ ] `figures/` 正好生成 8 张图；旧图先清空。
- [ ] `gambling_visitors_cleaned.csv` 为 84 行 × 31 列。
- [ ] `data_dictionary_84m.csv` 包含 `regime` 与 `m_2...m_12`。
- [ ] 报告/notebook 中的数字与 `comparison` 表一致。
- [ ] 提交前删除 `.DS_Store`、`.mplconfig`、`.cache`、`__pycache__`。

---

## 8. 这份项目不声称什么

1. **不声称因果**：游客与 GGR 同时受需求、容量、政策影响。
2. **不声称 84 个月一定更好**：pooled 结果更差；24m 是 2024 validation 选出的短窗口，2025 只是一次 holdout。
3. **不声称 0.658 是普遍精度**：只有 10 个月测试、一个 holdout；换一年可能不同。
4. **不声称月份哑变量很精确**：24 个月估 11 个月哑变量，标准误很大。
5. **不声称模型可用于生产**：没有供给端变量、没有滚动回测、没有预测区间。

---

## 9. 可读性设计说明

- 每个 Module 只回答一个问题；标题写“结论”，不是“图表类型”。
- 图表标题/图注写清：数据窗口、单位、模型、训练/测试。
- 颜色用于强调（绿色 = 修订模型，蓝色 = 基线，灰色 = 基准），但关键结论在正文重复，不依赖颜色。
- 数字统一保留 1-3 位小数；R² 保留 3 位，RMSE/MAE 保留 1 位。
- 重要 caveat 用 blockquote/加粗，不藏在附录。
- 所有表格的“模型/窗口/指标”顺序固定，方便横向比较。

---

## 10. 一句话

**先读 Module 5 的断点证据，再读 Module 6 的 24 个月窗口，最后读 Findings 的边界；不要把 0.658 当成“84 个月比 48 个月更好”，它只是说明：在复常期内，一个简单的趋势+季节模型就能达到和原模型差不多的 10 个月预测水平。**
