# RealRoute-Bench：统一问题定义 v1.0

状态：问题规范定稿；生成器、通用 evaluator 与 solver adapters 的实现另行推进。

本规范以本次提供的“问题定义与数据准备规划方案”和“约束原子为底层核心”两份材料为依据，完成问题定义、合法组合、输出及判分语义。它不规定城市采集名单，不宣称已完成任何新增问题的求解测评。

## 1. 研究对象与分层

RealRoute-Bench 评价求解系统能否在真实城市有向路由底座上，依据明确的目标和约束组合，产生可行、高质量且高效的解，并适应城市、规模、日期和约束组合的变化。

问题空间组织为：

\[
\text{城市底座}\times\text{规模}\times\text{目标与约束配置}\times\text{参数紧度}\times\text{泛化协议}.
\]

底层定义由结构化配置决定；ATSP、CVRP、OP 等经典名称是配置的预定义模板。没有经典名称的组合使用同一套定义与校验规则。

```mermaid
flowchart LR
    B[BaseInstance：节点与有向矩阵] --> I[ProblemInstance]
    A[原子库：字段、语义与依赖] --> S[Scenario：目标与合法组合]
    S --> I
    I --> R[Solution：车辆、路线与服务时刻]
    R --> E[独立校验与目标重算]
    S -.辅助名称.-> T[Canonical Template]
```

形式化地：

\[
\mathcal I=(B,S),\qquad
S=(\mathcal O,\mathcal W,\mathcal F,\mathcal D,\mathcal R,\mathcal A,\Theta).
\]

| 符号 | 含义 |
|---|---|
| \(B\) | 城市节点、有向成本/耗时/距离、字段来源、采集可用性 |
| \(\mathcal O\) | 优化目标及其单位、权重 |
| \(\mathcal W\) | 必访与可选服务节点 |
| \(\mathcal F\) | 可用车辆、出发节点/时刻、容量与启用成本 |
| \(\mathcal D\) | 终端节点集合及车辆的仓库分配 |
| \(\mathcal R\) | 闭合、固定终点或自由终点路线规则 |
| \(\mathcal A\) | 启用的约束/属性原子及关系集合 |
| \(\Theta\) | 需求、窗口、收益、惩罚和资源上限等具体参数 |

优化问题为：

\[
\operatorname*{opt}_{X\in\mathcal X(B,S)} f_{\mathcal O}(X),
\]

其中 \(\mathcal X(B,S)\) 是由配置共同确定的可行域；`opt` 根据目标为 min 或 max。只记录原子开关而没有目标、车辆、端点和参数，不能唯一确定一个问题。

## 2. 城市底座与符号约定

### 2.1 节点与规模

选定路由节点集合 \(V\)，终端节点集合 \(D\subseteq V\)，服务节点集合 \(U=V\setminus D\)。终端用于出发或结束，不作为普通客户收取需求、服务时间或收益。

- 每个节点使用稳定 `node_id`；矩阵索引是该 ID 的显式映射。
- 正式规模 \(N=|V|\)，包含该实例所有不同的物理路由节点及终端。另报 `customer_count=|U|`、`terminal_count=|D|` 和 `request_count`。
- 路线中同一仓库的起终两次出现不增加 \(N\)。虚拟起终副本是建模细节，不增加物理节点数。
- ATSP 从选定节点中指定一个锚点作为终端，其余为必访节点；锚点在输出中出现两次只是同一环的表示。
- 配置需要额外仓库时，仓库必须已有真实矩阵行/列；新增真实节点应形成新 BaseInstance，不能无说明地增加零成本虚拟地点。

### 2.2 三种边量分别定义

\[
C=(c_{ij}),\qquad T=(\tau_{ij}),\qquad L=(\ell_{ij}).
\]

| 边量 | 用途 | 单位 |
|---|---|---|
| \(c_{ij}\) | 优化出行成本、成本预算 | 声明的 cost unit，例如秒或货币单位 |
| \(\tau_{ij}\) | 时间传播、时间窗、路线时长 | 秒 |
| \(\ell_{ij}\) | 距离上限 | 米 |

所有有效边必须有限、非负；对角为0。v1要求所选物理节点的完整有向矩阵，不用零值代替缺边。允许 \(c_{ij}=c_{ji}\) 的个别边，但不假设整体对称或三角不等式。`Directed Cost` 表示使用有向矩阵，不能写成“任意一对节点必有 \(c_{ij}\ne c_{ji}\)”。

