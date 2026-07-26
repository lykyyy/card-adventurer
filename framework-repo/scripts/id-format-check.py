#!/usr/bin/env python3
"""
ID格式校验脚本
读取 ID-REGISTRY.md，校验所有已注册编号是否符合格式规范：^[A-Z]+(-[0-9]+)+$
"""
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ID_REGISTRY_PATH = os.path.join(PROJECT_ROOT, "docs", "GDD", "ID-REGISTRY.md")

# 有效编号格式：大写字母开头，支持复合前缀（如 FEAT-G-, BG-FEAT-），最后一段必须是数字
# 如 C-001, FEAT-G-01, PROF-FEAT-001, BG-FEAT-001
ID_PATTERN = re.compile(r'^[A-Z]+(-[A-Z]+)*-[0-9]+$')

# 一些特殊格式也在ID-REGISTRY中出现，需要额外允许
# PL1-PL10 格式（PL后直接跟数字，无连字符）
SPECIAL_PL_PATTERN = re.compile(r'^PL[0-9]+$')


def is_valid_id_format(id_str):
    """校验单个ID格式是否合法"""
    if ID_PATTERN.match(id_str):
        return True
    if SPECIAL_PL_PATTERN.match(id_str):
        return True
    return False


def extract_ids_from_registry(filepath):
    """从ID-REGISTRY.md中提取所有已注册和已废弃的编号"""
    if not os.path.exists(filepath):
        return [], [], "ID-REGISTRY.md 文件不存在"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    in_deprecated_section = False
    registered_ids = set()
    deprecated_ids = set()

    # 匹配编号的模式：大写字母开头，可能包含连字符和数字
    id_regex = re.compile(r'\b([A-Z][A-Z-]*[-]?[0-9]+(?:[-][0-9]+)*)\b')

    # GDD-/TDD-/PDD- 是文档编号，不是游戏元素编号，需要排除
    DOC_PREFIXES = ("GDD-", "TDD-", "PDD-")

    for line in lines:
        # 检测已废弃编号段落
        if line.strip().startswith("## 已废弃编号"):
            in_deprecated_section = True
            continue
        if in_deprecated_section and line.strip().startswith("## "):
            in_deprecated_section = False
            continue

        # 提取该行的所有ID
        if in_deprecated_section:
            matches = id_regex.findall(line)
            for m in matches:
                if not m.startswith(DOC_PREFIXES):
                    deprecated_ids.add(m)
        else:
            # 只提取表格行中"✅已注册"的ID
            if "✅已注册" in line:
                matches = id_regex.findall(line)
                for m in matches:
                    if not m.startswith(DOC_PREFIXES):
                        registered_ids.add(m)

    return sorted(registered_ids), sorted(deprecated_ids), None


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    errors = []

    if not os.path.exists(ID_REGISTRY_PATH):
        print(f"## id-format-check 校验报告")
        print(f"- 状态：❌ 1个错误")
        print(f"- 错误清单：")
        print(f"  {ID_REGISTRY_PATH}:0 ID-REGISTRY.md 文件不存在")
        sys.exit(1)

    registered_ids, deprecated_ids, err = extract_ids_from_registry(ID_REGISTRY_PATH)

    if err:
        print(f"## id-format-check 校验报告")
        print(f"- 状态：❌ 1个错误")
        print(f"- 错误清单：")
        print(f"  {ID_REGISTRY_PATH}:0 {err}")
        sys.exit(1)

    # 校验已注册编号格式
    for rid in registered_ids:
        if not is_valid_id_format(rid):
            errors.append(f"{ID_REGISTRY_PATH}:0 已注册编号 '{rid}' 格式违规（不符合 ^[A-Z]+(-[0-9]+)+$ 规范）")

    # 也校验已废弃编号格式（如果它们被引用，格式也应该是合法的）
    for did in deprecated_ids:
        if not is_valid_id_format(did):
            errors.append(f"{ID_REGISTRY_PATH}:0 已废弃编号 '{did}' 格式违规（不符合 ^[A-Z]+(-[0-9]+)+$ 规范）")

    # 输出报告
    print(f"## id-format-check 校验报告")
    if errors:
        print(f"- 状态：❌ {len(errors)}个错误")
        print(f"- 错误清单：")
        for e in errors:
            print(f"  {e}")
    else:
        print(f"- 状态：✅通过")
        print(f"- 校验范围：已注册编号 {len(registered_ids)} 个，已废弃编号 {len(deprecated_ids)} 个")
        print(f"- 全部编号格式合规")

    if errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
