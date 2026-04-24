# 🧠 Tiered Recall — 分层回忆系统

> 解决大模型上下文长度限制，保持跨会话项目延续性

[![version](https://img.shields.io/badge/version-1.2.0-blue)](./SKILL.md)
[![license](https://img.shields.io/badge/license-MIT-green)](#)
[![author](https://img.shields.io/badge/author-davidme6-orange)](https://github.com/davidme6)

---

## 🎯 解决的问题

大模型上下文有限（约20万token），复杂项目可能跨多天、多窗口进行。每次新会话开始时，如何快速恢复上下文，保持工作延续性？

**常见痛点：**
- 新开窗口，之前的项目背景全部丢失
- 跨天任务，第二天不记得昨天做了什么
- 多项目并行，切换时混乱
- 手动回顾太慢，浪费时间

---

## 🚀 解决方案：四层自动加载

| 层级 | 内容 | Token 预算 | 加载条件 |
|------|------|-----------|----------|
| 🔴 L0 核心 | `MEMORY.md` | ~4k | 始终加载 |
| 🟠 L1 近期 | 最近 2 天日志 | ~10k | 始终加载 |
| 🟡 L2 项目 | 活跃项目文件 | ~5k | 自动检测 |
| 🟢 L3 索引 | 记忆索引 | ~3k | 始终加载 |
| **总计** | | **~22k** | 约占上下文 11% |

---

## 🐛 v1.2.0 重要 Bug 修复

**问题（v1.1.0）：** L3 索引存储了每条记忆的摘要文本，实际消耗达 **34k token**（超出预算 33 倍）。

**修复（v1.2.0）：** 改用 slim index 格式，只存 `文件路径:行号`，不存摘要：

```python
# ✅ v1.2.0 正确格式（slim）
ref = f"{file.name}:{section['lines']}"   # "2026-03-23.md:100-200"
index["topics"].setdefault(topic, []).append(ref)
# 结果：每条 ~30 字符，总计 ~3k token（-91%）

# ❌ v1.1.0 错误格式（已废弃）
# {"file": "...", "lines": "...", "summary": "300字摘要..."}  → 34k token
```

**效果：** L3 从 34k → 3k token（**-91%**），总启动上下文从 50k → 22k（**-56%**）

---

## 📂 文件结构

```
workspace/
├── MEMORY.md                    # L0 核心记忆（长期）
├── memory/
│   ├── 2026-04-24.md            # 每日日志
│   └── ...
├── .tiered-recall/
│   ├── index.json               # L3 记忆索引（slim 格式）
│   ├── projects.json            # 活跃项目清单
│   └── state.json               # 加载状态
└── skills/tiered-recall/
    └── SKILL.md
```

---

## 🎮 手动深度回忆

| 指令 | 作用 |
|------|------|
| `回忆 [项目名]` | 加载该项目全部记忆 |
| `回忆最近7天` | 加载指定天数日志 |
| `回忆 [日期]` | 加载指定日期日志 |
| `回忆 [关键词]` | 按关键词搜索记忆 |
| `继续回忆` | 加载更多相关记忆 |

---

## ⚙️ 配置

```json
{
  "defaultLayers": ["L0", "L1", "L2", "L3"],
  "recentDays": 2,
  "maxTokensPerLayer": {
    "L0": 4000,
    "L1": 10000,
    "L2": 5000,
    "L3": 3000
  },
  "deepRecallBudget": 50000,
  "autoLoadOnNewSession": true
}
```

---

## 📈 效果对比

| 场景 | 无分层回忆 | 有分层回忆 |
|------|-----------|-----------|
| 新 session 启动 | 手动回顾 5-10 分钟 | 自动加载，即刻恢复 |
| 跨天任务 | "我们昨天做什么来着" | "继续昨天的 X 任务" |
| 多项目切换 | 混乱、遗忘 | 自动加载项目上下文 |
| Token 消耗 | 随机、不稳定 | 可控，~22k 预算 |

---

## 🤝 与 Jarvis Core 协作

本技能是 [Jarvis Core v2.0](../jarvis-core/) 的依赖项，在每次新会话的启动仪式中自动调用。

---

## 📝 Changelog

### v1.2.0
- 🐛 修复 L3 索引 token 膨胀 bug（-91%）
- ✅ slim index 格式：只存 `filename:lines`
- 📊 L3 预算从 1k 更新为 3k

### v1.1.0
- 增加 10 字摘要（已废弃，导致 token 膨胀）

### v1.0.0
- 初始版本，四层自动加载，手动深度回忆

---

**Made with 🧠 by [davidme6](https://github.com/davidme6)**
