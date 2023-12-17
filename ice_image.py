"""
    此代码用来批量生成僵尸被冰冻后的图像
"""


from PIL import Image, ImageEnhance


def apply_blue_filter(input_path, output_path, intensity=1.8):
    # 打开图像文件
    image = Image.open(input_path)

    # 将图像转换为带有 Alpha 通道的 RGBA 模式
    image = image.convert("RGBA")

    # 将图像拆分为红、绿、蓝和透明四个通道
    r, g, b, a = image.split()

    # 创建一个全蓝色通道的图像
    blue_channel = Image.new("L", image.size, 255)

    # 合并图像，将蓝色通道加强，保留透明度
    blue_image = Image.merge("RGBA", (r, g, blue_channel, a))

    # 使用图像增强来增加蓝色的强度
    enhancer = ImageEnhance.Brightness(blue_image)
    blue_image = enhancer.enhance(intensity)

    # 保存输出图像
    blue_image.save(output_path)


for i in range(10):
    input_image_path = f"./images/football_eat_{str(i)}.png"
    output_image_path = f"./images/ice_football_eat_{str(i)}.png"
    apply_blue_filter(input_image_path, output_image_path)
# 输入图像路径


# 输出图像路径


# 应用蓝色滤镜
