# Job Insight Lab — Job Data Analysis & Reporting v2.2.0

[中文文档](README.md) · Python 3.10+ · MIT

Built on [eatmoreduck/boss-zhipin-scraper](https://github.com/eatmoreduck/boss-zhipin-scraper), this repository presents extensions for structured job descriptions, historical data recovery, and offline reporting, supporting job research and an engineering portfolio.

Turn job listings and complete descriptions into comparable fields, then generate six chart categories: salary, experience, education, location, skills, and frequent JD terms. Synthetic data and report snapshots are included for browsing and local reproduction without signing in to a recruitment platform.

## View the demo

All demo jobs and companies are fictional. The examples contain no real recruiter information or login data.

- [Job listings](examples/boss_jobs_demo.json) and [structured JDs](examples/boss_details_demo.json)
- [Statistics snapshot](examples/report_stats.json)
- [Chart snapshots](examples/charts)

![Skill distribution from synthetic jobs](examples/charts/skills.png)

## Extensions in this repository

| Engineering problem | Implementation and result | Source |
|---|---|---|
| Long descriptions are hard to compare | Keep the complete `jd`; extract responsibilities, requirements, and work arrangements; preserve additional fields and sections in `work_info` and `detail_sections` | [boss_cdp_raw.py](scripts/boss_cdp_raw.py) |
| Old results lack newly added fields | Backfill structured fields from existing JD text when loading historical JSON, without revisiting detail pages | [boss_cdp_raw.py](scripts/boss_cdp_raw.py) |
| Failed retries can replace useful results | Merge details by job identity, retain valid JDs, record failure status, and save accumulated results before stopping on login expiry or security checks | [boss_cdp_raw.py](scripts/boss_cdp_raw.py) |
| Raw JSON is difficult to present | Produce six aggregate chart categories and statistics JSON, with synthetic offline examples | [report_gen.py](scripts/report_gen.py) |

The Chrome CDP connection, list-response capture, city mapping, and basic CLI come from the original project. This repository extends detail-data handling and report presentation on that foundation.

## Reproduce the offline report

A Python virtual environment is recommended. Create it with `python -m venv .venv`; activate it with `.venv\Scripts\Activate.ps1` on Windows or `source .venv/bin/activate` on macOS/Linux.

```bash
git clone https://github.com/gujiuji-1/job-insight-lab.git
cd job-insight-lab
python -m pip install -r requirements-report.txt
python scripts/report_gen.py --result-dir examples
```

The command reads the synthetic JSON in `examples/` and writes new results to `report/stats.json` and `report/charts/`. The files in `examples/` are committed preview snapshots; `report/` is the local output directory and is excluded from Git.

Counts describe the input sample only: salaries are grouped by their original labels, skills are counted from job tags, and JD terms are counted by text occurrence. These examples do not represent the recruitment market as a whole.

Generate a text summary and a copyable job-research prompt:

```bash
python scripts/job_summary.py --input examples/boss_jobs_demo.json --details examples/boss_details_demo.json --top 10
```

`job_summary.py` reads local JSON and produces text. It does not call a model API.

## Optional: collect through your own browser

Collection requires Chrome, Python 3.10+, and a BOSS Zhipin account you are authorized to use. These commands connect to a browser and access the recruitment platform; review the options and platform rules before running them.

```bash
python -m pip install -r requirements.txt
python scripts/boss_cdp_raw.py --setup-chrome
python scripts/boss_cdp_raw.py --keyword "Python" --city 上海 --pages 1 --max-details 5 --analysis
python scripts/boss_cdp_raw.py --stop-chrome
```

On the first run, sign in manually in the dedicated Chrome window. The persistent profile is `~/.boss-zhipin-scraper/chrome-profile`; login data from the main Chrome profile is not copied automatically. CDP `Network` captures API responses produced by the real search page. Detail extraction reads the job-description area and removes login notices, recruiter cards, and recommendations from the JD.

| Common option | Purpose |
|---|---|
| `--keyword` / `--city` | Keyword and city name or code; defaults to AI Agent / Shanghai |
| `--pages` / `--max-details` | Bound list pages and detail count; at most 10 pages |
| `--no-detail` | Collect listings only |
| `--format csv` | Export listing and detail CSV alongside JSON |
| `--output` / `--detail-output` | Set listing and detail output files |
| `--merge FILE` | Merge an existing list and deduplicate by job identity |
| `--input FILE --analysis --no-detail` | Analyze an existing list and its associated details |
| `--list-cities [keyword]` | Display city codes |
| `--check` | Check dependencies, CDP, and login state; accesses the platform |
| `--stop-chrome` | Close the collection browser matched by its dedicated profile |

See `python scripts/boss_cdp_raw.py --help` for all options. `--copy-login-state` copies Cookie-related files from the main Chrome profile into the dedicated profile and should be used only when explicitly needed. `--reset-chrome-profile` clears the dedicated browser's login state.

For compatibility, installed commands remain `boss-scraper` and `boss-summary`, the default result directory remains `~/.boss-zhipin-scraper/job-result`, and the version remains `2.2.0`.

## Verification and limitations

Tests use standard-library `unittest` and local mocks to cover JD parsing, historical backfill, merge preservation, failure states, and text summaries:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Offline examples demonstrate reproducible data processing. Real Chrome login, page changes, and platform restrictions require validation in the user's environment; ongoing collection availability is not guaranteed. Use only data you may access and follow the platform's rules. Keep Cookies, Tokens, browser profiles, and unprocessed personal information out of public repositories.

## Repository layout

```text
job-insight-lab/
├── examples/                  # Synthetic JSON, statistics, and chart snapshots
├── scripts/
│   ├── boss_cdp_raw.py        # CDP collection and JD processing
│   ├── job_summary.py         # Text summary and prompt generation
│   └── report_gen.py          # Statistics and charts
├── tests/                     # Local mock and offline tests
├── data/city_codes.json       # City mapping
├── requirements.txt           # Collection dependencies
├── requirements-report.txt    # Offline report dependencies
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SKILL.md
└── LICENSE
```

## Origin and license

Original project: [eatmoreduck/boss-zhipin-scraper](https://github.com/eatmoreduck/boss-zhipin-scraper). Original author: **eatmoreduck**. Its collection foundation and basic tools are used under the MIT license, with the original copyright notice preserved in [LICENSE](LICENSE).

[gujiuji-1](https://github.com/gujiuji-1) maintains this repository as a portfolio of engineering extensions to an open-source project. The structured JD, historical recovery, and report changes can be reviewed in the linked source and tests; upstream capabilities and local extensions are described separately.
