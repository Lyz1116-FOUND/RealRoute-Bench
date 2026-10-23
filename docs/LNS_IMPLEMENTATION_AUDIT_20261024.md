# LNS 实现出处与合理性核验

核验日期：2026-10-24。结论：LNS 有明确的学术来源，但本项目这份定制启发式没有查到足以认定为特定论文复现的实现依据，因此撤下 GitHub 当前下载结果中的该方法，不将它列为已验证的文献强基线。

## 1. 哪些出处已经核实

- Paul Shaw（1998），Using Constraint Programming and Local Search Methods to Solve Vehicle Routing Problems，CP98，LNCS 1520，DOI：[10.1007/3-540-49481-2_30](https://doi.org/10.1007/3-540-49481-2_30)。它给出路由 LNS 的经典框架：移除部分访问，再搜索重新插入。
- Stefan Ropke、David Pisinger（2006），An Adaptive Large Neighborhood Search Heuristic for the Pickup and Delivery Problem with Time Windows，Transportation Science 40(4):455–472，DOI：[10.1287/trsc.1050.0135](https://doi.org/10.1287/trsc.1050.0135)。[作者所在机构的论文记录](https://orbit.dtu.dk/en/publications/an-adaptive-large-neighborhood-search-heuristic-for-the-pickup-an/)及其手稿解释了随机移除、regret 插入、自适应算子选择和退火接受机制。

这些出处支持方法家族，不能证明本项目的代码复现了论文、采用作者代码或达到论文性能。当前源码中未见与具体文献对应的实现说明，也没有作者实现版本或原论文 benchmark 的复现实验记录。

## 2. 这份代码实际做什么

核验对象为本地 `heuristic.py` 和 `heuristic_v2.py` 中的 `Search`、`insertions`、`repair`、`solve`。以下来自代码读取，不是对论文算法的转述。

1. 将普通客户作为单个插入单元，取送请求作为一对；先构造全部必访任务，再尝试加入有收益或有助于最低收益要求的可选任务。
2. 枚举车辆和插入位置，计算完整路线成本与约束；取送同时枚举取点与送点的位置。
3. 必访任务使用第二好位置与最好位置目标值之差作为 regret，优先安排差值大的任务。只有一个候选位置时用大常数提高优先级。
4. 得到一个可行 incumbent 后，随机移除约 15%—40% 的已访问单元，重新插入；每五次迭代从空路线重建一次。
5. 只保存严格改善的最好解，运行到时间预算；最后仍需独立 checker 接受。代码不提供最优性或不可行性证明。

v1 会把一般同车/先后关系合并进插入单元；v2 不再让这些条件关系强制联合选择，只把取送请求作为原子单元。这也说明两版不能用同一个未区分版本的名称混作完全相同方法。

## 3. 为什么不是论文复现或完整 ALNS

| 检查项 | 当前代码 | 应如何解释 |
|---|---|---|
| 移除与修复 | 单一随机移除和定制插入 | 符合基础 LNS 思路 |
| regret 定义 | 对所有候选插入位置排序后取前两项 | 不等于上述论文按最好、次好车辆路线构造的 regret-2 |
| 算子自适应 | 没有多算子权重学习 | 不能叫已经复现 ALNS |
| 接受策略 | 只更新全局最好值，定期重启 | 没有复现该 ALNS 的退火接受策略 |
| 其他增强 | 未见 Shaw 相关性移除、worst removal 或独立 2-opt/3-opt 改进层 | 不能借文献名声推断搜索强度 |
| 复现依据 | 未核到作者实现绑定或公开标准算例对齐记录 | 不能列为文献复现型强基线 |

## 4. 思路合理吗

作为工程搜索器，思路合理：regret 优先处理将来可能难插入的任务，移除—修复让路线重新组合，重启增加探索机会，独立 checker 约束最终解的合法性。定制启发式不必有一篇与每行代码完全对应的论文，才能作为明确命名的实验方法。

作为正式 benchmark 的权威强基线，当前证据不够。单一移除与只保留最好解会限制搜索多样性；构造失败不回溯，可能遗漏可行分配；v2 对一般关系逐项检查但不做联合插入，搜索效率可能受影响。重复全路线评估也可能消耗较多预算。尚无依据断言这些限制在所有任务上的影响大小。

合理的后续准入是：明确称为“项目定制的随机移除/位置 regret 修复启发式”，固定源码和参数，核验已知小例和公开标准题，并与可复现外部算法在共同支持集合、相同总预算下比较。在完成之前，不用其成绩代表 LNS/ALNS 家族的公认水平。

## 5. 本次对外结果的处理

- 从公开 pilot CSV 移除该自研方法的 17 条记录，保留另外三种方法的 51 条历史记录。
- 剩余记录的 objective、valid、时间、bound 和证优字段保持原样；因历史 reference 池含被移除方法，暂不展示所有相对 gap，而非用更弱 reference 重算后伪装成原始结果。
- 暂缓展示该池的汇总参考数量，并在中英文首页、状态和机器快照说明原因；原始本地实验及历史提交不改写。
- 没有重跑求解器，没有重新判定数据、没有改动冻结协议、正在运行的任务或独立 checker。此处撤下的是未验证定制实现的对外成绩，不是否认 LNS 方法家族的学术依据。

## English clarification

LNS has established literature; this project's random-removal, position-regret repair heuristic is a custom implementation, not a verified reproduction of Shaw (1998) or Ropke and Pisinger (2006), and not a complete ALNS implementation. Its public pilot rows are withdrawn. Remaining historical solver objectives and validity fields are retained, but relative gaps and the mixed-pool reference summary are withheld until a separately versioned reference pool is established. Local raw runs and Git history are preserved; no solver was rerun for this documentation change.