只有显式声明成本就是秒制行驶耗时且来源一致时，才允许 `cost_matrix` 与 `travel_time_matrix` 指向同一数据。天气加权成本、距离或消费价格不能直接进入时间传播。没有真实距离矩阵时，启用 `distance_limit` 应报输入不完整，不能用耗时代替距离。

### 2.3 静态主问题与时间信息

本规范的 v1主问题在一次求解中固定 \(C,T,L\)。矩阵的采集区间和 `available_at` 是来源及信息可见性字段；窗口和服务时刻是运营时钟，二者不得混用。

历史复用可以提供过去实例及过去实际输出，但当前任务仍按当前固定矩阵校验。未来预测需要单独定义输入截止与目标矩阵。真正出发时间依赖路由需要 \(\tau_{ij}(t)\)、合法可见性和执行模型，不由“存在多帧矩阵”自动获得，本规范不将它计为已定义的静态原子组合。

## 3. 决策与所有配置共有的规则

### 3.1 访问变量

\[
U=U_{\rm req}\,\dot\cup\,U_{\rm opt},\qquad y_i\in\{0,1\}.
\]

必访节点满足 \(y_i=1\)；可选节点可不服务。每个被选择的服务节点恰好由一辆车服务一次。客户不可重复，禁止拆分配送、重复访问、中途补货及中途访问终端。没有启用可选访问时，\(U_{\rm req}=U\)。

所有终端必须在 \(D\) 内，不能同时是服务节点。一个基础POI承担服务或终端角色由Scenario明确指定。

### 3.2 车辆与路线

可用车辆 \(K=\{1,\ldots,M\}\)，车辆启用变量 \(u_k\in\{0,1\}\)。每辆车至多执行一条路线；未使用车辆不输出路线、不产生启用成本、不占显式车辆上限。

车辆 \(k\) 的出发终端为 \(d_k\in D\)，固定出发时刻为 \(r_k\)。`homogeneous` 表示车辆能力参数一致，`heterogeneous` 表示不同容量或启用成本；`single/multi vehicle` 由可用车辆数决定。这两个维度独立。v1使用共享边矩阵；不同车型专属速度/边矩阵属于后续版本。

有效已用路线必须包含至少一个服务节点。输出顺序构成完整有向路径，不允许分离子环。

| `route.end_mode` | 已用路线表示 | 最终节点规则 |
|---|---|---|
| `closed` | \((d_k,v_{k1},\ldots,v_{km_k},d_k)\) | 返回自己的出发终端 |
| `fixed` | \((d_k,v_{k1},\ldots,v_{km_k},e_k)\) | \(e_k\in D\) 显式指定，可与起点不同 |
| `free` | \((d_k,v_{k1},\ldots,v_{km_k})\) | 结束于最后服务的客户，不增加返回边 |

`fixed` 与 `free` 都是开放路径语义，分别记录，不能仅用一个 `open=true` 混同。普通开放配送默认 `free`；点到点OP采用 `fixed`。闭合OP必须作为另一配置报告。

若fixed配置中每车终点都等于其起点，有效语义归一化为closed，不能通过换端点模式名称制造“未见组合”。点到点AOP默认起终端不同。

每个节点在路线中的位置使用“出现位置”索引。闭合路线的仓库首尾是两个出现位置；时间与载荷按位置传播，不能对同一物理仓库套用相互矛盾的循环时间不等式。

### 3.3 解的共同可行条件

1. 已用车辆ID唯一、合法，路线起终符合配置。
2. 客户覆盖与必访/可选规则一致，无重复或中间终端。
3. 所有启用约束均满足；未启用约束不参与校验或目标。
4. 所有使用的边具有有效的原始矩阵值。
5. 算法自己给出的 objective、载荷或可行标志不作为真值，均由独立校验器重算。

可选任务允许全空解，其是否合法由最低收益、必访集合和其他约束决定；全空解的总成本、收益和makespan为0。

## 4. 原子库：一级定义

原子库包含三种模块：结构选择、属性/状态更新和可行性谓词。它们都影响问题语义，但“存在收益字段”与“容量上限”不是同一种约束，复杂度统计时必须区分。

### 4.1 结构维度

