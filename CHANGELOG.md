# Changelog

## 2026-10-14｜Job Insight Lab 展示版（v2.2.0）

### 本仓库的扩展与整理

- 以 Job Insight Lab｜岗位数据分析与报告工具为展示名称，维护仓库为 `gujiuji-1/job-insight-lab`；保留原作者 eatmoreduck、MIT 许可与上游来源说明。
- 完整 JD 增加结构化输出：职责、要求、工作安排、原始键值与章节；历史详情可由已有 `jd` 回填结构字段。
- 修复连续失败重试覆盖历史 JD 的问题，合并与重试保留有效正文；失败状态单独记录，登录失效或安全校验时停止并保存累计结果。
- `scripts/report_gen.py` 提供六类图表与统计 JSON；补充离线合成样例、统计和图表预览，区分预览快照与本地运行输出。
- `scripts/job_summary.py` 保留本地聚合摘要与提示词输出，文档以离线演示为入口，中英文说明同步。
- 项目版本保持 `2.2.0`，CLI `boss-scraper` / `boss-summary` 与运行时 `~/.boss-zhipin-scraper` 路径保持兼容。
- 清理无关推广与外部 Agent 下载说明，贡献指南改为本地验证与小范围改动流程。

测试使用本地 mock 与合成输入；真实浏览器采集可用性需在运行环境中另行验证。

## 上游基础

采集底座来自 [eatmoreduck/boss-zhipin-scraper](https://github.com/eatmoreduck/boss-zhipin-scraper)，原作者 eatmoreduck。Chrome CDP 连接、真实页面列表响应捕获、城市码表、基础 JSON/CSV 输出、专用浏览器 profile 和基础 CLI 均继承自该项目。

上游版本历史详见原仓库的 [CHANGELOG.md](https://github.com/eatmoreduck/boss-zhipin-scraper/blob/master/CHANGELOG.md)。上游历史测试记录不作为本展示版的当前验证结果。
