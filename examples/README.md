# 合成数据演示

此目录中的 6 条职位记录、公司名称、薪资、岗位职责和任职要求均为虚构内容。
它们用于展示数据格式、聚合分析和报告流程，不代表真实招聘信息或市场统计。
`example.invalid` 链接是不可用的占位地址，演示不需要打开网页、登录或访问外部服务。

- `boss_jobs_demo.json`：列表数据，包含 `data_source: synthetic` 标识。
- `boss_details_demo.json`：同一批虚构岗位的详情数据。
- `report_stats.json`：使用上述数据生成的统计预览。
- `charts/`：同一批数据生成的六类 PNG 图表。

在项目根目录运行：

```bash
python -m pip install -r requirements-report.txt
python scripts/report_gen.py --result-dir examples
```

新生成的统计和图表写入被 Git 忽略的 `report/` 目录；这里提交的预览不会被覆盖。
