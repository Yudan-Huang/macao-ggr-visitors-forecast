# Presentation Plan — M1 / M2 / M3

**项目**：CISC7204 Assignment 02 — Macao GGR and Inbound Visitor Arrivals  
**结构**：整个项目从头到尾讲一遍，按 M1 开场 → M2 分析 → M3 技术/演示/收尾  
**建议时长**：13 分钟（M1 4 + M2 5 + M3 4）+ 3–5 分钟 Q&A

---

## 0. 三个人的分工总表

| 角色 | 上台内容 | Slides | 时间 | 必须讲清楚的一句话 |
|---|---|---:|---:|---|
| **M1** | 开场：背景、研究问题、数据集、方法总览 + **相关分析** | 1–4 | 4 min | “84 个月不是更大样本，而是三个 regime；相关系数很高，但关系不稳定。” |
| **M2** | 分析：数据发现、逐张讲解图表、为什么 pooled 失败、validation、2025 结果、结论 | 5–9 | 5 min | “pooled 84m 全失败；24m 是 2024 validation 选的；2025 只测一次，R²=0.658。” |
| **M3** | 技术：可视化设计、Dash 现场演示、收尾与展望 | 10–13 | 4 min | “技术栈让分析可复现；Dash 只是展示层；84m 是诊断，24m 是 first draft。” |

**总时长 13 min。** 如果老师只给 10 min：M1 3 + M2 4 + M3 3，砍掉 Fig8 细节和 What-if 演示。  
如果给 15 min：加 full validation table 和 Q&A backup。

---

## 1. Slide map（整个项目从头到尾）

| Slide | 部分 | 标题 / 内容 | 主视觉 | 讲者 |
|---:|---|---|---|---|
| 1 | M1 | Title + one-sentence claim | 小图 `fig1_trend_84m.png` | M1 |
| 2 | M1 | 背景与研究问题：为什么要从 48 扩到 84 | 48 → 84 箭头图 | M1 |
| 3 | M1 | 数据集：3 个主数据集 + DSEC 校验 | 4 行表 | M1 |
| 4 | M1 | 方法总览 + 相关分析：correlation 0.97，但 regime-driven | `fig4_corr_84m.png` + 74.4/101.7/63.7 | M1 |
| 5 | M2 | 数据发现：seasonality + market mix | `fig2_seasonal_84m.png` + `fig3_market_84m.png` | M2 |
| 6 | M2 | 逐图：window sensitivity + model comparison | `fig5_window_compare.png` + `fig6_model_comparison.png` | M2 |
| 7 | M2 | 逐图：predicted vs actual + residuals | `fig7_pred_vs_actual.png` + `fig8_residuals.png` | M2 |
| 8 | M2 | 为什么 pooled 失败 + 2024 validation | 小表：Chow F；validation 24m | M2 |
| 9 | M2 | 2025 holdout + 结论 | 4 行结果表 | M2 |
| 10 | M3 | 技术栈与 pipeline | 架构图 | M3 |
| 11 | M3 | 可视化设计：8 张图各回答什么问题 | 8 图缩略图 | M3 |
| 12 | M3 | **Dash 现场演示** | 浏览器 / 备用截图 | M3 |
| 13 | M3 | 收尾：3 个 takeaway + 局限 + 展望 | 3 条结论 | M3 |
| 14 | Q&A | Backup | full validation table | 全员 |

---

## 2. M1 — 开场 + 数据 + 方法 + 相关分析（4 min）

### Slide 1 — Title（20 秒）

**标题**：Extending to 84 Months: Regime Diagnosis, Not a Bigger R²  
**副标题**：CISC7204 Assignment 02 · Huang Yudan · Chen Yuhan

**M1 说**：
> “Good morning. We extended the Macao GGR panel from 48 to 84 months. The point is not a bigger R² — it is to test whether the visitor–GGR relationship survives across three regimes.”

**怎么做**：
- 不要念目录；一句话立住主线。
- 背景深蓝，标题白色；右下角放很小的 `fig1_trend_84m.png`。

---

### Slide 2 — 背景与研究问题（50 秒）

**标题**：The question is not “can we fit better?” — it is “does the relationship survive?”

**3 个 bullet**：
- 48m Model 4: test R² 0.666, but trained only on the reopening period.
- 84m adds 2019–2021: pre-COVID boom, pandemic collapse, reopening.
- If the relationship is stable, a longer sample should help; if not, pooling should fail.

**M1 说**：
> “The original model looked good, but training and test both came from the reopening. Extending back to 2019 is a stress test: does the same relationship hold when the sample contains the pandemic?”

