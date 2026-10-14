import importlib.util
import io
import json
import pathlib
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "report_gen.py"


def load_module():
    spec = importlib.util.spec_from_file_location("report_gen", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReportGenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_import_does_not_create_report_directory(self):
        with mock.patch("os.makedirs") as makedirs:
            load_module()
        makedirs.assert_not_called()

    def test_missing_or_empty_jobs_have_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            result_dir = pathlib.Path(tmp)
            with self.assertRaisesRegex(ValueError, "未找到岗位输入文件"):
                self.module.load_jobs(result_dir)
            path = result_dir / "boss_jobs_demo.json"
            path.write_text(json.dumps({"jobs": []}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "岗位输入列表为空"):
                self.module.load_jobs(result_dir)

    def test_load_jobs_prefers_merged_and_details_stay_in_input_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            result_dir = pathlib.Path(tmp)
            payload = {"keyword": "merged", "city": "示例城市", "jobs": [{"job_id": "demo"}]}
            for name, keyword in (("boss_jobs_merged.json", "merged"), ("boss_jobs_z.json", "later")):
                (result_dir / name).write_text(json.dumps({**payload, "keyword": keyword}), encoding="utf-8")
            jobs, keyword, city, path = self.module.load_jobs(result_dir)
            self.assertEqual(jobs, payload["jobs"])
            self.assertEqual(keyword, "merged")
            self.assertEqual(city, "示例城市")
            self.assertEqual(pathlib.Path(path).name, "boss_jobs_merged.json")
            self.assertEqual(self.module.load_details(result_dir), [])
            details = [{"job_id": "demo", "jd": "Python SQL"}]
            (result_dir / "boss_details_demo.json").write_text(json.dumps({"details": details}), encoding="utf-8")
            self.assertEqual(self.module.load_details(result_dir), details)

    def test_report_uses_input_companies_and_generates_six_distributions(self):
        module = self.module
        with tempfile.TemporaryDirectory() as tmp:
            result_dir = pathlib.Path(tmp) / "input"
            out_dir = pathlib.Path(tmp) / "report"
            chart_dir = out_dir / "charts"
            result_dir.mkdir()
            jobs = [
                {"boss_name": "示例公司甲", "salary": "10-20K", "job_labels": "1-3年 | 本科",
                 "location": "示例城市·示例区", "skills": "Python | SQL"},
                {"company": "示例公司乙", "salary": "10-20K", "tags": "1-3年 | 本科",
                 "location": "示例城市·示例区", "skills": "Python"},
            ]
            (result_dir / "boss_jobs_demo.json").write_text(
                json.dumps({"keyword": "Python", "city": "示例城市", "jobs": jobs}), encoding="utf-8"
            )
            (result_dir / "boss_details_demo.json").write_text(
                json.dumps([{"jd": "Python Python SQL"}]), encoding="utf-8"
            )

            def write_chart(name, labels, values, xlabel):
                self.assertEqual(len(labels), len(values))
                self.assertTrue(values)
                (chart_dir / name).touch()

            with mock.patch.object(module, "OUT_DIR", str(out_dir)), \
                    mock.patch.object(module, "CHART_DIR", str(chart_dir)), \
                    mock.patch.object(module, "barh_chart", side_effect=write_chart) as chart, \
                    mock.patch.object(module.glob, "glob", wraps=module.glob.glob) as search, \
                    redirect_stdout(io.StringIO()):
                module.main(["--result-dir", str(result_dir)])

            stats = json.loads((out_dir / "stats.json").read_text(encoding="utf-8"))
            self.assertEqual(stats["company"], "示例公司乙、示例公司甲")
            self.assertEqual(stats["keyword"], "Python")
            self.assertEqual(stats["city"], "示例城市")
            self.assertEqual(stats["jobs_total"], 2)
            self.assertEqual(stats["details_total"], 1)
            expected = {
                "salary": [["10-20K", 2]], "experience": [["1-3年", 2]],
                "degree": [["本科", 2]], "district": [["示例区", 2]],
                "skills": [["Python", 2], ["SQL", 1]], "jd_terms": [["Python", 2], ["SQL", 1]],
            }
            for key, values in expected.items():
                self.assertEqual(stats[key], values)
            self.assertEqual(chart.call_count, 6)
            self.assertEqual({path.name for path in chart_dir.iterdir()}, {f"{key}.png" for key in expected})
            self.assertEqual(search.call_count, 2)
            for call in search.call_args_list:
                self.assertEqual(pathlib.Path(call.args[0]).parent, result_dir)


if __name__ == "__main__":
    unittest.main()
