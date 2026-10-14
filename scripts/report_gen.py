# -*- coding: utf-8 -*-
"""报告数据准备：读取抓取结果，生成统计 JSON 与图表 PNG（供 docx 报告使用）。
输出目录: <repo>/report/
"""
import argparse
import json
import glob
import os
import re
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── matplotlib 中文字体 ──
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# ── dataviz 验证过的默认色板（light 模式 slot 1 蓝色 + 文本色）──
SERIES = "#2a78d6"
INK = "#0b0b0b"
INK_MUTED = "#52514e"
GRID = "#e5e5e0"
SURFACE = "#fcfcfb"

RESULT_DIR = os.path.expanduser("~/.boss-zhipin-scraper/job-result")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "report")
CHART_DIR = os.path.join(OUT_DIR, "charts")


def load_jobs(result_dir=RESULT_DIR):
    files = sorted(glob.glob(os.path.join(result_dir, "boss_jobs_*.json")))
    if not files:
        raise ValueError(f"未找到岗位输入文件: {result_dir}/boss_jobs_*.json")
    merged = [f for f in files if "merged" in f]
    path = merged[-1] if merged else files[-1]
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict) or not isinstance(raw.get("jobs"), list):
        raise ValueError(f"岗位输入文件必须包含 jobs 列表: {path}")
    jobs = raw.get("jobs", [])
    if not jobs:
        raise ValueError(f"岗位输入列表为空: {path}")
    return jobs, raw.get("keyword", ""), raw.get("city", ""), path


def load_details(result_dir=RESULT_DIR):
    files = sorted(glob.glob(os.path.join(result_dir, "boss_details_*.json")))
    if not files:
        return []
    with open(files[-1], encoding="utf-8") as f:
        raw = json.load(f)
    return raw if isinstance(raw, list) else raw.get("details") or []


def split_tags(raw):
    return [t.strip() for t in str(raw or "").split("|") if t.strip()]


def is_experience_tag(tag):
    return tag in {"经验不限", "1年以内", "1-3年", "3-5年", "5-10年", "10年以上"} or re.fullmatch(r"\d+-\d+年", tag) is not None


def is_degree_tag(tag):
    return any(k in tag for k in ("学历", "大专", "本科", "硕士", "博士", "中专", "中技", "高中"))


def district_from_location(location):
    parts = str(location or "").split("·")
    if len(parts) >= 2 and ("区" in parts[1] or "县" in parts[1] or "市" in parts[1]):
        return parts[1]
    return parts[0] if parts else "未知"


# JD 词频：停用词（复用 boss_cdp_raw.extract_tech_terms_from_jds + job_summary 噪声词）
STOP_WORDS = {
    "任职", "要求", "岗位", "职责", "描述", "优先", "具有", "负责", "相关",
    "经验", "能力", "以上", "及其", "工作", "开发", "团队", "项目", "公司",
    "业务", "熟悉", "熟练", "了解", "掌握", "参与", "完成", "进行", "能够",
    "学历", "专业", "提供", "福利", "加入", "我们", "我们只", "是通过",
    "就是", "已经", "可以", "这个", "那个", "什么", "怎么", "欢迎", "期待",
    "为你", "为你提供", "职位描述", "查看全部", "搜索", "更多职位", "人还看",
    "精选职位", "热门职位", "推荐公司", "公司介绍", "工作地址", "点击查看",
    "工商信息", "公司名称", "竞争力", "安全提示", "包括但不限于", "微信扫码",
    "良好", "优秀", "极好", "一般", "城市招聘", "热门企业", "搜索",
    "一金", "薪酬待遇", "工作职责", "工作时间", "绩效",
}


def jd_term_freq(details, top=15):
    freq = Counter()
    for d in details:
        text = str(d.get("jd") or "")
        if not text:
            continue
        for w in re.findall(r"\b[A-Za-z][A-Za-z0-9._-]+\b", text):
            if 2 <= len(w) <= 30 and w.lower() not in {"boss", "www", "http", "https", "com", "cn"}:
                freq[w] += 1
        for w in re.findall(r"[一-鿿]{2,6}", text):
            if w not in STOP_WORDS:
                freq[w] += 1
    return freq.most_common(top)


