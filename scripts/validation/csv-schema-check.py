#!/usr/bin/env python3
"""
CSV-Schema一致性校验脚本
读取 _schema.csv，校验所有已注册CSV文件的列名、列数与定义一致。
注意：columns字段内部包含逗号，需要特殊处理。
"""
import os
import sys
import csv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA_PATH = os.path.join(PROJECT_ROOT, "data", "csv", "_schema.csv")
CSV_DIR = os.path.join(PROJECT_ROOT, "data", "csv")


def parse_columns_string(col_str):
    """解析columns字段，返回列名列表（去除type和constraint）"""
    if not col_str or not col_str.strip():
        return []
    parts = [p.strip() for p in col_str.split(",")]
    names = []
    for p in parts:
        # 格式: name:type:constraint 或 name:type
        name = p.split(":")[0].strip()
        if name:
            names.append(name)
    return names


def read_csv_headers(filepath):
    """读取CSV文件的列名（跳过#注释行）"""
    if not os.path.exists(filepath):
        return None, "文件不存在"

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # 找到了数据行（第一行非注释行是列名）
                reader = csv.reader([line])
                headers = next(reader)
                return [h.strip() for h in headers], None
        return None, "文件中无有效数据行"
    except Exception as e:
        return None, f"读取失败: {e}"


def parse_schema_csv(filepath):
    """
    解析 _schema.csv，处理 columns 字段内逗号的问题。
    前6个字段是固定字段(file_name,system,gdd_section,version,status,dependency)，
    第7个起全部合并为 columns 字段。
    """
    if not os.path.exists(filepath):
        return [], "文件不存在"

    schema_defs = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # 手动按逗号分割
                raw_parts = line.split(",")

                # 跳过标题行
                if raw_parts[0].strip() == "file_name":
                    continue

                if len(raw_parts) < 7:
                    continue

                file_name = raw_parts[0].strip()
                # 前6个是固定字段，第7个起都是columns内容
                columns_str = ",".join(raw_parts[6:])
                expected_cols = parse_columns_string(columns_str)

                schema_defs.append({
                    "file_name": file_name,
                    "columns": expected_cols
                })
    except Exception as e:
        return [], f"解析失败: {e}"

    return schema_defs, None


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    errors = []

    if not os.path.exists(SCHEMA_PATH):
        print(f"## csv-schema-check 校验报告")
        print(f"- 状态：❌ 1个错误")
        print(f"- 错误清单：")
        print(f"  {SCHEMA_PATH}:0 _schema.csv 文件不存在")
        sys.exit(1)

    schema_defs, err = parse_schema_csv(SCHEMA_PATH)
    if err:
        print(f"## csv-schema-check 校验报告")
        print(f"- 状态：❌ 1个错误")
        print(f"- 错误清单：")
        print(f"  {SCHEMA_PATH}:0 {err}")
        sys.exit(1)

    if not schema_defs:
        print(f"## csv-schema-check 校验报告")
        print(f"- 状态：✅通过")
        print(f"- 未找到任何已注册的CSV文件定义")
        sys.exit(0)

    total_files = 0
    ok_files = 0

    for sdef in schema_defs:
        file_name = sdef["file_name"]
        expected_cols = sdef["columns"]
        file_path = os.path.join(CSV_DIR, file_name)
        total_files += 1

        actual_cols, err = read_csv_headers(file_path)
        if err:
            errors.append(f"{file_path}:0 无法读取CSV文件: {err}")
            continue

        if actual_cols is None:
            errors.append(f"{file_path}:0 无法解析列名")
            continue

        # 比较列名
        expected_set = set(expected_cols)
        actual_set = set(actual_cols)

        # 检查 _schema 定义但CSV缺失的列
        missing_in_csv = expected_set - actual_set
        for col in sorted(missing_in_csv):
            errors.append(f"{file_path}:0 _schema.csv 定义了列 '{col}'，但CSV文件中未找到")

        # 检查 CSV 中存在但 _schema 未定义的列
        extra_in_csv = actual_set - expected_set
        for col in sorted(extra_in_csv):
            errors.append(f"{file_path}:0 CSV文件包含列 '{col}'，但 _schema.csv 中未定义")

        # 检查列数
        if len(expected_cols) != len(actual_cols):
            errors.append(
                f"{file_path}:0 列数不匹配：_schema定义 {len(expected_cols)} 列，CSV实际 {len(actual_cols)} 列"
            )

        if not missing_in_csv and not extra_in_csv and len(expected_cols) == len(actual_cols):
            ok_files += 1

    # 输出报告
    print(f"## csv-schema-check 校验报告")
    if errors:
        print(f"- 状态：❌ {len(errors)}个错误")
        print(f"- 错误清单：")
        for e in errors:
            print(f"  {e}")
        print(f"- 统计：{ok_files}/{total_files} 个CSV文件通过校验")
    else:
        print(f"- 状态：✅通过")
        print(f"- 统计：{total_files}/{total_files} 个CSV文件全部通过校验")

    if errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
