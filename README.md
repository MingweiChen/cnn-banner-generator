# CNN Banner Generator

为图片添加 CNN 风格的新闻 banner。

## 特性

- 🎨 底部半透明深色 banner（可调透明度）
- 🔴 左侧红色竖条装饰
- ✨ 主标题支持部分高亮（黄色）
- 📝 副标题支持竖线分隔
- ⚙️ 可配置字体、颜色、间距等参数
- 📐 支持 2.35:1 宽屏比例裁切

## 安装

```bash
pip install Pillow
```

## 使用方法

### 命令行

```bash
# 基础用法
python banner_generator.py input.png -o output.png

# 自定义标题（用|分隔，第2段会高亮）
python banner_generator.py input.png -o output.png \
  -t "全球|17.8%|的人已在用AI" \
  -s "阿联酋70%领跑 | GitHub代码量暴涨78%"

# 指定高亮部分（索引从0开始）
python banner_generator.py input.png -o output.png \
  -t "今日|头条|新闻" \
  --highlight "1"

# 调整透明度（0-100，默认50）
python banner_generator.py input.png -o output.png --opacity 70

# 使用自定义字体
python banner_generator.py input.png -o output.png \
  --title-font fonts/SourceHanSansSC-Bold.otf \
  --subtitle-font fonts/SourceHanSansSC-Regular.otf
```

### Python API

```python
from banner_generator import add_banner, BannerConfig

# 基础用法
add_banner(
    "input.png",
    "output.png",
    title_parts=[
        ("全球", "white"),
        ("17.8%", "highlight"),
        ("的人已在用AI", "white"),
    ],
    subtitle="阿联酋70%领跑 | GitHub代码量暴涨78%",
)

# 自定义配置
config = BannerConfig()
config.title_font_size = 90
config.bottom_margin = 120
config.banner_bg = (5, 10, 20, 180)     # 调整透明度
config.highlight_color = (255, 180, 0)  # 更深的黄色

add_banner(
    "input.png",
    "output.png",
    title_parts=[("突发", "highlight"), ("新闻", "white")],
    subtitle="重要消息 | 实时更新",
    config=config,
)
```

## 配置项

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `aspect_ratio` | 2.35 | 图片宽高比 |
| `title_font_size` | 85 | 主标题字号 |
| `subtitle_font_size` | 30 | 副标题字号 |
| `title_spacing` | 6 | 主标题字间距 |
| `subtitle_spacing` | 3 | 副标题字间距 |
| `title_sub_gap` | 30 | 主副标题间距 |
| `top_padding` | 30 | banner 顶部内边距 |
| `bottom_padding` | 50 | banner 底部内边距 |
| `bottom_margin` | 100 | 底部留白 |
| `red_bar_width` | 12 | 红色条宽度 |
| `banner_bg` | (5,10,20,128) | Banner背景色 RGBA (50%不透明度) |

## 推荐字体

- 思源黑体 (Source Han Sans)
- 阿里巴巴普惠体
- 文泉驿正黑

## License

MIT