**怎么做**：
- 只放 0.666 和 84m 两个数字；不要放公式。
- 用箭头表示 48m → 84m 的 stress test。

---

### Slide 3 — 数据集（60 秒）

**标题**：Three official datasets, 84 months, no new variables

**表格 4 行**：

| Dataset | Provider | Role |
|---|---|---|
| Monthly GGR, 2019–2025 | DICJ | target |
| Monthly total arrivals | MGTO Data+ | main regressor |
| Arrivals by 28 markets | MGTO Data+ | Model 2 / EDA |
| Annual totals | DSEC / DICJ | validation only |

**M1 说**：
> “We use three primary datasets from two independent providers, plus DSEC annual totals for validation. Every month is present; the 28 markets sum exactly to the total; the 2019–2021 annual totals match the official figures.”

**怎么做**：
- 这张 slide 同时回答“至少两个数据集”的要求：3 个主数据集 + 1 个校验来源。
- 不要逐行念；点一行说一句“target / regressor / market / validation”。

---

### Slide 4 — 方法总览 + 相关分析（110 秒）

**标题**：Correlation is strong — but the relationship is regime-dependent

**左侧：方法总览（4 行）**
1. 84-month panel，2019-01..2025-12.
2. 三个 regime：pre-COVID 13 / pandemic 35 / reopening 36.
3. 模型：M1 总游客；M2 三客源；M3 当月+滞后；M4 regime-aware.
4. 评估：2024 validation 选窗口，2025 只测一次；rolling backtest.

**右侧：相关分析**
- `fig4_corr_84m.png` 的小图：GGR vs total arrivals **0.97**；GGR vs Mainland **0.96**；vs HK **0.92**；vs Other **0.95**.
- 但 GGR/10k arrivals：pre-COVID **74.4** / pandemic **101.7** / reopening **63.7**.

**M1 说**：
> “At face value, correlation is 0.97. But the same 10,000 visitors are associated with 74.4 million MOP before COVID, 101.7 during the pandemic, and 63.7 in the reopening. The correlation is high because all three series share a trend; it is not a stable structural relationship. That is why M2 will show what happens when we model it.”

**怎么做**：
- 这是 M1 的 punchline，也是 M1 的“相关分析”部分。
- 不要解释每个相关系数；只强调 0.97 和 74.4/101.7/63.7 的对比。
- 收尾 handoff：
  > “So the data are clean, but the relationship is not one line. [M2] will walk through the figures and show why pooling fails.”

---

## 3. M2 — 分析 + 逐张讲图 + 结论（5 min）

> M2 的任务不是“再讲一遍数据”，而是**按 notebook 的图逐张讲发现**，最后落到 pooled 失败、validation 和 2025 结果。

### Slide 5 — 数据发现：seasonality + market mix（60 秒）

**标题**：What the data show: seasonality and market mix

**图**：`fig2_seasonal_84m.png`（左）+ `fig3_market_84m.png`（右）

**逐图一句话**：
- **Fig 2**：复常期月份剖面；**10 月最高、9 月最低**；所以后面模型要保留 month dummies。
- **Fig 3**：Mainland **69.8%**、Hong Kong **21.7%**、Other **8.5%**；市场结构高度集中。

**M2 说**：
> “Figure 2 shows the reopening seasonal profile: October is the strongest month, September the weakest. Figure 3 shows the market mix: 69.8% Mainland, 21.7% Hong Kong, 7% other. These are the two descriptive facts that motivate the model’s month dummies and the three-market Model 2.”

---

### Slide 6 — 逐图：window sensitivity + model comparison（80 秒）

**标题**：The pooled models fail; the 24m model is validation-selected

**图**：`fig5_window_compare.png`（左）+ `fig6_model_comparison.png`（右）

**逐图一句话**：
- **Fig 5**：五个窗口的 **post-hoc test sensitivity**；绿色 24m 是 **2024 validation 选的**，不是用 2025 挑的。
- **Fig 6**：M1–M4 pooled 的 test R² 全为负；24m 绿色 0.658，48m 蓝色 0.666，**基本持平**。

**M2 说**：
> “Figure 5 is a post-hoc sensitivity check: the 24m bar is green because it is the validation-selected window, not because we picked the best test result. Figure 6 shows the pooled models are all negative; the selected 24m is comparable to the 48m reference, not better.”

**怎么做**：
- 主动说“post-hoc”，防止老师问“你们是不是用 test 挑的”。
- 不要念所有 R²；只强调“pooled negative vs 24m/48m comparable”。

---

### Slide 7 — 逐图：prediction + residuals（55 秒）

**标题**：The selected model tracks 2025, with two visible misses

**图**：`fig7_pred_vs_actual.png`（左）+ `fig8_residuals.png`（右）

