---
name: job-insight-lab
description: "研究公开职位与岗位描述，通过本地 JSON 生成岗位摘要、结构化 JD 和六类统计图表；可在明确授权后使用 Chrome CDP 采集。"
version: 2.2.0
author: eatmoreduck
maintainer: gujiuji-1
license: MIT
metadata:
  hermes:
    tags: [jobs, career, cdp, chrome, zhipin, reporting]
---

# Job Insight Lab｜岗位数据分析与报告工具 v2.2.0

基于 [eatmoreduck/boss-zhipin-scraper](https://github.com/eatmoreduck/boss-zhipin-scraper) 扩展；原作者和 MIT 许可保留。维护仓库：[gujiuji-1/job-insight-lab](https://github.com/gujiuji-1/job-insight-lab)。

## 脚本与依赖

先确定仓库或 Skill 安装目录，再使用其中脚本的实际路径。不要假定当前目录包含脚本。

- `scripts/boss_cdp_raw.py`：Chrome CDP 采集、完整 JD 与结构字段、历史详情恢复。
- `scripts/job_summary.py`：读取本地 JSON，输出聚合摘要与可复制提示词。
- `scripts/report_gen.py`：读取本地 JSON，输出统计与六类图表。

Python 3.10+。仅做文字摘要无需浏览器；图表依赖在 `requirements-report.txt`，采集依赖在 `requirements.txt`。需要安装时在项目虚拟环境中使用 `python -m pip install -r requirements-report.txt` 或 `python -m pip install -r requirements.txt`，遵守用户对安装和联网的授权范围。

## 离线分析流程

用户要求分析已有数据时，优先使用明确指定的文件；没有文件时可使用仓库合成示例演示。

```bash
python scripts/job_summary.py --input examples/boss_jobs_demo.json --details examples/boss_details_demo.json --top 10
python scripts/report_gen.py --result-dir examples
```

`job_summary.py` 只生成文本，不调用模型。报告输出到 `report/stats.json` 与 `report/charts/`；`examples/report_stats.json` 和 `examples/charts/` 是合成样例的预览快照。

报告包括薪资、经验、学历、地区、技能、JD 高频词。说明每项统计的样本范围，避免把小样本描述为整体市场。JD 高频词是文本出现次数，不是具备该技能的人数。

## 采集流程

只有用户明确要求采集时才访问 BOSS直聘。需本人有权访问的账号、Chrome 和采集依赖；登录由用户在专用浏览器中手动完成。

```bash
python scripts/boss_cdp_raw.py --setup-chrome
python scripts/boss_cdp_raw.py --keyword "Python" --city 上海 --pages 1 --max-details 5 --analysis
python scripts/boss_cdp_raw.py --stop-chrome
```

`--setup-chrome` 创建或复用 `~/.boss-zhipin-scraper/chrome-profile`，默认不复制主 Chrome 登录状态。列表通过 CDP `Network` 捕获真实搜索页面自身产生的 API 响应；详情只读取职位描述区域。不要向接口注入额外请求，不绕过验证码或安全校验。

遇到登录失效或安全校验时，保存累计结果并停止；告知用户在专用 Chrome 中完成登录或验证。不要无限重试，也不要用不可信的 DOM 薪资替代缺失的 API 薪资。

`--copy-login-state` 会复制 Cookie 相关文件，仅在用户明确要求导入时使用；`--reset-chrome-profile` 会清除专用浏览器登录状态，使用前须得到相应授权。`--stop-chrome` 按专用 profile 匹配进程，不关闭主 Chrome。

## 数据与兼容

详情保留完整 `jd`、`job_responsibilities`、`job_requirements`、工作安排、`work_info`、`detail_sections` 和 `detail_schema_version`。加载旧结果可从已有 JD 回填结构字段；合并和失败重试保留有效历史 JD。

默认结果目录仍为 `~/.boss-zhipin-scraper/job-result`。安装后的 CLI 仍为 `boss-scraper` 和 `boss-summary`；详见 `--help`。

对外展示使用合成数据，不公开 Cookie、Token、浏览器 profile、招聘者个人信息或未经处理的真实结果。该工具用于岗位研究与聚合分析，不替用户投递、登录或联系招聘者。
