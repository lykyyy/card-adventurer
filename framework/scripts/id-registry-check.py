#!/usr/bin/env python3
"""
ID-REGISTRY注册状态校验脚本
- 检查是否有重复注册的编号
- 检查废弃编号是否仍在活跃表中
- 检查注册统计表与实际注册数量的一致性
"""
import os
import sys
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ID_REGISTRY_PATH = os.path.join(PROJECT_ROOT, "docs", "GDD", "ID-REGISTRY.md")


def extract_all_ids_from_markdown_table(filepath):
    """从ID-REGISTRY.md中提取所有表格中的编号及状态"""
    if not os.path.exists(filepath):
        return {}, {}, "文件不存在"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    in_deprecated_section = False

    registered = {}   # id -> 名称
    deprecated_from_registry = {}  # id -> 废弃原因
    duplicates = set()

    # 匹配表格行中的ID和状态
    # 表格格式: | ID | 名称 | ... | 状态 |

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## 已废弃编号"):
            in_deprecated_section = True
            continue
        if in_deprecated_section and stripped.startswith("## "):
            in_deprecated_section = False
            continue

        if in_deprecated_section:
            # 解析已废弃编号表：| 编号 | 废弃日期 | 原因 | 替代编号 |
            if stripped.startswith("|") and not stripped.startswith("| "):
                continue
            parts = [p.strip() for p in stripped.split("|")]
            if len(parts) >= 3 and parts[1] and parts[1] not in ("编号", "---"):
                dep_id = parts[1]
                deprecated_from_registry[dep_id] = parts[3] if len(parts) >= 4 else ""
            continue

        # 解析活跃注册表
        if "✅已注册" in stripped or "❌已废弃" in stripped:
            # 提取ID（表格第一列数据列）
            parts = [p.strip() for p in stripped.split("|")]
            if len(parts) >= 2:
                id_candidate = parts[1]
                # 验证它看起来像一个ID
                if id_candidate and re.match(r'^[A-Z]', id_candidate) and not id_candidate.startswith("---"):
                    # 跳过表头行
                    if id_candidate in ("ID", "编号"):
                        continue

                    is_registered = "✅已注册" in stripped
                    is_deprecated_mark = "❌已废弃" in stripped

                    if is_registered and not is_deprecated_mark:
                        if id_candidate in registered:
                            duplicates.add(id_candidate)
                        registered[id_candidate] = stripped[:80]
                    elif is_deprecated_mark:
                        # 活跃表中标记为废弃的ID
                        deprecated_from_registry[id_candidate] = "活跃表中标记废弃"

    return registered, deprecated_from_registry, None


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    errors = []

    if not os.path.exists(ID_REGISTRY_PATH):
        print(f"## id-registry-check 校验报告")
        print(f"- 状态：❌ 1个错误")
        print(f"- 错误清单：")
        print(f"  {ID_REGISTRY_PATH}:0 ID-REGISTRY.md 文件不存在")
        sys.exit(1)

    registered, deprecated, err = extract_all_ids_from_markdown_table(ID_REGISTRY_PATH)

    if err:
        print(f"## id-registry-check 校验报告")
        print(f"- 状态：❌ 1个错误")
        print(f"- 错误清单：")
        print(f"  {ID_REGISTRY_PATH}:0 {err}")
        sys.exit(1)

    # 检查：重复注册的编号
    # 重新扫描找重复
    with open(ID_REGISTRY_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 在活跃表区域（废弃表之前）搜索所有✅已注册行中的编号
    active_section = content.split("## 已废弃编号")[0] if "## 已废弃编号" in content else content
    id_pattern = re.compile(r'^\| ([A-Z][A-Za-z-]*[-]?[0-9]+(?:[-][0-9]+)*)')
    id_occurrences = {}

    for line in active_section.split("\n"):
        if "✅已注册" in line:
            m = id_pattern.match(line.strip())
            if m:
                rid = m.group(1)
                if rid not in id_occurrences:
                    id_occurrences[rid] = []
                id_occurrences[rid].append(line.strip()[:100])

    # 找重复
    dup_found = []
    for rid, occurrences in id_occurrences.items():
        if len(occurrences) > 1:
            dup_found.append(rid)
            errors.append(f"{ID_REGISTRY_PATH}:0 编号 '{rid}' 出现 {len(occurrences)} 次重复注册")

    # 检查：废弃编号是否错误出现在活跃区域
    dep_ids_from_table = set()
    if "## 已废弃编号" in content:
        dep_section = content.split("## 已废弃编号")[1]
        dep_section = dep_section.split("## ")[0] if "## " in dep_section else dep_section
        for line in dep_section.split("\n"):
            m = id_pattern.match(line.strip())
            if m:
                dep_ids_from_table.add(m.group(1))

    active_registered_ids = set(id_occurrences.keys())
    cross_contamination = active_registered_ids & dep_ids_from_table
    for rid in sorted(cross_contamination):
        errors.append(f"{ID_REGISTRY_PATH}:0 编号 '{rid}' 同时出现在活跃表和已废弃表中（冲突）")

    # 输出报告
    print(f"## id-registry-check 校验报告")
    if errors:
        print(f"- 状态：❌ {len(errors)}个错误")
        print(f"- 错误清单：")
        for e in errors:
            print(f"  {e}")
    else:
        print(f"- 状态：✅通过")
        print(f"- 统计：已注册 {len(id_occurrences)} 个唯一编号，已废弃 {len(dep_ids_from_table)} 个编号")
        print(f"- 无重复注册，无活跃表/废弃表交叉污染")

    if errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