**逐图一句话**：
- **Fig 7**：2025 预测 vs 实际；大多数月份贴近 45° 线；**6 月、10 月**是最大 misses（模型低估）。
- **Fig 8**：残差均值约 **−325**，范围约 **−1,606 到 +1,150**；没有明显 funnel，但误差不小。

**M2 说**：
> “The model tracks most of 2025, but it under-predicts June and October, the two strongest months. The residuals are centred slightly negative and are wide, so this is a first draft, not a production forecast.”

---

### Slide 8 — 为什么 pooled 失败 + 2024 validation（90 秒）

**标题**：Pooling fails structurally; the window is selected on 2024

**左侧：3 条证据**
- Chow: 2020-02 **F=25.25**；2023-01 **F=33.12**；p<0.0001.
- Pooled trend: **−56.7**（p≈0.017）— trend absorbs the pandemic collapse.
- Month dummies diluted → 2025 peaks missed.

**右侧：validation 小表**

| Window | Val RMSE | Val MAE |
|---:|---:|---:|
| 18 | 5,656.8 | 5,486.3 |
| **24** | **1,888.7** | **1,496.5** |
| 60 | 1,930.5 | 1,619.0 |

**M2 说**：
> “The break is structural, not random. The Chow test rejects one relationship at both the pandemic start and the reopening; the pooled trend is negative because it absorbs the collapse. We then select the window on 2024 only: 24m has the lowest RMSE, but only narrowly over 60m — 1,889 vs 1,930. This is a weak but honest selection; 2025 is untouched.”

**怎么做**：
- 这是 M2 的核心 slide；讲慢一点。
- 主动承认“weak selection”，老师会加分。

---

### Slide 9 — 2025 holdout + 结论（65 秒）

**标题**：2025 holdout: comparable, not a bigger R²

**表格 4 行**：

| Model | Train | Test R² | RMSE | MAE |
|---|---:|---:|---:|---:|
| 24m | 24 | 0.658 | 941.6 | 832.9 |
| 48m M4 | 38 | 0.666 | 929.3 | 755.3 |
| Seasonal naive | — | −1.198 | 2,385.7 | 2,044.7 |
| Last value | — | −1.504 | 2,546.2 | 1,730.4 |

**M2 说**：
> “The 24m model gets 0.658, essentially the same R² as the original 48m model. The 48m model is still slightly better on RMSE and MAE, so we do not claim that 84 months improves point prediction. What we claim is that the 84-month panel diagnoses the regime problem and the selected window recovers a comparable holdout.”

**Handoff to M3**：
> “[M3] will show the technical stack, the visualization design, and a live Dash demo.”

---

## 4. M3 — 技术 + 可视化 + Dash + 收尾（4 min）

### Slide 10 — 技术栈与 pipeline（50 秒）

**标题**：A reproducible pipeline, not a one-off notebook

**画一个 4 步 pipeline**：

```text
data/raw (DICJ + MGTO)
   → cleaned panel (84 rows, 31 cols)
   → validation-selected model (24m)
   → figures + report + Dash app
```

**M3 说**：
> “The project is a pipeline: three raw files, one cleaned 84-row panel, one validation-selected model, then figures, report and a Dash app. Every number in the report is generated from the notebook; the app reads the same cleaned panel.”

**怎么做**：
- 不要投代码；只画 pipeline。
- 强调 reproducibility：`Restart & Run All`。

---

### Slide 11 — 可视化设计（50 秒）

**标题**：Eight figures, each with one job

**8 图缩略图**（2×4 grid）：
- Fig1 trend + regimes
- Fig2 seasonality
- Fig3 market mix
- Fig4 correlation
- Fig5 window sensitivity
- Fig6 model comparison
- Fig7 predicted vs actual
- Fig8 residuals

**M3 说**：
> “Each figure answers one question: what happened over time, what is seasonal, who visits, is correlation stable, which window, which model, how close is the prediction, and what do residuals say. We deliberately avoided a dashboard that just puts every chart on one screen.”

**怎么做**：
- 用缩略图，不要放大图；让观众看到整体设计。
- 强调“one figure = one message”。

---

### Slide 12 — Dash 现场演示（90 秒）

**标题**：Dash demo: same model, interactive view

**演示前**：运行 `python dash_app.py`，打开 `http://127.0.0.1:8050`；备用截图在 `presentation_assets/`。

**90 秒流程**：

