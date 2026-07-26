#!/usr/bin/env python3
"""
外键完整性校验脚本
读取 _foreign_keys.csv，验证所有外键引用的完整性：
- source_file 和 target_file 是否存在
- source_column 和 target_column 是否在对应文件中存在
- 引用的值是否实际存在于目标文件中
"""
import os
import sys
import csv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FK_PATH = os.path.join(PROJECT_ROOT, "data", "csv", "_foreign_keys.csv")
CSV_DIR = os.path.join(PROJECT_ROOT, "data", "csv")


def read_csv_headers(filepath):
    """读取CSV的列名"""
    if not os.path.exists(filepath):
        return None, "文件不存在"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                reader = csv.reader([line])
                return [h.strip() for h in next(reader)], None
        return None, "文件中无有效数据行"
    except Exception as e:
        return None, f"读取失败: {e}"


def read_csv_data_rows(filepath):
    """读取CSV的所有数据行（跳过注释和表头）"""
    if not os.path.exists(filepath):
        return None, [], "文件不存在"
    try:
        rows = []
        headers = None
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                reader = csv.reader([line])
                cells = next(reader)
                if headers is None:
                    headers = [c.strip() for c in cells]
                    continue
                rows.append([c.strip() for c in cells])
        return headers, rows, None
    except Exception as e:
        return None, [], f"读取失败: {e}"


def get_column_values(headers, rows, column_name):
    """获取指定列的所有值"""
    if headers is None:
        return set()
    try:
        col_idx = headers.index(column_name)
    except ValueError:
        return set()
    return {row[col_idx] for row in rows if col_idx < len(row)}


def parse_foreign_keys(filepath):
    """解析 _foreign_keys.csv"""
    if not os.path.exists(filepath):
        return [], "文件不存在"
    try:
        fk_list = []
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = None
            for row in reader:
                if not row or row[0].startswith("#"):
                    continue
                if headers is None:
                    headers = [h.strip() for h in row]
                    continue
                if len(row) >= 6:
                    fk_list.append({
                        "source_file": row[0].strip(),
                        "source_column": row[1].strip(),
                        "target_file": row[2].strip(),
                        "target_column": row[3].strip(),
                        "on_delete": row[4].strip(),
                        "on_update": row[5].strip(),
                    })
        return fk_list, None
    except Exception as e:
        return [], f"解析失败: {e}"


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    errors = []

    if not os.path.exists(FK_PATH):
        print(f"## foreign-key-check 校验报告")
        print(f"- 状态：❌ 1个错误")
        print(f"- 错误清单：")
        print(f"  {FK_PATH}:0 _foreign_keys.csv 文件不存在")
        sys.exit(1)

    fk_list, err = parse_foreign_keys(FK_PATH)
    if err:
        print(f"## foreign-key-check 校验报告")
        print(f"- 状态：❌ 1个错误")
        print(f"- 错误清单：")
        print(f"  {FK_PATH}:0 {err}")
        sys.exit(1)

    if not fk_list:
        print(f"## foreign-key-check 校验报告")
        print(f"- 状态：✅通过")
        print(f"- 未找到任何外键引用定义")
        sys.exit(0)

    # 缓存已读取的CSV文件，避免重复读取
    file_cache = {}

    for fk in fk_list:
        src_path = os.path.join(CSV_DIR, fk["source_file"])
        tgt_path = os.path.join(CSV_DIR, fk["target_file"])

        # 检查源文件存在性
        if not os.path.exists(src_path):
            errors.append(f"{FK_PATH}:0 外键引用 source_file='{fk['source_file']}' 文件不存在 ({src_path})")
            continue

        # 检查目标文件存在性
        if not os.path.exists(tgt_path):
            errors.append(f"{FK_PATH}:0 外键引用 target_file='{fk['target_file']}' 文件不存在 ({tgt_path})")
            continue

        # 读取源文件列名
        if src_path not in file_cache:
            src_headers, _ = read_csv_headers(src_path)
            file_cache[src_path] = src_headers
        else:
            src_headers = file_cache[src_path]

        if src_headers is None:
            errors.append(f"{src_path}:0 无法解析源文件列名")
            continue

        # 检查源列是否存在
        if fk["source_column"] not in src_headers:
            errors.append(
                f"{src_path}:0 源文件 '{fk['source_file']}' 中不存在列 '{fk['source_column']}'"
            )

        # 读取目标文件
        if tgt_path not in file_cache:
            tgt_headers, tgt_rows, _ = read_csv_data_rows(tgt_path)
            file_cache[tgt_path] = (tgt_headers, tgt_rows)
        else:
            tgt_headers, tgt_rows = file_cache[tgt_path]

        if tgt_headers is None:
            errors.append(f"{tgt_path}:0 无法解析目标文件")
            continue

        # 检查目标列是否存在
        if fk["target_column"] not in tgt_headers:
            errors.append(
                f"{tgt_path}:0 目标文件 '{fk['target_file']}' 中不存在列 '{fk['target_column']}'"
            )
            continue

        # 检查引用值完整性：源文件的列值必须在目标文件的列值中
        if src_path not in file_cache or not isinstance(file_cache.get(src_path), tuple):
            src_full_headers, src_rows, _ = read_csv_data_rows(src_path)
            file_cache[src_path] = (src_full_headers, src_rows)
        else:
            src_full_headers, src_rows = file_cache[src_path]

        target_values = get_column_values(tgt_headers, tgt_rows, fk["target_column"])
        source_values = get_column_values(src_full_headers, src_rows, fk["source_column"])

        orphan_values = source_values - target_values - {""}
        for ov in sorted(orphan_values):
            errors.append(
                f"{src_path}:0 外键 '{fk['source_file']}.{fk['source_column']}' 的值 '{ov}' "
                f"在 '{fk['target_file']}.{fk['target_column']}' 中不存在"
            )

    # 输出报告
    print(f"## foreign-key-check 校验报告")
    if errors:
        print(f"- 状态：❌ {len(errors)}个错误")
        print(f"- 错误清单：")
        for e in errors:
            print(f"  {e}")
    else:
        print(f"- 状态：✅通过")
        print(f"- 校验了 {len(fk_list)} 条外键引用，全部完整")

    if errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
