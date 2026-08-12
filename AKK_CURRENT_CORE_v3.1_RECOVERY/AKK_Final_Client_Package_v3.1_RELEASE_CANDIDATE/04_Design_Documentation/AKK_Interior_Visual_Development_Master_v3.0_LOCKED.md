---
schema_version: 1
id: akk-interior-visual-development-master-v3-0
title: AKK Interior & Visual Development Master v3.0 — LOCKED
type: project-visual-development-master
status: CONTROLLED_REFERENCE
lifecycle_stage: LOCKED_REFERENCE
created: 2026-08-10
updated: 2026-08-10
owner: alan
language: zh-CN
categories:
  - project
  - interior
  - visual-development
tags:
  - project/akk
  - baseline/v3.0
  - status/locked-reference
source: AKK MASTER v3.0 Engineer Drawing Baseline plus controlled Ground, First, Second and Roof engineer drawings
confidence: medium-high
sensitivity: internal
publish: false
rag: false
---

# AKK Interior & Visual Development Master v3.0 — LOCKED

> **Status: LOCKED REFERENCE / NOT CURRENT CONTROL**
>
> The sole project-level CURRENT Master is `01_Master_Baseline/AKK_Master_Baseline_v3.0.md`.

## 1. 控制依据

1. 当前几何与空间控制基准：`AKK_Master_Baseline_v3.0.md`。
2. 现已受控归档的原图：Ground、First、Second与Roof Floor工程师图纸。
3. 四张楼层原图均已完成字节级验证；图纸未表达的专业细节继续保持`VERIFY`。
4. 旧v2.2仅保留历史证据；与v3.0冲突的参数停止用于当前生产。

## 2. 本次PDF核验

| 核验项 | 图面证据 | v3.0基准 | 结论 |
|---|---|---|---|
| PDF页数 | 1页 | 应有Ground / First / Second / Roof四张控制图 | **VERIFY — 本PDF不是四图完整来源** |
| 楼层标题 | Ground Floor Plan | Ground Floor — Community Level | **MATCH** |
| 建筑外轮廓 | 110' × 60' | 110' × 60' | **MATCH** |
| 横向尺寸链 | 15' + 15' + 15' + 20' + 15' + 15' + 15' | 同值，共110' | **MATCH** |
| 纵向尺寸链 | 25' + 10' + 25' | 同值，共60' | **MATCH** |
| Ground功能 | Study Room、Store、Dining Area、Reception、Office、Lobby、Female toilet、Male toilet | 同一功能清单 | **MATCH** |
| 中央楼梯 | 图面中央可见双跑楼梯 | Central Stair / 20 ft Stair Module | **MATCH（20 ft来自尺寸链及基准）** |
| First Floor | 本Ground PDF未包含；另有First独立受控原图 | Girls Hostel / 46 Beds | **SEPARATELY VERIFIED — 见补充核验** |
| Second Floor | 本Ground PDF未包含；另有Second独立受控原图 | Boys Hostel / 46 Beds | **SEPARATELY VERIFIED — 见补充核验** |
| Roof Floor | 本Ground PDF未包含；另有Roof独立受控原图 | Bath & W.C、Kitchen & Dining标签；细节待核 | **SEPARATELY VERIFIED — 见补充核验** |
| 参数冲突 | 本页未见110'×66'、30'+6'+30'、96床等旧参数 | 上述旧参数已退役 | **NO CONFLICT VISIBLE** |

### First Floor补充图核验