1. **Overview（15 秒）**：点 2020、2023、2024-25；说“three regimes”。
2. **Regimes（15 秒）**：74.4 / 101.7 / 63.7；说“same visitors, different GGR”。
3. **Models（20 秒）**：24m 绿色 vs 48m 蓝色；说“pooled negative, selected comparable”。
4. **Validation（15 秒）**：24m highlighted；说“2024 selected, 2025 untouched”。
5. **2025 test（15 秒）**：scatter around 45°；说“0.658 / 941.6 / 832.9”。
6. **What-if（10 秒）**：350 / Month 10 / t=75 → ~22.9bn；说“illustrative only, not a forecast”。

**M3 说（收尾）**：
> “The app is a presentation layer, not a new model. It reads the same cleaned panel and the same 24m model; it is here to make the logic visible, not to claim a production system.”

**如果 Dash 崩了**：
- 立刻切到 `presentation_assets/dash_overview.png` / `dash_models.png` / `dash_whatif.png`。
- 说：“The app is running locally; these are the same screens from the final notebook.” 不要在台上 debug。

---

### Slide 13 — 收尾与展望（45 秒）

**标题**：What we learned — and what we would do next

**3 个 takeaway**：
1. 84m is a **regime diagnostic**, not a bigger R².
2. 24m is **validation-selected**; 2025 test .658; comparable to 48m.
3. Rolling: beats seasonal naive; last-value edge **not significant**; first draft.

**3 个 next step**：
- Add supply-side controls (gaming tables, hotels, transport).
- Longer sample / rolling-origin backtest.
- Regularized or hierarchical market models.

**M3 说**：
> “The extension is worth doing because it changes what we know, not because it raises R². Next, we would add supply-side variables and test the model on more rolling windows.”

**Handoff to Q&A**：
> “Thank you — we are happy to take questions.”

---

## 5. 如果六个人都要上（M1/M2/M3 各拆 2 个小段）

| 小段 | 内容 | Slides | 时间 | 讲者 |
|---|---|---|---:|---|
| M1a | Title + why 84m + datasets | 1–3 | 2.0 min | S1 |
| M1b | Method + correlation analysis | 4 | 2.0 min | S2 |
| M2a | Data findings + Fig2–3 | 5 | 2.0 min | S3 |
| M2b | Pooled failure + validation + Fig5–6 | 6, 8 | 2.0 min | S4 |
| M2c | 2025 result + Fig7–8 + conclusion | 7, 9 | 1.5 min | S4/S5 |
| M3a | Tech + visualization + Dash | 10–12 | 2.5 min | S5/S6 |
| M3b | Closing + Q&A | 13 | 1.0 min | S6 |

> 只有 3 个 speaker 时，按 M1/M2/M3 每人一段；另外 3 人做 slide master、timekeeper、Q&A backup。

---

## 6. Q&A 准备（最可能被问的 8 个问题）

| 问题 | 回答 |
|---|---|
| Why 84 months if final model uses 24? | 84m is a diagnostic; it exposes regimes and enables 2024 validation. The final model is deliberately local. |
| Why 24, not 26 or 60? | 2024 validation lowest RMSE; 24 vs 60 is 1,889 vs 1,930 — weak signal, reported. |
| Did you use 2025 to choose the window? | No. 2024 validation; 2025 touched once. |
| Is 0.658 good? | Comparable to 48m 0.666; far better than seasonal naive; single 10-month holdout. |
| Is 24m overfit? | 13 params / 24 months; coefficients unstable (arrival p≈0.33); prediction only; rolling is conservative. |
| Does it beat last value? | Not significantly; beats seasonal naive (DM p≈0.037). |
| Does visitor cause GGR? | No causal claim; demand, capacity and policy drive both. |
| What next? | Supply-side controls, longer sample, rolling/regularized models. |

---

## 7. 排练与交付

- 第一次：每人单独讲，录音，不看时间。
- 第二次：M1→M2→M3 完整串场，13 分钟；每部分最后 30 秒举牌。
- 第三次：随机 Q&A 3 个，练“先结论、后解释”。
- 提交前：PDF 备份；Dash 截图备份；所有数字与 notebook 一致。

**不要说的话**：
- ❌ “84 months improves R².”
- ❌ “Our model beats last value.”
- ❌ “24m was the best on the test set.”
- ❌ “0.658 is our forecast accuracy.”
- ❌ “Visitors cause GGR.”

---

## 8. 一句话总结

**M1 讲“为什么 84 个月值得做 + 相关分析”，M2 讲“逐张图 + pooled 为什么失败 + validation + 2025 结果”，M3 讲“技术栈 + 可视化 + Dash 现场演示 + 收尾”。**  
三个人各 4/5/4 分钟；六个人就按 M1a/M1b、M2a/M2b、M3a/M3b 拆。全程只围绕一句主线：**84m 是诊断，24m 是 validation-selected first draft，不是“更大数据一定更好”。**