| 维度 | 合法取值 | 必填参数/含义 |
|---|---|---|
| Objective | 本文第6节的四类目标 | 方向、单位；混合目标的权重 |
| Visit | 必访/可选集合的划分 | 两集合不相交且并为 \(U\) |
| Fleet | homogeneous / heterogeneous | 可用车辆列表；车辆数量独立记录 |
| Depot | 单终端 / 多终端 | \(D\)、每车固定起点、必要时固定终点 |
| Route | closed / fixed / free | 路线结束语义 |

`multi_depot`、`heterogeneous_fleet`、`open_route` 的特征由上述结构派生，配置不再保留另一套可能冲突的开关。

### 4.2 可选原子注册表

| 稳定ID | 类型 | 参数 | 语义与依赖 |
|---|---|---|---|
| `capacity` | 状态＋谓词 | `mode`、节点需求或请求量、\(Q_k\) | 每一步载荷合法；区分仓库配送与配对取送 |
| `time_window` | 谓词 | 每个相关节点 \([a_i,b_i]\) | 硬服务开始窗；允许等待；终端到达也检查 |
| `service_time` | 状态更新 | 每客户 \(s_i\ge0\) | 计入时间，终端为0；不自动计入出行目标 |
| `route_duration` | 谓词 | 每车 \(H_k\) | 完成时间减出发时间不超过 \(H_k\) |
| `distance_limit` | 谓词 | \(L\)、每车 \(D_k^{\max}\) | 实际行驶边距离总和受限 |
| `cost_budget` | 谓词 | `scope=per_route/total`、上限 | 限制出行成本，不含未访问惩罚；scope显式指定 |
| `prize` | 属性 | \(p_i\ge0\) | 每个已服务客户收益收取一次 |
| `penalty` | 属性 | \(\rho_i\ge0\) | 每个未服务客户惩罚一次 |
| `min_prize` | 谓词 | \(P_{\min}\) | 总收益至少 \(P_{\min}\)，依赖prize |
| `pickup_delivery` | 关系＋状态 | 不重叠配对、每请求 \(q_h>0\) | 同车、先取后送、成对选择；依赖paired容量模式 |
| `precedence` | 关系谓词 | 有向关系 \((i,j)\) | 当二者都被服务时，同车且i在j之前 |
| `same_vehicle` | 关系谓词 | 无向节点对 | 当二者都被服务时，由同车服务 |
| `different_vehicle` | 关系谓词 | 无向节点对 | 当二者都被服务时，由不同车服务 |
| `vehicle_limit` | 谓词 | \(B_{\rm veh}\le M\) | \(\sum_k u_k\le B_{\rm veh}\)，与可用车队大小区别 |

`time_budget`若表示运营总时长，只作为 `route_duration` 别名；若表示算法运行时间，属于评测预算而不是路由原子。`distance_limit` 与 `cost_budget` 不互为别名。服务时间与route duration不能因为同属Time被合并。

v1 hard约束之外的软时间窗、分割需求、跨车转运、车流反馈、途中补货和多趟车不在本规范中。求解器遇到这些输入不得静默按v1弱化。

## 5. 原子的精确数学语义

### 5.1 时间、等待与完成时刻

在路线位置 \(h\) 的节点记为 \(v_h\)，服务开始为 \(b_{kh}\)，离开为 \(d_{kh}\)，到达为 \(a_{kh}^{\rm arr}\)。出发时刻固定，不允许通过推迟发车逃避route duration约束。

起点：\(b_{k0}=d_{k0}=r_k\)。对后续位置：

\[
a_{kh}^{\rm arr}=d_{k,h-1}+\tau_{v_{h-1},v_h},\qquad
b_{kh}\ge a_{kh}^{\rm arr},\qquad
d_{kh}=b_{kh}+s_{v_h}.
\]

启用time window时还需：

\[
a_{v_h}\le b_{kh}\le b_{v_h}.
\]

服务开始不晚于上界即可，服务完成可以晚于该客户窗口上界；若要求完成前截止，须在未来版本引入另一原子，不暗中改语义。服务时间关闭时所有 \(s_i=0\)。时间窗开启时，已用车辆起点的固定 \(r_k\) 也必须位于起点窗内。

固定终点/闭合路线末终端服务时间为0，窗口作用于末终端的服务开始（即允许等待后的到达）。自由终点没有额外终端窗，其完成时刻为最后客户服务完成。

\[
F_k=d_{k,\rm last},\qquad F_k-r_k\le H_k.
\]