def barh_chart(name, labels, values, xlabel):
    """dataviz 规范：横向条形、单色 slot-1、thin marks、直接数值标签、recessive 网格。"""
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    y = range(len(labels))
    ax.barh(list(y), values, height=0.58, color=SERIES, zorder=3)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=10, color=INK)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel, fontsize=9.5, color=INK_MUTED)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", colors=INK_MUTED, labelsize=9)
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    # 直接数值标签（relief 规则：色板有 <3:1 对比的槽位，必须带标签）
    for xi, v in zip(y, values):
        ax.text(v + max(values) * 0.012, xi, str(v), va="center", fontsize=9.5, color=INK_MUTED)
    ax.set_xlim(0, max(values) * 1.12)
    fig.tight_layout(pad=0.6)
    fig.savefig(os.path.join(CHART_DIR, name), facecolor=SURFACE)
    plt.close(fig)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result-dir", default=RESULT_DIR, help="岗位列表及详情 JSON 所在目录")
    args = parser.parse_args(argv)
    jobs, keyword, city, jobs_path = load_jobs(args.result_dir)
    details = load_details(args.result_dir)
    os.makedirs(CHART_DIR, exist_ok=True)
    print(f"列表: {len(jobs)} 条 ({jobs_path})")
    print(f"详情: {len(details)} 条")

    salary = Counter()
    experience = Counter()
    degree = Counter()
    district = Counter()
    skills = Counter()
    for j in jobs:
        salary[str(j.get("salary") or "未知")] += 1
        for t in split_tags(j.get("job_labels") or j.get("tags")):
            if is_experience_tag(t):
                experience[t] += 1
            elif is_degree_tag(t):
                degree[t] += 1
        district[district_from_location(j.get("location"))] += 1
        for t in split_tags(j.get("skills")):
            skills[t] += 1

    jd_terms = jd_term_freq(details)
    companies = sorted({str(j.get("boss_name") or j.get("company") or "").strip() for j in jobs} - {""})

    stats = {
        "keyword": keyword,
        "city": city,
        "company": "、".join(companies) or "未提供",
        "jobs_total": len(jobs),
        "details_total": len(details),
        "salary": salary.most_common(12),
        "experience": experience.most_common(8),
        "degree": degree.most_common(8),
        "district": district.most_common(12),
        "skills": skills.most_common(15),
        "jd_terms": jd_terms,
    }
    with open(os.path.join(OUT_DIR, "stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)
    print("stats.json 已写入:", os.path.join(OUT_DIR, "stats.json"))

    # ── 图表（form: 类别分布 → 条形；均为单系列，slot-1 蓝色）──
    if stats["salary"]:
        barh_chart("salary.png", [k for k, v in stats["salary"]], [v for k, v in stats["salary"]], "岗位数")
    if stats["experience"]:
        barh_chart("experience.png", [k for k, v in stats["experience"]], [v for k, v in stats["experience"]], "岗位数")
    if stats["degree"]:
        barh_chart("degree.png", [k for k, v in stats["degree"]], [v for k, v in stats["degree"]], "岗位数")
    if stats["district"]:
        barh_chart("district.png", [k for k, v in stats["district"]], [v for k, v in stats["district"]], "岗位数")
    if stats["skills"]:
        barh_chart("skills.png", [k for k, v in stats["skills"]], [v for k, v in stats["skills"]], "岗位数")
    if stats["jd_terms"]:
        barh_chart("jd_terms.png", [k for k, v in stats["jd_terms"]], [v for k, v in stats["jd_terms"]], "出现次数")
    print("图表已生成:", sorted(os.listdir(CHART_DIR)))
    # 摘要打印
    for key in ("salary", "experience", "degree", "district", "skills", "jd_terms"):
        print(f"\n{key}:")
        for k, v in stats[key]:
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
