<p align="center"><img src="assets/hero.svg" alt="RealRoute-Bench" width="100%"></p>

# RealRoute-Bench

**在真实城市道路底座上，评测路由系统对城市、规模、约束组合与交通变化的适应能力。**

[English](README.md) · [最新进度](docs/STATUS.md) · [完整汇总报告](docs/GROUP_SUMMARY_20261024.md) · [数据卡](docs/DATA_CARD.md) · [方法覆盖](docs/METHOD_COVERAGE.md)

**研究预览 · 核验时点：2026-10-24T01:04:05.760539+09:00（日本时间）。** 本公开仓库提供精选输入、说明与聚合证据，不是完整工作区备份。完整动态发布、全方法正式比较和排行榜尚未完成。

## 数据与任务

`真实地点/道路 → 有向矩阵 + 业务 Scenario → 求解系统 → Solution → 独立 checker`

12城、2,400个固定公共道路访问点，20/50/100/200为嵌套规模，静态时间/距离共48对矩阵。节点不认证设施内部车辆入口。1,176道静态题使用父N20/N50，部分取送题为物理N19/N49；另有1,512道全原子组合题，分别使用城市留出与同底座交互留出协议。

真实 OSM 来源、OSRM profile 静态估计、高德交通感知 OD 估计、模型重建与合成业务属性明确区分。需求、窗口、车队、收益和罚金不是实采订单；重建值不称为真实采集。

## 实际进度

| 项目 | 核验结果 |
|---|---|
| 生产账本记录 | 1,080/1,680（64.3%），仅表示时段记录覆盖 |
| 原时段 provider 完整帧 | 1,005；按活动计划的时间与来源规则分类 |
| 错时恢复 provider 帧 | 17；真实查询，单列实际恢复时间 |
| 派生/重建引用 | 58；不并入纯实采数量 |
| 全部本地采集尝试 | 1,119次，其中QUARANTINE 81次；含试采/未选用尝试，分母不同 |
| 静态历史候选作业 | 5,880/5,880结果与收据齐全；含已撤下方法，混合池质量汇总暂缓 |
| 组合候选新批 | 283/2,086作业；完成数不等于可公开reference题数 |
| Spark 小样 | 64次；首答9/48有效，追加重复5/16有效；不是模型榜单 |
| 工程验收 | 最近归档全量541项、0失败、2跳过；本次来源分类专项8项通过，未重跑全仓 |

采集活动计划为中国时间2026-10-15至10-28，每城每天10个名义时段。三组城市按0/5/10分钟错峰，每城矩阵是有界窗口观测。日期、实际接收时间和父组相关性均需保留。

[机器快照](evidence/PROGRESS_SNAPSHOT.json) · [采集分项](downloads/COLLECTION_PROGRESS.json) · [逐城逐日](downloads/COLLECTION_COVERAGE.csv)

## 方法与评分

约束原子为一级配置，经典名称仅为模板；独立checker按原参数重算可行性与目标。精确求解、构造/局部搜索、各类元启发式、神经构造与改进、LLM及混合系统均需登记准入、支持范围和资源预算，不能只比较少数方便运行的方法。

Direct提交路线；Model提交声明式Scenario，经语义核验后由固定HiGHS求解。两轨分别报告。神经算法正式条件及全方法公平比较尚未完成，不支持任务必须标明，不删约束凑覆盖。

**LNS处理保持不变：** 未验证定制实现的17条pilot成绩已撤下；剩余[51条历史记录](downloads/PILOT_RESULTS.csv)保留原始求解字段、暂不展示相对gap。原混合池EXACT/BKS/gap汇总未恢复。[出处与处理说明](docs/LNS_IMPLEMENTATION_AUDIT_20261024.md)。当前新批仍含内部定制作业，本仓库仅报告执行工作量，不授予公开基线准入。

## 资源与下一步

[静态输入包](downloads/static_public_v1.zip) · [城市分区](downloads/STATIC_SPLIT.json) · [冻结问题定义](docs/PROBLEM_SPEC_V1.md) · [Schema](schemas/) · [Catalog](catalog/) · [来源署名](ATTRIBUTION.md)

先统一采集来源与最终日期清单，完成获准方法的参考池新版本及难度控制，再执行完整方法谱系与时间信息对照。预测/JEPA、Agent产品任务、正式排行榜仍待各自验收。

```sh
python3 scripts/verify_downloads.py
python3 scripts/test_collection_provenance_v4.py
python3 scripts/verify_progress_v4.py
```

这些命令核验本仓库的下载、分类行为和聚合一致性，不重放地图API或证明实车交通准确度。原始响应、私有路线/witness、账户和凭据均未上传。