v1只有路线内部顺序关系，没有跨车辆时间同步。对任一固定路线，按 \(b_{kh}=\max(a_{kh}^{\rm arr},a_{v_h})\) 递推得到最早日程；无窗口时直接取到达时刻。由于约束只有服务开始上下界和时长上界，若最早日程失败，加入额外等待不能救回该路线。不得把局部下一步可行当作整个未完成任务可行。

### 5.2 仓库配送容量：`depot_delivery`

每客户具有 \(q_i\ge0\)，路线出发载荷由已选客户共同决定：

\[
L_{k0}=\sum_{i\text{ served by }k}q_i,\qquad
L_{kh}=L_{k,h-1}-q_{v_h},\qquad
0\le L_{kh}\le Q_k.
\]

在禁止补货、拆分且仅配送的条件下，等价于 \(\sum_{i\in R_k\cap U}q_i\le Q_k\)，服务完后载荷为0。可选客户不访问就不装载其需求。

### 5.3 配对取送容量：`paired_pickup_delivery`

每请求 \(h=(p_h,d_h,q_h)\)，起点和终点是不同服务节点；不同请求的端点不重叠。v1该容量模式要求所有服务节点由请求配对覆盖，不混入普通仓库配送节点。

\[
y_{p_h}=y_{d_h},\qquad
k(p_h)=k(d_h),\qquad
\operatorname{pos}_k(p_h)<\operatorname{pos}_k(d_h).
\]

若请求必选，两个端点都属于必访集合；若可选，两个端点都属于可选集合。禁止只选择其中一个端点。

\[
\Delta_{p_h}=q_h,\quad\Delta_{d_h}=-q_h,\quad
L_{k0}=0,\quad L_{kh}=L_{k,h-1}+\Delta_{v_h},\quad
0\le L_{kh}\le Q_k,\quad L_{k,\rm end}=0.
\]

取送不能用整条路线的净需求和约束替代：净和为0也可能在中途超载。自由终点也必须完成所有已选请求，不能携带未配送货物结束。

PickupDelivery内生包含same-vehicle与precedence，不要求重复启用这两个原子。额外precedence/same-vehicle只用于其他关系，并且独立记录。

### 5.4 一般关系

v1 `precedence(i,j)` 定义为：当 \(y_i=y_j=1\) 时，两者同车且i先于j。它不自行强制选择i或j，也不表达跨车时钟顺序。`same_vehicle`/`different_vehicle` 也只在两端都被选择时生效。若业务要求“选j必须选i”，不能只写precedence；v1通过强制必访或pickup-delivery成对选择表达，其他一般选择蕴含留后续版本。

关系中节点不存在属于输入错误。合法节点上的关系冲突或强制precedence环可以产生不可行实例，应保留其问题语义，而不是把真正不可行全部当作格式错误过滤。

### 5.5 收益、惩罚与资源

\[
P(X)=\sum_{i\in U}p_i y_i,\qquad
\Pi(X)=\sum_{i\in U}\rho_i(1-y_i),\qquad
P(X)\ge P_{\min}\quad\text{if min-prize enabled}.
\]

收益按已服务节点一次计数，不按经过节点或路线中的重复终端计数。配对取送若表示请求收益，应事先将收益分配给其端点且使端点合计等于请求收益；不能两端各收完整请求收益。

记已用路线边集合（按顺序的多重集）为 \(E_k(X)\)：

\[
C_k(X)=\sum_{(i,j)\in E_k(X)}c_{ij},\qquad
D_k(X)=\sum_{(i,j)\in E_k(X)}\ell_{ij}.
\]

闭合/固定终点包含末终端边，自由终点没有返回边。距离限制为 \(D_k(X)\le D_k^{\max}\)，成本限制为 \(C_k(X)\le B_k\) 或 \(\sum_k C_k(X)\le B_{\rm total}\)，不能根据含糊的“预算”自行选择量纲。

## 6. 目标函数

车辆启用成本 \(f_k\ge0\) 默认0，与出行cost同单位。定义：

\[
C_{\rm total}(X)=\sum_{k:u_k=1}(C_k(X)+f_k).
\]

| `objective.type` | 方向与定义 | 必需字段 |
|---|---|---|
| `min_total_cost` | \(\min C_{\rm total}(X)\) | cost；显式启用成本或默认0 |
| `min_makespan` | \(\min[\max_{k:u_k=1}F_k-t_{\rm origin}]\)；空解为0 | travel time、固定出发时刻与统一时钟原点 |
| `max_prize` | \(\max P(X)\) | prize及限制可服务范围的资源/容量/时间等 |
| `min_cost_plus_penalty` | \(\min[w_c C_{\rm total}(X)+w_p\Pi(X)]\) | penalty；\(w_c>0,w_p\ge0\)，成本与惩罚统一目标单位 |

