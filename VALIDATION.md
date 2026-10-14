# 本地验证记录

验证日期：2026-10-14。环境：Windows，CPython 3.13.2。

| 验证项 | 结果 | 范围 |
|---|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` | 105 项通过 | 固定样例、mock 和临时文件；包含连续两次失败时保留旧 JD 的回归测试 |
| `python scripts/report_gen.py --result-dir examples` | 运行成功 | 读取 6 条合成列表和 6 条合成详情，生成统计及六类 PNG 图表 |
| `python scripts/job_summary.py --input examples/boss_jobs_demo.json --details examples/boss_details_demo.json --top 10` | 运行成功 | 本地生成岗位摘要及可复制提示词 |
| 元数据与许可 | 检查通过 | 项目名与锁文件一致，版本保持 2.2.0，原始 MIT 许可证完整保留 |

Windows 沙箱默认临时目录曾导致文件操作权限错误。本次测试使用项目内的临时目录，
`TEMP`、`TMP` 指向 `.artifacts/test-tmp`，`MPLCONFIGDIR` 指向 `.artifacts/matplotlib`；
这些目录均被 Git 忽略，不属于发布文件。

图表和统计只来自仓库内的虚构示例，不构成真实招聘市场结论。
本次未验证真实 Chrome 登录、BOSS 页面采集和平台限制下的长期可用性。

## 来源记录

采集基础来自 MIT 许可项目 `eatmoreduck/boss-zhipin-scraper`。
发布副本基于本地维护版本 `1c134e4`，该版本在上游基础 `2bc40f5` 上增加了结构化 JD、
历史结果恢复和报告功能。本次发布进一步修复连续失败时的数据覆盖，整理文档并加入合成演示。
原本地仓库及其提交历史保留，公开展示仓库使用带有明确来源说明的代码快照。
