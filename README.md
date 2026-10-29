# spatial-resource-mapper

一个通用的空间资源地图与资料库开发 Skill，用于多源资源点位数据的清洗、坐标精修、
空间归属、分类统计、多格式导出和方法论沉淀。

## 功能

- 多源点位数据汇聚与清洗
- 坐标精修与坐标系转换
- 未识别行政区点位空间归属
- 分类统计与行政区分布统计
- GeoJSON / CSV / Excel 导出
- 数据质量校验与一致性检查
- 可迁移的数据整合方法论沉淀

## 适用场景

- 省级/市级/区县级资源地图建设
- 文保单位、非遗、博物馆、公园、景区、文化场馆等资源整理
- 资料库入库前数据治理
- 跨省份、跨领域数据整合方法复用
- 资源地图项目标准化口径建设

## 目录结构

```
spatial-resource-mapper/
├── SKILL.md
├── README.md
├── LICENSE
├── .gitignore
├── scripts/
│   └── locate_unidentified_points.py
├── references/
│   ├── methodology.md
│   ├── shandong-case-study.md
│   ├── classification-example.md
│   └── cleaning-rules.md
└── assets/
    └── .gitkeep
```

## 使用方法

将 `spatial-resource-mapper` 文件夹放入你的 Agent Skills 目录后，即可在支持 Agent Skills
的环境中调用。

典型触发词包括：

- 资源地图
- 点位清洗
- 坐标精修
- 地市/区县归属
- 未识别数据定位
- GeoJSON/CSV 导出
- 数据整合方法论
- 跨省份数据迁移

## 脚本说明

`scripts/locate_unidentified_points.py` 用于对未识别行政区的点位做空间归属。

示例：

```
python scripts/locate_unidentified_points.py \
  --input data/unidentified_points.csv \
  --boundary data/admin_boundaries.geojson \
  --output output/located_points.csv \
  --city_field name
```

注意：行政区划边界文件需要使用者自备，本仓库不内置具体省份边界数据。

## 参考案例

`references/shandong-case-study.md` 提供了山东文化资源地图项目的案例，包括点位口径、
资源分类、地市分布、清洗规则和一致性校验结果。该案例仅作为方法验证示例，迁移到其他省份
或其他领域时，需要替换区域范围、分类体系、边界数据和字段口径。

## 许可证

MIT