`min_makespan`是统一时钟下的最晚完成时间，不是 `max(F_k-r_k)`；各车发车不同则二者可能不同，后一目标需另行命名。混合目标的权重必须在输入中给定，不能由solver自行选取。

目标决定优化方向，原子决定可行域/状态和目标所需属性。`capacity + prize + open_route`仍不完整，必须给出目标、访问规则与限制：例如最大收益＋可选访问＋单车＋容量＋自由终点＋时长上限，才形成可执行场景。

v1不使用隐含的“先少车，再最短距离”字典序目标。需要该目标时应登记未来版本或明确的多目标协议，不能用本规范 `min_total_cost` 默认代表它。

以下配置数学上合法但可能退化：纯可选访问＋最小成本＋无必访/惩罚/最低收益时，空解最优；全必访＋最大节点收益时，所有可行解收益相同。标记 `degenerate_objective`，仅用于诊断，不纳入主质量榜。不能错误地称这些问题无界。

## 7. 合法配置、依赖闭包与归一化

### 7.1 基础约束

节点ID、矩阵映射和角色必须完整；必访/可选集合准确划分服务节点。车辆数有限、每车参数有效，capacity开启时 \(Q_k>0\)。所有数值有限，上下限非负，时间窗有 \(a_i\le b_i\)，关系端点合法。

属性有值不代表启用；关闭的原子不参与求解。v1 Scenario只携带当前有效属性，未启用字段不放入solver公开输入。缺失开关归一化为关闭；缺失启用参数报输入错误，不能默认无穷大、0需求或“忽略约束”。

### 7.2 依赖与冲突规则

| 配置 | 归一化要求 |
|---|---|
| time window / service time / route duration / min makespan | 必须有秒制travel time；service time关闭时使用0 |
| distance limit | 必须有米制distance矩阵 |
| max prize / min prize | 启用prize并提供非负收益；主质量榜max prize须非退化 |
| min cost plus penalty | 启用penalty并提供目标单位及权重 |
| pickup delivery | 启用capacity且mode为paired；生成内生同车/先后/成对选择条件 |
| paired capacity | 必须启用pickup delivery；与depot-delivery模式互斥 |
| homogeneous fleet | 车辆能力参数一致；不同起终仓库不自动变成异构车队 |
| fixed end | 每车end_node在D；closed终点由start_node派生；free不指定end_node |
| multi depot | 由终端集合/分配派生，所有终端都有矩阵数据 |
| explicit vehicle limit | \(0\le B_{\rm veh}\le M\)；0上限可以用于认证不可行案例 |

依赖的开关不被静默补成新的任务；缺失依赖时给 `INPUT_INVALID` 并要求修正配置。成功归一化后输出依赖闭包与所诱导的逻辑约束，供签名、split和审计使用。

另外移除可直接判断的语义重复：fixed终点全等起点归为closed；声明异构但有效能力/启用成本全部一致时归为同构；只复述pickup请求内生先后/同车条件的关系不增加独立原子。全0服务时间不增加有效service-time特征。保留原输入及归一化记录；这里只消除明确重复，不声称能够穷尽所有组合的数学等价性。

### 7.3 不可行与输入错误分别处理

| 状态 | 定义 | 例子 |
|---|---|---|
| INPUT_INVALID | 无法构成本文定义的问题 | 窗口缺失、耗时单位未知、矩阵缺边、角色重叠 |
| VALID_FEASIBLE | 问题定义完整且至少存在一个可行解 | 隔离witness或独立解验证 |
| VALID_INFEASIBLE | 问题定义完整但可行域为空，且有证明 | 配送全必访且总需求超过可用车容量总和 |
| FEASIBILITY_UNKNOWN | 有效问题尚无可行解或不可行证明 | 有限时间搜索未找到路线 |

对可选服务或取送净载荷，不能直接套用 `sum(demand)>sum(capacity)` 判断不可行。必访仓库配送的该不等式是充分的不可行证据，但反向成立也不保证可行。构造失败、超时、返回invalid均不是不可行证明。

## 8. Canonical Templates：配置的辅助名称

