#!/usr/bin/env python3
"""
CNN-style Banner Generator
为图片添加 CNN 风格的新闻 banner

特性：
- 底部半透明深色 banner
- 左侧红色竖条装饰
- 主标题支持部分高亮（黄色）
- 副标题支持竖线分隔
- 可配置字体、颜色、间距等参数
- 支持 2.35:1 宽屏比例裁切
"""

from PIL import Image, ImageDraw, ImageFont
import os
import argparse


class BannerConfig:
    """Banner 配置"""
    # 图片比例
    aspect_ratio = 2.35
    
    # 字体大小
    title_font_size = 85
    subtitle_font_size = 30
    
    # 间距
    title_spacing = 6       # 主标题字间距
    subtitle_spacing = 3    # 副标题字间距
    title_sub_gap = 30      # 主副标题行间距（= 副标题字号）
    top_padding = 30        # banner 顶部内边距
    bottom_padding = 50     # banner 底部内边距
    bottom_margin = 100     # 底部留白
    
    # 颜色 (RGBA)
    banner_bg = (5, 10, 20, 128)        # 深色半透明背景 (50%不透明度)
    red_bar = (220, 30, 30, 255)        # 左侧红色条
    title_color = (255, 255, 255)       # 主标题白色
    highlight_color = (255, 210, 0)     # 高亮黄色
    subtitle_color = (255, 255, 255)    # 副标题白色
    
    # 红色条宽度
    red_bar_width = 12
    text_left_margin = 30   # 文字左侧边距（红色条右边）


def draw_text_with_spacing(draw, pos, text, font, fill, spacing=6):
    """绘制带字间距的文字"""
    x, y = pos
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        bbox = draw.textbbox((x, y), char, font=font)
        x = bbox[2] + spacing
    return x


def crop_to_ratio(img, target_ratio):
    """裁切图片到目标比例"""
    width, height = img.size
    current_ratio = width / height
    
    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        return img.crop((left, 0, left + new_width, height))
    else:
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        return img.crop((0, top, width, top + new_height))


def load_font(font_path, size, fallback_paths=None):
    """加载字体，支持 fallback"""
    if fallback_paths is None:
        fallback_paths = [
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        ]
    
    # 尝试主字体
    if font_path and os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except:
            pass
    
    # 尝试 fallback
    for path in fallback_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    
    # 最终 fallback
    return ImageFont.load_default()


def add_banner(
    input_path,
    output_path,
    title_parts,           # [("全球", "white"), ("17.8%", "highlight"), ("的人已在用AI", "white")]
    subtitle,              # "阿联酋70%领跑 | GitHub代码量暴涨78%"
    config=None,
    title_font_path=None,
    subtitle_font_path=None,
):
    """
    给图片添加 CNN 风格 banner
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        title_parts: 主标题列表，每项为 (文字, 颜色类型)，颜色类型: "white" 或 "highlight"
        subtitle: 副标题文字
        config: BannerConfig 配置对象
        title_font_path: 主标题字体路径
        subtitle_font_path: 副标题字体路径
    """
    if config is None:
        config = BannerConfig()
    
    # 打开并裁切图片
    img = Image.open(input_path).convert("RGBA")
    img = crop_to_ratio(img, config.aspect_ratio)
    width, height = img.size
    
    # 计算 banner 高度
    banner_height = (
        config.top_padding + 
        config.title_font_size + 
        config.title_sub_gap + 
        config.subtitle_font_size + 
        config.bottom_padding
    )
    
    banner_top = height - config.bottom_margin - banner_height
    banner_bottom = height - config.bottom_margin
    
    # 创建叠加层
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 绘制 banner 背景
    draw.rectangle([(0, banner_top), (width, banner_bottom)], fill=config.banner_bg)
    
    # 绘制红色条
    draw.rectangle(
        [(0, banner_top), (config.red_bar_width, banner_bottom)], 
        fill=config.red_bar
    )
    
    # 加载字体
    font_title = load_font(title_font_path, config.title_font_size)
    font_sub = load_font(subtitle_font_path, config.subtitle_font_size)
    
    # 合并背景
    img_with_overlay = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img_with_overlay)
    
    # 文字位置
    title_y = banner_top + config.top_padding
    sub_y = title_y + config.title_font_size + config.title_sub_gap
    
    # 绘制主标题
    x = config.red_bar_width + config.text_left_margin
    for text, color_type in title_parts:
        if color_type == "highlight":
            fill = config.highlight_color
        else:
            fill = config.title_color
        x = draw_text_with_spacing(draw, (x, title_y), text, font_title, fill, config.title_spacing)
    
    # 绘制副标题
    draw_text_with_spacing(
        draw, 
        (config.red_bar_width + config.text_left_margin, sub_y),
        subtitle, 
        font_sub, 
        config.subtitle_color, 
        config.subtitle_spacing
    )
    
    # 保存
    result = img_with_overlay.convert("RGB")
    result.save(output_path, quality=95)
    print(f"已保存: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="CNN-style Banner Generator")
    parser.add_argument("input", help="输入图片路径")
    parser.add_argument("-o", "--output", help="输出图片路径", default="output.png")
    parser.add_argument("-t", "--title", help="主标题（用|分隔高亮部分，如：全球|17.8%|的人已在用AI）", 
                        default="全球|17.8%|的人已在用AI")
    parser.add_argument("-s", "--subtitle", help="副标题", 
                        default="阿联酋70%领跑 | GitHub代码量暴涨78% | 南北差距拉大")
    parser.add_argument("--highlight", help="高亮部分索引（从0开始，逗号分隔）", default="1")
    parser.add_argument("--title-font", help="主标题字体路径")
    parser.add_argument("--subtitle-font", help="副标题字体路径")
    parser.add_argument("--opacity", help="Banner不透明度 (0-100)", type=int, default=50)
    
    args = parser.parse_args()
    
    # 解析标题
    title_texts = args.title.split("|")
    highlight_indices = set(int(i) for i in args.highlight.split(",") if i.strip())
    
    title_parts = []
    for i, text in enumerate(title_texts):
        color_type = "highlight" if i in highlight_indices else "white"
        title_parts.append((text, color_type))
    
    # 配置透明度
    config = BannerConfig()
    alpha = int(args.opacity * 255 / 100)
    config.banner_bg = (5, 10, 20, alpha)
    
    add_banner(
        args.input,
        args.output,
        title_parts,
        args.subtitle,
        config=config,
        title_font_path=args.title_font,
        subtitle_font_path=args.subtitle_font,
    )


if __name__ == "__main__":
    main()
