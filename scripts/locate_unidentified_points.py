"""
未识别点位空间归属脚本

功能：
- 读取未识别行政区的点位数据
- 校验坐标有效性
- 使用行政区划边界做空间归属
- 输出带行政区、置信度、推断方法的清洗轨迹表

注意：
- 行政区划边界文件需要使用者自备
- 坐标系应与边界文件保持一致，默认使用 EPSG:4326
- 本脚本不内置任何省份边界数据
"""

import argparse
import sys
from datetime import datetime

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


def parse_args():
    parser = argparse.ArgumentParser(
        description="未识别点位空间归属脚本"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="输入文件路径，CSV 或 Excel",
    )
    parser.add_argument(
        "--boundary",
        required=True,
        help="行政区划边界文件路径，GeoJSON / Shapefile / GeoPackage",
    )
    parser.add_argument(
        "--output",
        default="output/located_points.csv",
        help="输出文件路径，默认 output/located_points.csv",
    )
    parser.add_argument(
        "--lon",
        default="经度",
        help="经度字段名，默认 经度",
    )
    parser.add_argument(
        "--lat",
        default="纬度",
        help="纬度字段名，默认 纬度",
    )
    parser.add_argument(
        "--city_field",
        default="name",
        help="边界文件中行政区名称字段，默认 name",
    )
    parser.add_argument(
        "--crs",
        default="EPSG:4326",
        help="坐标系，默认 EPSG:4326",
    )
    return parser.parse_args()


def is_valid_coordinate(lat, lon):
    """判断坐标是否有效"""
    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        return False

    if lat == 0 and lon == 0:
        return False

    if not (-90 <= lat <= 90):
        return False

    if not (-180 <= lon <= 180):
        return False

    return True


def load_points(path, lon_field, lat_field):
    """读取点位数据"""
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path)
    elif path.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(path)
    else:
        raise ValueError("输入文件仅支持 CSV / Excel")

    required = [lon_field, lat_field]
    missing = [f for f in required if f not in df.columns]
    if missing:
        raise ValueError(f"缺少字段：{missing}")

    df["坐标有效"] = df.apply(
        lambda r: is_valid_coordinate(r.get(lat_field), r.get(lon_field)),
        axis=1,
    )

    def build_point(row):
        if row["坐标有效"]:
            return Point(float(row[lon_field]), float(row[lat_field]))
        return None

    df["geometry"] = df.apply(build_point, axis=1)

    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    return gdf


def load_boundary(path, city_field, crs):
    """读取行政区划边界"""
    boundary = gpd.read_file(path)

    if boundary.crs is None:
        boundary.set_crs(crs, inplace=True)
    else:
        boundary = boundary.to_crs(crs)

    if city_field not in boundary.columns:
        raise ValueError(
            f"边界文件中缺少行政区名称字段：{city_field}，"
            f"当前可用字段：{list(boundary.columns)}"
        )

    return boundary


def locate_points(points_gdf, boundary_gdf, city_field):
    """空间归属"""
    with_coord = points_gdf[points_gdf["geometry"].notna()].copy()
    without_coord = points_gdf[points_gdf["geometry"].isna()].copy()

    if not with_coord.empty:
        located = gpd.sjoin(
            with_coord,
            boundary_gdf[[city_field, "geometry"]],
            how="left",
            predicate="within",
        )
        located["推断行政区"] = located.get(city_field, "")
        located["推断方法"] = "坐标空间归属"
        located["置信度"] = "高"
    else:
        located = with_coord.copy()
        located["推断行政区"] = ""
        located["推断方法"] = "无有效坐标"
        located["置信度"] = "待核验"

    if not without_coord.empty:
        without_coord["推断行政区"] = ""
        without_coord["推断方法"] = "待地理编码或人工核验"
        without_coord["置信度"] = "待核验"

    result = pd.concat([located, without_coord], ignore_index=True)
    return result


def main():
    args = parse_args()

    try:
        points_gdf = load_points(args.input, args.lon, args.lat)
        boundary_gdf = load_boundary(args.boundary, args.city_field, args.crs)
        result = locate_points(points_gdf, boundary_gdf, args.city_field)

        result["处理时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result["是否人工复核"] = result["置信度"].isin(
            ["待核验", "低"]
        )

        result.to_csv(args.output, index=False, encoding="utf-8-sig")

        total = len(result)
        located_count = (result["推断方法"] == "坐标空间归属").sum()
        pending_count = total - located_count

        print(f"处理完成，共 {total} 条点位")
        print(f"通过坐标空间归属：{located_count} 条")
        print(f"待后续处理：{pending_count} 条")
        print(f"结果已保存至：{args.output}")

    except Exception as e:
        print(f"执行失败：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