| 核验项 | 图面证据 | v3.0基准 | 结论 |
|---|---|---|---|
| PDF页数 | 1页 | First独立工程师原图 | **MATCH / PARTIAL SET** |
| 楼层及用途 | `First Floor Plan`；`46 nos. Girls Hostel` | Girls Hostel / 46 Beds | **MATCH** |
| 房型与床位 | 10处4-Bed + 1处6-Bed = 46 Beds | 10×4-Bed + 1×6-Bed = 46 Beds | **MATCH** |
| 建筑外轮廓 | 110' × 60' | 110' × 60' | **MATCH** |
| 横向尺寸链 | 15' + 15' + 15' + 20' + 15' + 15' + 15' | 同值，共110' | **MATCH** |
| 纵向尺寸链 | 25' + 10' + 25' | 同值，共60' | **MATCH** |
| 中央楼梯 | 位于中央20'开间 | Central 20 ft Stair Module | **MATCH；20'为结构开间，不等于净梯宽** |
| 湿区 | 上部左、右端各一组镜像湿区 | 旧基准称“左侧区域” | **CONFLICT RESOLVED — 以原图左右双湿区为准** |
| W/C / Shower | 左右各5个，共10个W/C及10个Shower隔间 | 仅给出设施类型 | **MATCH / DETAIL ADDED** |
| Basin | 左右各1组；图形约10个盆位 | 仅给出Basin类型 | **MATCH；单盆规格VERIFY** |

### Second Floor补充图核验

| 核验项 | 图面证据 | v3.0基准 | 结论 |
|---|---|---|---|
| PDF页数 | 1页 | Second独立工程师原图 | **MATCH / PARTIAL SET** |
| 楼层及用途 | `Second Floor Plan`；`46 nos. Boys Hostel` | Boys Hostel / 46 Beds | **MATCH** |
| 房型与床位 | 10处4-Bed + 1处6-Bed = 46 Beds | 10×4-Bed + 1×6-Bed = 46 Beds | **MATCH** |
| 建筑外轮廓 | 110' × 60' | 110' × 60' | **MATCH** |
| 横向尺寸链 | 15' + 15' + 15' + 20' + 15' + 15' + 15' | 同值，共110' | **MATCH** |
| 纵向尺寸链 | 25' + 10' + 25' | 同值，共60' | **MATCH** |
| 中央楼梯 | 位于上部中央20'开间并连接10'走廊 | Central 20 ft Stair Module | **MATCH；20'不是净梯宽** |
| 湿区 | 上部左、右端各一组镜像湿区 | 基本延续First Floor | **MATCH** |
| W/C / Shower | 左右各5个，共10个W/C及10个Shower隔间 | W/C + Shower配置 | **MATCH / DETAIL ADDED** |
| Basin | 左右各1组；图形约10个盆位 | Basin配置 | **MATCH；单盆规格VERIFY** |
| 门窗/墙体 | 11间宿舍均由10'走廊进入；外围可见窗；湿区入口未见门扇弧 | 必须保持原图关系 | **LOCKED；门表、窗表及构造规格VERIFY** |

### Roof Floor补充图核验

| 核验项 | 图面证据 | v3.0基准 | 结论 |
|---|---|---|---|
| PDF页数 | 1页 | Roof独立工程师原图 | **MATCH / PARTIAL SET** |
| 楼层标题 | `Roof Floor Plan` | Roof Floor | **MATCH** |
| 建筑外轮廓 | 110' × 60' | 110' × 60' | **MATCH** |
| 横向尺寸链 | 15' + 15' + 15' + 20' + 15' + 15' + 15' | 同值，共110' | **MATCH** |
| 纵向尺寸链 | 25' + 10' + 25' | 同值，共60' | **MATCH** |
| 中央楼梯 | 位于上部中央20'模块内 | Central 20 ft Stair Module | **MATCH；20'不是净梯宽** |
| Bath & W.C | 右上围合空间；可见门、窗式开口及一个洁具式符号 | 保留工程师标注 | **MATCH；洁具类型、面积及完整配置VERIFY** |
| Kitchen & Dining | 右侧上半部较大围合空间；可见门式及窗式开口 | 保留工程师标注 | **MATCH；未见厨房设备，内部边界及布局VERIFY** |
| 其余屋面 | 大面积未分隔、未标注 | 大面积开放空间方向 | **PARTIAL MATCH；实际用途VERIFY** |
| 与Second垂直关系 | 总尺寸、尺寸链、中央模块及楼梯大体位置一致 | 保持垂直关系 | **MATCH；逐线叠合VERIFY，无明确CONFLICT** |

