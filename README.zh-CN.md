<p align="center"><img src="assets/hero.svg" alt="RealRoute-Bench：12城、2400冻结节点、14约束原子" width="100%"></p>

# RealRoute-Bench

**真实城市路由系统，能否泛化到新城市、新约束组合和变化中的交通？**

[English](README.md) · [进度](docs/STATUS.md) · [数据卡](docs/DATA_CARD.md) · [评测协议](docs/EVALUATION.md) · [仓库范围](docs/REPOSITORY_SCOPE.md)

> **研究预览 · 2026-10-19。** 动态采集和静态参考解正在推进；完整数据发布、正式 LLM 实验和排行榜尚未完成。本仓库保持私有，保存精选资料与进度证据，不是完整研究工作区备份。下列数字为注明时间的快照。

## 核心设计

`BaseInstance + Scenario → Solver / LLM → Solution → 独立 checker`

城市底座固定节点身份、顺序与有向成本；Scenario 定义目标、车辆、访问规则和约束。**约束原子是一等配置，经典问题名只是模板。** checker 独立于 solver，重新计算可行性与目标。

![从城市底座到独立校验](assets/pipeline.svg)

| 研究轴 | 已有基础 | 尚待完成 |
| --- | --- | --- |
| 空间泛化 | 12城冻结底座；1,176个静态实例；跨城分区 | 完整参考解与受控算法比较 |
| 组合泛化 | 新增1,512例；14原子覆盖；独立组合留出协议 | 全量组合参考解与正式模型实验 |
| 时间信息价值 | 固定未来矩阵上的 Static / Reactive / Oracle；来源资格检查 | 完整序列 QA、动态日期分区和预测方法实验 |

需求、时间窗、服务时间、奖赏和车队是**合成业务属性**；OSRM 时间是 profile 估计，高德时间是 provider 的交通感知 OD 估计。它们都不是实车配送订单或轨迹真值。

## 当前进度

读取时间：`2026-10-19T06:15:45.768891+00:00`（UTC）。计划采集日期为中国时间 **2026-10-15 至 10-28**。

| 项目 | 当前证据 |
| --- | --- |
| 动态采集记录 | **540 / 1,680 个生产时段（32.1%）**；逐帧质量状态见机器快照 |
| 静态参考作业 | **2519 / 5,880** 个可信终态；**486 / 1,176** 道题全部作业结束 |
| 当前参考覆盖 | 183道题已有 EXACT；334道题已有 BKS；均为进行中快照 |
| 工程验收 | **431项，0失败，1项跳过**；不等于正式实验完成 |
| 确定性建模对照 | 68个训练条件全部通过门禁；另检验14原子的两种表示；未新增模型调用 |
| LLM 执行准备 | 46条历史记录分层回放；12次／48次均衡开发候选，执行关闭 |

采集记录数表示已记录的生产时段；完整性与来源口径见机器快照及数据卡。不同 seed 作业不增加独立实例数；EXACT 与 BKS 分开；进行中结果不构成排名。

[机器可读进度](evidence/PROGRESS_SNAPSHOT.json) · [采集状态](downloads/COLLECTION_PROGRESS.json) · [逐城逐日覆盖](downloads/COLLECTION_COVERAGE.csv) · [本轮离线交付](docs/OFFLINE_PREPARATION.md)

## 城市与冻结节点

北京、上海、西安、重庆、成都、杭州、武汉、厦门研究区、三亚、义乌、敦煌、安吉。每城200点，总计2,400点；20／50／100／200为同一母集的嵌套子集。节点是**真实 OSM 地点关联的公共道路访问点**，不认证建筑入口或最后一段进场成本。

<details><summary>查看12城冻结采点图</summary>

![第一组四城](assets/NODE_MAPS_1.png)
![第二组四城](assets/NODE_MAPS_2.png)
![第三组四城](assets/NODE_MAPS_3.png)

</details>

[城市结构指标](downloads/CITY_METRICS.csv)；采样分层是研究设计，不代表实测城市配送需求分布。

## 数据与使用

| 资源 | 内容与边界 |
| --- | --- |
| [静态输入包](downloads/static_public_v1.zip) | 1,176对 base / scenario；无私有 witness；父规模 N20／N50，部分取送题物理 N19／N49 |
| [静态分区](downloads/STATIC_SPLIT.json) | train 588、validation 196、test 392；同城派生实例绑定同分区 |
| [冻结规范](docs/PROBLEM_SPEC_V1.md) · [Schema](schemas/) · [Catalog](catalog/) | 14原子、4目标、11经典模板、6原始组合预设 |
| [历史开发结果](downloads/PILOT_RESULTS.csv) | 上海17题开发试验；不是当前全量参考结果或排行榜 |
| [校验哈希](downloads/SHA256.json) | 下载包、分区和快照完整性 |

```sh
python3 scripts/verify_downloads.py
```

该命令只验证本仓库下载资料。完整执行代码、原始交通响应、运行环境、账本与私有参考答案不在此快照中。

## 如何评价

- **Direct**：公开约束与矩阵 → 路线 JSON → checker。
- **Model**：相同公开输入 → 声明式 Scenario → 语义门禁 → 固定求解器 → checker。
- **确定性对照**：相同受控 prompt → 规则解析 → 同一门禁和求解协议；不声称支持任意自然语言。
- **时间任务**：三种信息权限选定路线，在同一个指定未来矩阵上评分。启发式 Oracle 不是数学下界。

城市留出与组合留出是不同实验。组合开发使用共享城市底座，不能据此声称同时实现未见城市与未见组合泛化。未来数据只属于 Oracle 和评分端；离线插补可使用后续观测，不能冒充因果预测输入。

## 下一步

1. 完成采集与 QA，保留真实缺失，冻结动态日期分区。
2. 完成参考解并汇总实例级 EXACT／BKS／无有效参考。
3. 核验模型身份、工具控制、usage 与余额后，冻结均衡调用方案。
4. 完成受控实验、统计报告及版本化数据发布，再发布论文与排行榜。

网站与存储规划见 [HOSTING.md](docs/HOSTING.md)。引用与再分发边界见 [ATTRIBUTION.md](ATTRIBUTION.md)；正式论文与作者确认的引用格式待发布。
