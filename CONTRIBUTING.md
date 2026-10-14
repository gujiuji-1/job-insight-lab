# 贡献指南

Job Insight Lab 基于 [eatmoreduck/boss-zhipin-scraper](https://github.com/eatmoreduck/boss-zhipin-scraper) 扩展，维护仓库为 [gujiuji-1/job-insight-lab](https://github.com/gujiuji-1/job-insight-lab)。修改时保留原项目的 MIT 版权与许可。

## 本地环境与验证

要求 Python 3.10+。在虚拟环境中安装依赖：

```bash
git clone https://github.com/gujiuji-1/job-insight-lab.git
cd job-insight-lab
python -m pip install -r requirements-report.txt
python -m unittest discover -s tests -p "test_*.py"
python scripts/report_gen.py --result-dir examples
```

单元测试使用本地 mock；报告命令读取合成样例，输出到被 Git 忽略的 `report/`，不访问招聘平台。浏览器相关改动还需要另行验证真实 Chrome/CDP 行为，不能仅凭 mock 测试通过宣称采集可用。

## 修改约定

- 每次修改围绕一个具体问题，沿用现有结构和依赖；不要为小功能新增大型依赖。
- JD 解析或合并逻辑改动须覆盖历史字段、失败结果和已有有效 JD 的保留行为；报告改动须使用合成样例验证计数与图表。
- 只捕获需要处理的具体异常，避免隐藏错误或覆盖有效历史数据。
- 用户可见行为变化时同步中英文 README；版本变化时同步脚本、`pyproject.toml`、`SKILL.md` 与 README。
- 提交说明应包括问题、改动和实际验证结果；真实采集与离线测试分别说明。

提交前检查 `git diff` 和 `git status`。示例只用虚构数据，不提交 Cookie、Token、登录 profile、个人信息或真实采集文件。采集逻辑应遵守平台规则，不加入验证码绕过、代理轮换或无限重试机制。

## 讨论与提交

可先用本地分支完成小范围修改，再向维护仓库提交 Pull Request。需要讨论的设计可在 [Issues](https://github.com/gujiuji-1/job-insight-lab/issues) 中说明；普通修复不要求先开 Issue。