下表固定本benchmark的默认模板；文献同名问题可能有其他变体，正式实验必须附完整配置签名。服务时间默认0，可在带窗变体显式开启。

| 模板 | 目标 | 访问 / 车辆 / 端点 | 核心原子 |
|---|---|---|---|
| ATSP | min total cost | 全必访；单车；闭合；一个锚点 | 有向矩阵为基础规则，无可选原子 |
| ACVRP | min total cost | 全必访；多车同构；单仓闭合 | depot-delivery容量 |
| AVRPTW | min total cost | 全必访；多车同构；单仓闭合 | 服务开始时间窗；service time独立可选 |
| ACVRPTW | min total cost | 全必访；多车同构；单仓闭合 | depot-delivery容量＋时间窗；service time独立可选 |
| AOP | max prize | 全可选；单车；不同固定起终端 | prize＋route duration |
| PCTSP | min cost plus penalty | 全可选；单车；单仓闭合 | prize＋penalty＋min prize |
| AOVRP | min total cost | 全必访；多车同构；单仓自由终点 | depot-delivery容量 |
| AMDVRP | min total cost | 全必访；多车同构；多仓闭合 | depot-delivery容量；每车起点预先指定 |
| APDP | min total cost | 所有请求必选；多车同构；单仓闭合 | paired容量＋pickup delivery |
| APDPTW | min total cost | 所有请求必选；多车同构；单仓闭合 | paired容量＋pickup delivery＋时间窗 |
| AHCVRP | min total cost | 全必访；多车异构；单仓闭合 | depot-delivery容量；不同Q/f允许 |

`CVRP/VRPTW/OP/PDP`可作显示别名，但有向协议以带A模板ID和完整签名为准。AOP的“时间预算版本”与“距离预算版本”、闭合与点到点版本签名不同。AMDVRP不隐含优化仓库分配；v1车队仓库分配给定，优化分配留后续版本。

`canonical_task`是可选标签，不参与推导参数、不改变checker。若标签与配置不匹配，报告 `template_mismatch` 并移除标签；评测仍以规范配置为准，不按名字修正问题。没有匹配模板则标签为null。

## 9. Compositional Problems：完整的无名称组合

无名称场景仍须给足目标、访问、车辆、端点与原子参数。以下是规范组合，所有数值由实例具体给定：

| 场景ID | 目标与访问 | 车队/端点 | 原子组合 |
|---|---|---|---|
| `comp_capacity_prize_open_duration` | max prize；全可选 | 单车；free | depot-delivery容量＋prize＋route duration |
| `comp_multidepot_tw_open` | min total cost；全必访 | 多车；多仓；free | time window＋service time |
| `comp_pd_open_duration` | min total cost；全部请求必选 | 多车；单仓；free | paired容量＋pickup delivery＋route duration |
| `comp_penalty_hetero_tw` | min cost plus penalty；必访/可选混合 | 多车异构；closed | depot-delivery容量＋time window＋penalty |
| `comp_prize_tw_fixedend` | max prize；全可选 | 单车；fixed | prize＋time window＋service time＋route duration |
| `comp_pd_prize_multidepot` | max prize；请求成对可选 | 多车；多仓；closed | paired容量＋pickup delivery＋prize＋route duration |

这些组合不宣称没有相关文献名称或首创；其用途是测试按语义组合处理任务的能力。不得把“没有提供缩写”直接等同于“模型预训练从未见过”。

## 10. 配置表示、签名与复杂度

### 10.1 可读向量与真实定义

按 `problem_catalog.json` 固定顺序，14个可选原子产生 \(z^{\rm atom}\in\{0,1\}^{14}\)。另给三个派生结构特征（multi depot、heterogeneous fleet、open route）和端点具体枚举。

\[
z\ne\text{完整问题定义}.
\]

例如OP和PCTSP即使都含prize，目标、惩罚、最低收益与端点也不同。单个布尔向量不能建立“problem↔configuration”一一对应；结构化配置＋具体参数才能唯一确定任务实例。

- `config_signature`：规范版本、目标类型、访问模式、车队类型/单多车、端点模式、有效原子ID及模式、关系语义、资源scope。数值不进入此结构签名。
- `instance_signature`：base hash＋归一化Scenario全部有效参数hash。
- `effective_signature`：结构签名连同依赖闭包/内生条件；用于组合泄漏检查。
- 数值紧度、车数、收益/窗口分布另作为参数分层，不能仅靠更换seed称未见组合。

