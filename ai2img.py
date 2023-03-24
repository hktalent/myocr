from PIL import Image
import paddlehub as hub
module = hub.Module(name='disco_diffusion_ernievil_base')


"""
hub install disco_diffusion_cnclip_vitb16==1.0.0


def generate_image(
          text_prompts,
          style: Optional[str] = None,
          artist: Optional[str] = None,
          width_height: Optional[List[int]] = [1280, 768],
          seed: Optional[int] = None,
          output_dir: Optional[str] = 'disco_diffusion_ernievil_base_out'):
文图生成API，生成文本描述内容的图像。

参数

text_prompts(str): 输入的语句，描述想要生成的图像的内容。通常比较有效的构造方式为 "一段描述性的文字内容" + "指定艺术家的名字"，如"孤舟蓑笠翁，独钓寒江雪。风格如齐白石所作"。
style(Optional[str]): 指定绘画的风格，如水墨画、油画、水彩画等。当不指定时，风格完全由您所填写的prompt决定。
artist(Optional[str]): 指定特定的艺术家，如齐白石、Greg Rutkowsk，将会生成所指定艺术家的绘画风格。当不指定时，风格完全由您所填写的prompt决定。各种艺术家的风格可以参考网站。
width_height(Optional[List[int]]): 指定最终输出图像的宽高，宽和高都需要是64的倍数，生成的图像越大，所需要的计算时间越长。
seed(Optional[int]): 随机种子，由于输入默认是随机高斯噪声，设置不同的随机种子会由不同的初始输入，从而最终生成不同的结果，可以设置该参数来获得不同的输出图像。
output_dir(Optional[str]): 保存输出图像的目录，默认为"disco_diffusion_ernievil_base_out"。
返回

ra(DocumentArray): DocumentArray对象， 包含n_batches个Documents，其中每个Document都保存了迭代过程的所有中间结果。详细可参考DocumentArray使用文档。
"""

result = module.generate_image(text_prompts="greg rutkowski和thomas kinkade在artstation上的一幅美丽的画，一个独特的灯塔，照耀着它的光穿过喧嚣的血海。", output_dir='独特灯塔')

# display(Image.fromarray(result[0].load_uri_to_image_tensor().tensor))


result[0].chunks.save_gif('孤舟蓑笠翁.gif')