## 3. Ground Floor锁定输入

- Building Footprint：`110' × 60'`。
- Horizontal Grid：`15' | 15' | 15' | 20' | 15' | 15' | 15'`。
- Vertical Grid：`25' | 10' | 25'`。
- 当前功能：Study Room、Store、Dining Area、Reception、Office、Lobby、Female Toilet、Male Toilet、Central Stair。
- 不得修改：建筑外轮廓、轴网、柱网、楼梯、墙线、湿区、门窗。
- 允许深化：家具、材质、灯光、软装、配色、导视、空间编号及视觉层次。

## 4. Interior & Visual Development方向

### 设计语言

- `Japanese Privacy × Singapore Efficiency`
- `Warm Natural Boutique`

### 材质与色彩

- Warm White / Warm Beige
- Natural Wood
- Charcoal Grey

### Pod与住宿层重点

- Privacy
- Personal Storage
- Reading Light
- Individual Power
- Corridor Material and Room Identity

First与Second Floor均已完成原图归档及几何基准核验，可按锁定墙线、湿区、楼梯、中央交通带、门窗和柱网开展室内及视觉深化，但不得冒充施工批准。

### Ground与Roof重点

- Ground：Clean、Calm、Modern、Student Friendly。
- Roof：按受控原图保持外轮廓、尺寸链、中央楼梯及右侧围合空间；`Bath & W.C`、`Kitchen & Dining`仅按图面可见边界控制，不得自行补充面积、设备或内部布局。

## 5. 生产门槛

- CAD、3D、家具、灯光、材质和客户展示必须先核对对应楼层工程师原图。
- 不得把客户视觉图、概念图或3D图称为批准施工图。
- 结构、消防、疏散、机电及法定合规继续由相应专业人员审核。
- Roof图纸未表达的洁具、厨房设备、室内尺寸、屋面用途、排水、防护和逐线垂直对位保持`VERIFY`。

## 6. 受控原图登记

| 文件 | 页数 | 内容 | 字节 | SHA-256 | 状态 |
|---|---:|---|---:|---|---|
| `Controlled_Engineer_Drawings_v3.0/AKK_Ground_Floor_Engineer_Drawing_2026-08-10.pdf` | 1 | Ground Floor Plan | 93,769 | `c8e4ebc3e97c39108d0e50f54087cee06b56edb0dd6051033c1723b1deba3386` | CONTROLLED / VERIFIED |
| `Controlled_Engineer_Drawings_v3.0/AKK_First_Floor_Engineer_Drawing_2026-08-10.pdf` | 1 | First Floor Plan / 46 Girls Hostel | 93,942 | `2751a43af3a07750679bac5b0697194f12507edaba9ee5bf1ce04c3ae06df92b` | CONTROLLED / VERIFIED |
| `Controlled_Engineer_Drawings_v3.0/AKK_Second_Floor_Engineer_Drawing_2026-08-10.pdf` | 1 | Second Floor Plan / 46 Boys Hostel | 165,772 | `5cd342d28a3c3d2f28d6565b457262d857a28985271de95ad284c91a8d4d1304` | CONTROLLED / VERIFIED |
| `Controlled_Engineer_Drawings_v3.0/AKK_Roof_Floor_Engineer_Drawing_2026-08-10.pdf` | 1 | Roof Floor Plan | 91,643 | `e7386014ea9e3518096cdbdba9286251d8c5595cecf88e9843a5694929a5d514` | CONTROLLED / VERIFIED |

## 7. 锁定声明

本文件锁定AKK室内与视觉开发的当前生产边界，但不替代工程师原图。Ground、First、Second与Roof四张原图均已完成受控归档及字节级验证；图纸未表达的结构、消防、机电、门窗、设备、屋面用途及构造细节继续保持`VERIFY`。
