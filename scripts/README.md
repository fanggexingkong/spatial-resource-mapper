# scripts

本目录存放空间资源地图工具的可执行脚本。

## 当前脚本

| 脚本 | 说明 |
|---|---|
| `locate_unidentified_points.py` | 对未识别行政区的点位进行空间归属，输出带行政区、置信度、推断方法的结果表 |

## 使用方式

```
python scripts/locate_unidentified_points.py \
  --input data/unidentified_points.csv \
  --boundary data/admin_boundaries.geojson \
  --output output/located_points.csv \
  --city_field name
```

## 参数说明

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--input` | 输入文件路径，支持 CSV / Excel | 必填 |
| `--boundary` | 行政区划边界文件路径，支持 GeoJSON / Shapefile / GeoPackage | 必填 |
| `--output` | 输出文件路径 | `output/located_points.csv` |
| `--lon` | 经度字段名 | `经度` |
| `--lat` | 纬度字段名 | `纬度` |
| `--city_field` | 边界文件中的行政区名称字段 | `name` |
| `--crs` | 坐标系 | `EPSG:4326` |

## 注意事项

- 行政区划边界文件需要使用者自备，本仓库不内置具体省份边界数据。
- 点位坐标系应与边界文件保持一致，默认使用 EPSG:4326。
- 脚本不会自动合并相似名称的点位，也不会强行归属低置信数据。
- 输出结果中的"待核验"数据应进入人工复核流程。
