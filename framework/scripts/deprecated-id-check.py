#!/usr/bin/env python3
"""
废弃编号引用检测脚本
读取 ID-REGISTRY.md 中的"已废弃编号"表，在 GDD/TDD/PDD/CSV 中搜索废弃编号的引用。
"""
import os
import sys
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ID_REGISTRY_PATH = os.path.join(PROJECT_ROOT, "docs", "GDD", "ID-REGISTRY.md")

# 搜索范围
SEARCH_DIRS = [
    os.path.join(PROJECT_ROOT, "docs", "GDD"),
    os.path.join(PROJECT_ROOT, "docs", "TDD"),
    os.path.join(PROJECT_ROOT, "docs", "PDD"),
    os.path.join(PROJECT_ROOT, "data", "csv"),
]


def extract_deprecated_ids(filepath):
    """从ID-REGISTRY.md的已废弃编号表中提取编号列表"""
    if not os.path.exists(filepath):
        return set(), "文件不存在"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    deprecated_ids = set()

    # 解析已废弃编号表
    if "## 已废弃编号" in content:
        dep_section = content.split("## 已废弃编号")[1]
        # 截止到下一个 ## 或文件末尾
        dep_section = dep_section.split("\n## ")[0] if "\n## " in dep_section else dep_section

        for line in dep_section.split("\n"):
            line = line.strip()
            if not line or not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                id_candidate = parts[1]
                # 跳过表头和分隔行
                if id_candidate in ("编号", "---") or not id_candidate:
                    continue
                # 检查是否像个编号
                if re.match(r'^[A-Z]', id_candidate):
                    deprecated_ids.add(id_candidate)

    return deprecated_ids, None


def search_id_in_file(filepath, deprecated_ids):
    """搜索文件中引用的废弃编号"""
    if not os.path.exists(filepath):
        return []

    findings = []
    # 跳过元数据CSV文件
    basename = os.path.basename(filepath)
    if basename.startswith("_"):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                for did in deprecated_ids:
                    # 精确匹配：编号前后应该是非字母数字或边界
                    # 但不排除同一个文件作为废弃编号表本身的ID-REGISTRY
                    if did in line:
                        # 检查是否是真正的引用而不是被包含在其他编号中
                        # 例如 C-001 不应该匹配 C-0010
                        idx = line.find(did)
                        # 确认前后是边界
                        before_ok = idx == 0 or not line[idx - 1].isalnum() and line[idx - 1] != '-'
                        after_ok = idx + len(did) >= len(line) or not line[idx + len(did)].isdigit()
                        if before_ok and after_ok:
                            # 跳过ID-REGISTRY自身中的废弃编号表
                            if basename == "ID-REGISTRY.md":
                                continue
                            findings.append((did, line_no, line.strip()[:120]))
    except Exception as e:
        findings.append(("ERROR", 0, f"读取文件失败: {e}"))

    return findings


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    errors = []

    if not os.path.exists(ID_REGISTRY_PATH):
        print(f"## deprecated-id-check 校验报告")
        print(f"- 状态：❌ 1个错误")
        print(f"- 错误清单：")
        print(f"  {ID_REGISTRY_PATH}:0 ID-REGISTRY.md 文件不存在")
        sys.exit(1)

    deprecated_ids, err = extract_deprecated_ids(ID_REGISTRY_PATH)

    if err:
        print(f"## deprecated-id-check 校验报告")
        print(f"- 状态：❌ 1个错误")
        print(f"- 错误清单：")
        print(f"  {ID_REGISTRY_PATH}:0 {err}")
        sys.exit(1)

    if not deprecated_ids:
        print(f"## deprecated-id-check 校验报告")
        print(f"- 状态：✅通过")
        print(f"- 未找到任何已废弃编号")
        sys.exit(0)

    # 搜索所有目标目录
    all_findings = []
    for search_dir in SEARCH_DIRS:
        if not os.path.exists(search_dir):
            continue
        for root, dirs, files in os.walk(search_dir):
            for fname in files:
                if fname.endswith(".md") or fname.endswith(".csv"):
                    fpath = os.path.join(root, fname)
                    findings = search_id_in_file(fpath, deprecated_ids)
                    for did, line_no, text in findings:
                        all_findings.append((fpath, did, line_no, text))

    # 输出报告
    print(f"## deprecated-id-check 校验报告")
    if all_findings:
        print(f"- 状态：❌ {len(all_findings)}个引用")
        print(f"- 错误清单：")
        for fpath, did, line_no, text in all_findings:
            print(f"  {fpath}:{line_no} 引用了废弃编号 '{did}'：{text}")
    else:
        print(f"- 状态：✅通过")
        print(f"- 已废弃编号 {len(deprecated_ids)} 个：{', '.join(sorted(deprecated_ids))}")
        print(f"- 在 GDD/TDD/PDD/CSV 中未发现对废弃编号的引用")

    if all_findings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
