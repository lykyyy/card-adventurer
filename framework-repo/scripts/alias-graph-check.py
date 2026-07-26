#!/usr/bin/env python3
"""
ID-ALIAS和ID-REFERENCE-GRAPH完整性校验脚本
- 检查 ID-ALIAS.md 中每个废弃编号是否都有替代编号映射
- 检查 ID-REFERENCE-GRAPH.md 中每个前缀是否在 ID-REGISTRY.md 中存在
"""
import os
import sys
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ALIAS_PATH = os.path.join(PROJECT_ROOT, "docs", "GDD", "ID-ALIAS.md")
REF_GRAPH_PATH = os.path.join(PROJECT_ROOT, "docs", "GDD", "ID-REFERENCE-GRAPH.md")
ID_REGISTRY_PATH = os.path.join(PROJECT_ROOT, "docs", "GDD", "ID-REGISTRY.md")


def extract_prefixes_from_registry(filepath):
    """从ID-REGISTRY.md的编号格式规范表提取所有已注册的前缀"""
    if not os.path.exists(filepath):
        return set(), "文件不存在"

    prefixes = set()
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 方法：匹配编号格式规范表中的行：| PREFIX- | 含义 | 格式 | 示例 | 源文件 |
    # 表中每行以 "| " 开头，第一列是前缀（包含连字符）
    in_prefix_table = False
    for line in content.split("\n"):
        stripped = line.strip()

        # 检测表格头部
        if stripped.startswith("| 前缀 |") and "含义" in stripped:
            in_prefix_table = True
            continue

        if in_prefix_table:
            # 表格结束条件：空行或不以 | 开头
            if not stripped or not stripped.startswith("|"):
                in_prefix_table = False
                continue

            parts = [p.strip() for p in stripped.split("|")]
            # parts[0] 是空字符串（行首|），parts[1]是前缀
            if len(parts) >= 2 and parts[1]:
                prefix = parts[1]
                # 跳过表头和分隔行
                if prefix in ("前缀", "---"):
                    continue
                if prefix.startswith("---"):
                    continue
                # 跳过空内容和纯符号
                if prefix and not prefix.startswith("---") and re.match(r'^[A-Z]', prefix):
                    prefixes.add(prefix)

    return prefixes, None


def extract_alias_mappings(filepath):
    """从ID-ALIAS.md提取别名映射"""
    if not os.path.exists(filepath):
        return [], "文件不存在"

    mappings = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析别名表
    in_alias_table = False
    for line in content.split("\n"):
        line = line.strip()
        if "| 别名 | 指向编号 |" in line:
            in_alias_table = True
            continue
        if in_alias_table and line.startswith("---"):
            continue
        if in_alias_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3 and parts[1] and parts[1] not in ("别名", "---"):
                alias = parts[1]
                target = parts[2] if len(parts) >= 3 else ""
                mappings.append((alias, target))
        elif in_alias_table and not line.startswith("|"):
            in_alias_table = False

    return mappings, None


def extract_graph_prefixes(filepath):
    """从ID-REFERENCE-GRAPH.md提取所有前缀"""
    if not os.path.exists(filepath):
        return set(), "文件不存在"

    prefixes = set()
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 方法1：从跨系统引用清单表提取
    # | 编号前缀 | 定义系统 | 被引用系统 | 引用方式 |
    in_cross_ref_table = False
    for line in content.split("\n"):
        stripped = line.strip()

        if stripped.startswith("| 编号前缀 |") and "定义系统" in stripped:
            in_cross_ref_table = True
            continue

        if in_cross_ref_table:
            if not stripped.startswith("|"):
                in_cross_ref_table = False
                continue
            parts = [p.strip() for p in stripped.split("|")]
            if len(parts) >= 2 and parts[1]:
                p = parts[1]
                if p in ("编号前缀", "---"):
                    continue
                if p.startswith("---"):
                    continue
                if p and re.match(r'^[A-Z]', p):
                    prefixes.add(p)

    # 方法2：从系统依赖图中提取（├── 职业 (P-)）
    prefix_pattern = re.compile(r'\(([A-Z][A-Za-z]*-)\)')
    for match in prefix_pattern.finditer(content):
        p = match.group(1)
        prefixes.add(p)

    # 方法3：从各前缀文件引用明细标题提取
    # ### C- (卡牌)
    section_prefix = re.compile(r'^### ([A-Z][A-Za-z]*-) ')
    for line in content.split("\n"):
        m = section_prefix.match(line.strip())
        if m:
            prefixes.add(m.group(1))

    return prefixes, None


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    errors = []

    # === 检查 ID-ALIAS.md ===
    alias_exists = os.path.exists(ALIAS_PATH)
    mappings = []
    if alias_exists:
        mappings, err = extract_alias_mappings(ALIAS_PATH)
        if err:
            errors.append(f"{ALIAS_PATH}:0 解析ID-ALIAS.md失败: {err}")
        else:
            # 检查每个废弃编号是否都有替代编号映射
            empty_targets = [(alias, target) for alias, target in mappings if not target or target == "—"]
            for alias, target in empty_targets:
                errors.append(f"{ALIAS_PATH}:0 别名 '{alias}' 缺少替代编号映射（指向空）")
    else:
        errors.append(f"{ALIAS_PATH}:0 ID-ALIAS.md 文件不存在")

    # === 检查 ID-REFERENCE-GRAPH.md ===
    graph_exists = os.path.exists(REF_GRAPH_PATH)
    graph_prefixes = set()
    if graph_exists:
        graph_prefixes, err = extract_graph_prefixes(REF_GRAPH_PATH)
        if err:
            errors.append(f"{REF_GRAPH_PATH}:0 解析ID-REFERENCE-GRAPH.md失败: {err}")
        else:
            # 获取ID-REGISTRY中注册的前缀
            registry_prefixes, reg_err = extract_prefixes_from_registry(ID_REGISTRY_PATH)
            if reg_err:
                errors.append(f"{ID_REGISTRY_PATH}:0 解析ID-REGISTRY.md失败: {reg_err}")
            else:
                # 检查graph中的前缀是否在registry中存在
                missing_in_registry = graph_prefixes - registry_prefixes
                for p in sorted(missing_in_registry):
                    errors.append(
                        f"{REF_GRAPH_PATH}:0 ID-REFERENCE-GRAPH中定义了前缀 '{p}'，"
                        f"但ID-REGISTRY中未注册该前缀"
                    )
    else:
        errors.append(f"{REF_GRAPH_PATH}:0 ID-REFERENCE-GRAPH.md 文件不存在")

    # 输出报告
    print(f"## alias-graph-check 校验报告")
    if errors:
        print(f"- 状态：❌ {len(errors)}个问题")
        print(f"- 问题清单：")
        for e in errors:
            print(f"  {e}")
    else:
        alias_count = len(mappings) if alias_exists else 0
        graph_count = len(graph_prefixes) if graph_exists else 0
        print(f"- 状态：✅通过")
        print(f"- ID-ALIAS.md：{alias_count} 条别名映射，全部有替代编号")
        print(f"- ID-REFERENCE-GRAPH.md：{graph_count} 个前缀，全部在ID-REGISTRY中存在")

    if errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
