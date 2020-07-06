
import os
import zipfile
import pylab as pl
import numpy as np
import wave
# from App.models import ImgUrl, ProjectImg
# from common.util import EXECUTOR

#音频波形
from App.models import Img


def keep_wave(audio_url,audio_name,audio):
    # 打开WAV文档
    f = wave.open(rf'{audio_url}', "rb")
    # 读取格式信息

    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    print(nchannels,sampwidth,framerate,nframes)
    # 读取波形数据
    str_data = f.readframes(nframes)
    f.close()
    # 将波形数据转换为数组
    wave_data = np.fromstring(str_data, dtype=np.short)

    # wave_data.shape = -1, 2
    # wave_data = wave_data.T

    time = np.arange(0, nframes) * (1.0 / framerate)
    # 绘制波形
    pl.plot(time, wave_data, 'black', linewidth=0.1)
    pl.axis('off')
    print(wave_data,len(wave_data))
    print(time,len(time))
    print(audio_url)
    print(audio_name)
    pl.savefig(f'static/img/{audio_name}.jpg')
    pl.close()

    img=Img(img_url=f'/static/img/{audio_name}.jpg')
    img.name=audio_name
    print(audio)

    img.audio=audio
    print(111111111111)
    img.save()

    print(22222222)
    return img.img_url

# def upload_img(pro,img_files,pro_name,attr_dict,pro_time):
#     pro.save()
#     for img in img_files:
#         # 这种思路是仅仅保存了文件到服务器，需要单独保存文件路径到数据库
#         file = open(os.path.join(f'static/pro/{pro_name}_{pro_time}/', img.name), 'wb')
#         for chunk in img.chunks():
#             # 保存文件路径
#             image = ImgUrl(img_url=f'/static/pro/{pro_name}_{pro_time}/' + img.name)
#             image.img_name=img.name
#             try:
#                 image.save()
#             except BaseException as error:
#                 print(error)
#             pj = ProjectImg()
#             pj.project = pro
#             pj.img = image
#             pj.save()
#             # 保存文件到 img 下
#             file.write(chunk)
#         file.close()
#
#     with open(os.path.join(f'static/pro/{pro_name}_{pro_time}', 'options.txt'), 'w', encoding='UTF-8') as steam:
#         steam.write(f'{attr_dict}')
#
#
# from functools import wraps, partial
#
# #线程池
# # def run_in_thread_pool(*,callbacks=(), callbacks_kwargs=()):
# #     """将函数放入线程池执行的装饰器"""
# #
# #     def decorator(func):
# #
# #         @wraps(func)
# #         def wrapper(*args, **kwargs):
# #             future = EXECUTOR.submit(func, *args, **kwargs)
# #             for index, callback in enumerate(callbacks):
# #                 try:
# #                     kwargs = callbacks_kwargs[index]
# #                 except IndexError:
# #                     kwargs = None
# #                 fn = partial(callback, **kwargs) if kwargs else callback
# #                 future.add_done_callback(fn)
# #             return future
# #         return wrapper
# #
# #     return decorator
# def run_in_thread_pool(func):
#     """将函数放入线程池执行的装饰器"""
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         future=EXECUTOR.submit(func, *args, **kwargs)
#         # for index, callback in enumerate(callbacks):
#         #     try:
#         #         kwargs = callbacks_kwargs[index]
#         #     except IndexError:
#         #         kwargs = None
#         #     fn = partial(callback, **kwargs) if kwargs else callback
#         #     future.add_done_callback(fn)
#         # return func(*args,**kwargs)
#         return future.result()
#     return wrapper
#
#
# #文件压缩
# def zip_pro(zip_url, dir1, dir2):
#     file_news = zip_url + '.zip'  # 压缩后文件夹的名字
#     z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
#
#     for dirpath, dirnames, filenames in os.walk(dir1):
#
#         fpath = dirpath.replace(dir1, '')  # 这一句很重要，不replace的话，就从根目录开始复制
#         fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
#         for filename in filenames:
#             if filename.endswith('.txt'):
#                 pass
#             else:
#                 z.write(os.path.join(dirpath, filename), fpath + filename)
#
#     for dirpath, dirnames, filenames in os.walk(dir2):
#         fpath = dirpath.replace(dir2, '')  # 这一句很重要，不replace的话，就从根目录开始复制
#         fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
#         for filename in filenames:
#             z.write(os.path.join(dirpath, filename), fpath + filename)
#     z.close()
#
#
# # startdir = '../template'
# # dir1 = '../static/pro/1w2w2w2w2w2'
# # dir2 = '../static/pro/1w2w2w2w2w2_txt'
# # zip_ya(startdir, dir1, dir2)