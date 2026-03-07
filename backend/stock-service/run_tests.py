import os
import datetime
import subprocess

def run_tests():
    """运行测试并生成HTML报告"""
    # 创建报告目录
    report_dir = "test_reports"
    os.makedirs(report_dir, exist_ok=True)
    
    # 生成报告文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"test_report_{timestamp}.html")
    coverage_dir = os.path.join(report_dir, f"coverage_{timestamp}")
    
    # 构建命令
    cmd = [
        "poetry", "run", "pytest",
        "--html", report_file,
        "--self-contained-html",
        "--cov=app",
        f"--cov-report=html:{coverage_dir}",
        "-v"
    ]
    
    # 运行测试
    subprocess.run(cmd)
    
    print(f"\n测试报告已生成: {report_file}")
    print(f"覆盖率报告已生成: {coverage_dir}")

if __name__ == "__main__":
    run_tests()