访问模式含all-required、all-optional、mixed；对于mixed，用模式作为结构签名、节点具体划分放实例签名。开放模式free/fixed不能折叠成同一个测试组合。

### 10.2 复杂度统计

\[
K_{\rm atom}=\sum_j z_j^{\rm atom}.
\]

同时报告 \(K_{\rm hard}\)（显式启用的谓词/关系原子数量）、结构特征、紧度和规模。prize/penalty/service time影响目标或状态，不混称新增硬不等式。pickup内生的same-vehicle/precedence不重复增加原子数；另行独立启用的额外关系计入。

`K_atom=0`不表示无约束或容易：ATSP仍有覆盖、单环与端点基础规则。相同K不意味着相同难度；tightness、目标和交互均需分层。

\[
\widehat h(z)=\beta_0+\sum_i\beta_i z_i+\sum_{i<j}\beta_{ij}z_i z_j
\]

可以作为开发集上的经验分析模型，系数依赖求解器、预算、分布和指标，不能表述为客观复杂度定理。不得用测试结果拟合权重后重新选取测试配置。展示 `FeasibleRate(N,K)`、可行质量和完整耗时，所有数字必须来自实际实验。

## 11. 泛化协议的严格定义

定义开发阶段全部可用任务结构集合为 \(Z_{\rm dev}\)，有效原子集合为 \(A_{\rm dev}\)。开发阶段包括train/validation、few-shot、RAG任务案例、算法生成与公开调试；仅排除梯度训练数据不足以保证组合未暴露。

| 协议 | 必须成立的条件 |
|---|---|
| Seen Composition | 测试有效结构已在开发阶段出现，换独立母实例；不自动宣称严格IID |
| Cross-City | 测试城市无开发实例；约束配置保持已见以单独隔离城市变化 |
| Cross-Time | 前向日期/时间块划分，测试目标数据按available_at不可提前见 |
| Cross-Scale | 测试N未参与开发，城市/配置尽量匹配；共享母图必须披露 |
| Unseen Composition | 测试effective signature不在开发集合，所有原子在开发任务出现过 |
| Unseen Atom | 至少一个测试原子从未出现在开发任务，且adapter/RAG没有泄露该任务解模板 |
| Cross-City + Composition | 同时满足新城市与未见组合条件 |

“未见”只针对可审计的本benchmark开发资源。基础模型预训练不可完全核验时，应写benchmark-unseen，不能宣称绝对未接触。上述协议不规定性能必然从易到难排序；不同solver可能表现不同。

Unseen Composition另分两种，不混报：

1. **Exact configuration held out**：仅完整有效结构未见；训练可能出现其子组合或更大组合，必须披露。
2. **Co-occurrence held out**：例如测试capacity＋time window，开发任何任务都不含二者同时激活的有效语义，包括更大组合；二者分别单独出现。此协议更直接测试新交互。

在dependency closure上审查而不是仅看开关。例如pickup任务已经含same-vehicle与precedence；不能据此声称这两个语义在开发中完全未见。

同母图的子集、约束派生、语言改写和翻译必须分组。跨规模允许共享母图的协议单独标“shared-base scale”；严格独立泛化使用不同母图。不能为满足两个冲突划分要求而静默拆开相关样本。

主LLM约束理解输入不提供canonical名称，包含与JSON等价的约束描述和完整矩阵；named-template输入作为单独对照。禁止自然语言新增或漏掉JSON约束。

## 12. 输入、输出与状态契约

### 12.1 输入

统一为 `BaseInstance + Scenario`，不按问题名称分别设计互不兼容的数据格式。

| 层 | 最低内容 |
|---|---|
| BaseInstance | schema_version、base_id、node_ids、矩阵及单位、来源/available_at与hash |
| Scenario | scenario_id、base_id、objective、visit、fleet、depots、route、enabled constraints、有效attributes |
| Task metadata | canonical_task可选、split、effective signature、字段来源、输入可见性与算法预算 |

Scenario中的 `constraints` 用 `{enabled, mode/scope/limit...}` 对象；节点属性按node_id索引，矩阵按 `node_ids` 索引，不能只凭两数组等长配对。每个派生业务字段附REAL/PROVIDER_DERIVED/DERIVED/SEMI_SYNTHETIC/SYNTHETIC标签；来源不影响数学约束，但影响可对外声称的真实性。

伴随文件 `example_acvrptw.json` 给出完整小规模Base＋Scenario＋Solution，没有省略矩阵或未定义“预算”。这是构造示例，不是采集数据。

