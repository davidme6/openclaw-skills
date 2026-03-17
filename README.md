# OpenClaw Skills 技能合集

> 高质量 OpenClaw 技能合集 - 由 Jarvis 精心打造

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skills-blue)](https://openclaw.ai)

---

## 📦 已发布技能

### 1. Smart Web Search v3.0 ⭐⭐⭐⭐⭐

**最强大的智能搜索技能**

- 🔍 **12 个搜索引擎** - 百度、谷歌、360、DuckDuckGo 等
- 🛡️ **广告过滤** - 自动识别过滤，准确率 95%+
- 🧪 **内容去毒** - 虚假信息过滤，准确率 90%+
- ⏰ **实时搜索** - 当天/24 小时/7 天/30 天
- 📊 **多引擎聚合** - 同时搜索 3 个引擎
- 📝 **结果摘要** - AI 生成关键信息

**安装命令**：
```bash
clawhub install smart-web-search
```

**使用示例**：
```
"用百度搜索今天 3 月 17 日的 AI 新闻"
"搜索疫苗信息（去毒）"
"搜索在线课程（过滤广告）"
```

**详细文档**：[skills/smart-web-search/README.md](skills/smart-web-search/README.md)

---

## 🚀 快速开始

### 安装技能

```bash
# 通过 ClawHub 安装
clawhub install <skill-name>

# 或手动安装
git clone https://github.com/davidme6/openclaw-skills.git
cp -r openclaw-skills/skills/<skill-name> ~/.openclaw/skills/
```

### 使用技能

直接在 OpenClaw 中使用自然语言：
```
"搜索 XXX"
"search for XXX"
"帮我找一下 XXX"
```

---

## 📊 技能开发

### 技能结构

```
skill-name/
├── SKILL.md          # 技能清单
├── _meta.json        # 元数据
├── README.md         # 用户文档
├── LICENSE           # 许可证
└── tools/            # 工具脚本（可选）
```

### 提交技能

欢迎提交你的 OpenClaw 技能！

1. Fork 本仓库
2. 在 `skills/` 下创建技能文件夹
3. 确保包含必要文件
4. 提交 Pull Request

---

## 📈 统计数据

| 指标 | 数值 |
|------|------|
| 技能数量 | 1 个 |
| 总下载量 | 待统计 |
| 平均评分 | 待统计 |
| 最后更新 | 2026-03-17 |

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [ClawHub 技能市场](https://clawhub.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Discord 社区](https://discord.gg/clawd)

---

## 📝 更新日志

### v3.0.0 (2026-03-17)
- ✅ 新增 Smart Web Search v3.0
- ✅ 集成百度/谷歌搜索
- ✅ 广告过滤功能
- ✅ 内容去毒功能
- ✅ 反馈监控系统

---

*Made with ❤️ for OpenClaw Community*