### 12.2 输出

```json
{
  "schema_version": "realroute.problem.v1",
  "scenario_id": "example_acvrptw_4",
  "status": "feasible",
  "routes": [
    {"vehicle_id": "v1", "node_ids": ["d", "a", "d"]},
    {"vehicle_id": "v2", "node_ids": ["d", "b", "c", "d"]}
  ]
}
```

有时间语义时，solver可附逐出现位置的service_starts；不给则checker使用最早日程。给定日程时按其实际时刻检查，不把不合法日程偷偷修成另一个解。`min_makespan`按经验证日程计算，因此输出额外等待会影响目标。

收益、访问集、载荷与objective可附带但均需重算。路线列表为空表示没有启用车辆。取送、容量、窗口等真值不得靠模型自报。

### 12.3 求解状态与评测状态分离

solver可报告 `feasible`、`infeasible_claim`、`no_solution`、`unsupported`；超时、执行错误和输出错误由harness观测。checker给出：

- `VALID_FEASIBLE_SOLUTION`：完整输出通过所有当前约束。
- `INVALID_SOLUTION`：返回路线违反覆盖/端点/容量/时间/关系等，并给原子级原因。
- `PROVEN_INFEASIBLE`：参考证书或独立认证支持可行域为空。
- `UNVERIFIED_INFEASIBLE_CLAIM`：仅声称不可行，没有证明。
- `NO_VALID_SOLUTION`：无输出、超时、错误或unsupported；仍保留具体子状态。

小规模不可行诊断单列；不能把“所有不可行样本都拒答”计入正常路线可行率，也不能把拒答当不可行检测的正确证据。定义良好的有效任务上unsupported计为该方法未完成，不从主成功率分母中删除。

## 13. 评测与校验义务

checker读取规范化配置，顺序执行：输入有效性→车辆与端点→访问覆盖→成对选择/关系→逐位置载荷→时间日程→运营资源→收益/惩罚→目标。输出每个失败原子和首个失败位置，隐藏测试的逐项信息不反馈给调参过程。

数学定义使用精确不等式。运行实现使用float64重算，并在数据版本中冻结每一量纲的数值容差；数值容差只处理舍入，不充当百分比业务放宽。节点ID、覆盖、同车、先后和配对等离散条件零容差。任何目标取整及整数solver缩放同时记录，并在原矩阵单位下复算。

质量只对可行解计算，并同时报告全任务成功率以保留失败：

\[
\mathrm{Success}_{\epsilon,B}(X)=
\mathbf1[\text{feasible}\land\text{returned within }B\land\text{gap}\le\epsilon].
\]

最小化/最大化gap方向相反，reference标EXACT或BKS，bounds单列。不能把匹配启发式BKS称认证最优。运营route duration与算法wall-clock budget分别判断：一条合法短路线也可能因算法超时而不满足评测成功条件。

统一报告结构配置、规模、紧度、可行率、质量、超时和完整资源成本。两组榜单是同一实例体系的两个视角：canonical便于阅读和比较，constraint-generalization展示已见/未见组合与原子能力。固定名称不会替代配置签名。

## 14. 定义完成的验收清单

| 检查项 | 本规范的确定答案 |
|---|---|
| 谁决定问题语义？ | Base＋归一化Scenario；canonical名称仅为标签 |
| cost等于时间吗？ | 默认不等；只有显式一致声明才可共享数据 |
| 时间窗作用于什么？ | 服务开始；终端也检查；允许等待 |
| Open Route在哪结束？ | fixed与free分别定义；不添加不存在的返回边 |
| 取送容量如何算？ | 按访问顺序增减，起始与结束0载荷 |
| 可选访问会漏服务吗？ | 必访必须覆盖；可选取送必须整对选择 |
| 缺参数可忽略吗？ | 不可；输入错误与不可行分开 |
| 布尔向量是否唯一确定问题？ | 否，目标/结构/参数/依赖也必须给定 |
| 约束多就一定难吗？ | 否，K是描述指标，需控制紧度和交互 |
| 未见组合怎样检查？ | 有效签名及依赖闭包；exact与co-occurrence区分 |
| 是否已经实现所有问题？ | 本次完成定义及目录；生成器/通用checker/solver运行不在此完成状态内 |

后续实现必须以本规范及机器目录为准；新语义通过版本扩展，不能用适配器隐含改变任务。
