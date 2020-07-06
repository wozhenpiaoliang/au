import json
import os
import time
# import wave
# import numpy as np
# import scipy.signal as signal
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
import paramiko
# from django.views.decorators.clickjacking import xframe_options_exempt

from App.models import Audio

from App.tool import keep_wave

from shudu_ai.settings import BASE_DIR


# 首页
def index(request):
    new_time = int(time.time())
    timeout = Audio.objects.filter(Q(state=0, read=1, time__lt=new_time - 60)).only('state', 'read', 'time').all()
    if timeout:
        for i in timeout:
            i.time = 0
            i.read = 0
            i.save()
    audios = Audio.objects.all().only('id')

    data = {
        'code': 200000,
        'msg': '获取所有标注的音频文件',
        'audios': audios
    }
    return render(request, 'index.html', context=data)


# 拿音频数据
def take_wav(request):
    t = paramiko.Transport(('192.168.101.39', 22))
    t.connect(username='running', password='3155665400.')
    sftp = paramiko.SFTPClient.from_transport(t)
    head_folder = sftp.listdir(r"/home/running/文档/")
    if not os.path.exists('static/wav'):
        os.mkdir('static/wav')

    try:
        tail_folder =os.listdir('static/wav')[0]
        xuni_tail_folder=sftp.listdir(rf"/home/running/文档/{tail_folder}/")
        for i in xuni_tail_folder:
            if i not in os.listdir(tail_folder):
                sftp.get(rf"/home/running/文档/{tail_folder}/{i}", rf'static/wav/{tail_folder}/{i}')
                audio = Audio(audio_url=f'static/wav/{tail_folder}/{i}')
                audio.name = i
                audio.save()
    except BaseException as err:
        print(err)

    finally:
        for folder in head_folder:
            if folder not in os.listdir('static/wav'):
                os.mkdir(f'static/wav/{folder}')
                files=sftp.listdir(rf"/home/running/文档/{folder}/")
                for file in files:
                    sftp.get(rf"/home/running/文档/{folder}/{file}", rf'static/wav/{folder}/{file}')
                    audio = Audio(audio_url=f'static/wav/{folder}/{file}')
                    audio.name = file
                    audio.save()

        return JsonResponse({
                'code': 200100,
                'msg': '数据拿取成功'
            })

# def take_wav(request):
#     addr_wav = os.path.join(BASE_DIR, 'audio/file')
#     print(os.listdir('static/wav'))
#     for i in os.listdir(fr'{addr_wav}'):
#         if i not in os.listdir('static/wav'):
#             # 打开wav文件 ，open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据。
#             f = wave.open(os.path.join(addr_wav, i), "rb")
#             # 读取格式信息
#             # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采
#             # 样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
#             params = f.getparams()
#             nchannels, sampwidth, framerate, nframes = params[:4]
#             # 读取波形数据
#             # 读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）,二进制数据
#             str_data = f.readframes(nframes)
#             f.close()
#             # print(str_data)
#             # 转成可读数据
#             # wave_data = np.fromstring(str_data, dtype=np.short)
#             # time = 10
#             # f = wave.open(os.path.join(BASE_DIR,f'static/wav/{i}'), "wb")
#             f = wave.open(f'static/wav/{i}', "wb")
#             f.setnchannels(nchannels)
#             f.setsampwidth(sampwidth)
#             f.setframerate(framerate)
#             f.writeframes(str_data)
#             f.close()
#             audio = Audio(audio_url=f'static/wav/{i}')
#             audio.name = i
#             audio.save()
#     return JsonResponse({
#         'code': 200100,
#         'msg': '数据拿取成功'
#     })


# # 展示所有标注的音频
# def all_audio(request):


# 音频标注(第一次)
def label(request):
    audio_id = request.GET.get('id')
    audio = Audio.objects.filter(id=audio_id).only('id').first()

    if not audio:
        audios = Audio.objects.all().only('id')
        data = {
            'code': 200000,
            'msg': '获取所有标注的音频文件',
            'audios': audios
        }
        return render(request, 'index.html', context=data)
    new_time = int(time.time())
    timeout = Audio.objects.filter(Q(state=0, read=1, time__lt=new_time - 60)).only('state', 'read', 'time').all()
    if timeout:
        for i in timeout:
            i.time = 0
            i.read = 0
            i.save()
    if audio.state != 0 or audio.read != 0:
        data = {
            'code': 2004001,
            'msg': '音频已被操作，跳转未被操作音频',
        }
        return render(request, 'over.html')
        # return JsonResponse(data)
    audio_url = audio.audio_url
    audio_name = audio.name
    if f'{audio_name}.jpg' not in os.listdir('static/img'):
        try:
            img_url = keep_wave(rf'{audio_url}', audio_name, audio)
        except BaseException as err:
            print(err)
            data = {
                'code': 400200,
                'msg': '波形图生成失败'
            }
            return JsonResponse(data)

    else:
        img_url = fr'/static/img/{audio_name}.jpg'

    audio.time = new_time
    audio.read = 1
    audio.save()

    no_audios = Audio.objects.filter(~Q(state=0)).only('id').all()
    audios = Audio.objects.all().only('id')
    data = {
        'code': 200000,
        'msg': '返回波形图和音频',
        'audio_url': '/' + audio_url,
        'img_url': img_url,
        'audio_id': audio.id,
        'no_all_audios': len(no_audios) + 1,
        'all_audios': len(audios)
    }
    return render(request, 'label.html', data)


# 持续标注
def continue_label(request):
    '''
    第一个标注成功后，点下一个会跳转到这个试图函数，先获取音频状态和操作状态为0未标注的音频和音频正在被操作的音频，
    判断是否还存在未标注和未操作的音频，不存在的话判断是否有正在标注的，有的话返回正在标注音频的数量，没有的话则所有音频已经标注，
    存在未标注和未操作的音频，则生成音频图并改变音频的操作状态
    :param request:
    :return:
    '''
    audios = Audio.objects.filter(Q(state=0, read=0)).only('state', 'read')

    audio = audios.first()

    audios_label = Audio.objects.filter(Q(state=0, read=1)).only('state', 'read', 'time').all()

    new_time = int(time.time())
    timeout = audios_label.filter(time__lt=new_time - 60).only('state', 'read', 'time').all()

    if timeout:
        for i in timeout:
            i.time = 0
            i.read = 0
            i.save()
    if not audio:
        if audios_label:
            # data = {
            #     'code': 200400,
            #     'msg': f'未被操作的音频已标注完成，正在被操作的音频还剩{len(audios_label)}个',
            #     'timeout': timeout
            # }
            # return JsonResponse(data)
            return render(request, 'over.html')
        else:
            # data = {
            #     'code': 200001,
            #     'msg': '所有音频已标注完成',
            # }
            # return JsonResponse(data)
            return render(request, 'over.html')

    else:

        audio_url = audio.audio_url
        audio_name = audio.name
        if f'{audio_name}.jpg' not in os.listdir('static/img'):
            try:
                img_url = keep_wave(rf'{audio_url}', audio_name, audio)
            except BaseException as err:
                print(err)
                # data = {
                #     'code': 400200,
                #     'msg': '波形图生成失败'
                # }
                # return JsonResponse(data)
                return render(request, '404.html')

        else:
            img_url = fr'/static/img/{audio_name}.jpg'

        audio.time = new_time
        audio.read = 1
        audio.save()

        audios_num = Audio.objects.all().only('id')
        len_audios_num = len(audios_num)
        out_audios_num = len_audios_num - (len(audios_label) + len(audios.all())) + 1
        print(len(audios_label), len(audios.all()))
        print(len(audios_num))
        data = {
            'code': 200000,
            'msg': '返回波形图和音频',
            'audio_url': '/' + audio_url,
            'img_url': img_url,
            'audio_id': audio.id,
            'no_all_audios': out_audios_num,
            'all_audios': len_audios_num
        }
        return render(request, 'label.html', data)

        # audio_url = audio.audio_url
        # try:
        #     img_url = keep_wave(rf'{audio_url}', audio)
        # except BaseException as err:
        #     print(err)
        #     data = {
        #         'code': 400200,
        #         'msg': '波形图生成失败'
        #     }
        #     return JsonResponse(data)
        # audio.time=new_time
        # audio.read = 1
        # audio.save()
        # data = {
        #     'code': 200000,
        #     'msg': '返回波形图和音频',
        #     'audio_url': audio_url,
        #     'img_url': img_url
        # }
        # return JsonResponse(data)


# 保存标注
def keep_label(request):
    id = request.POST.get('voice_id')
    print(id)
    chemicals = request.POST.get('chemicals')
    distance = request.POST.get('distance')
    detail = request.POST.get('other_info')
    audio = Audio.objects.filter(id=id).only('id').first()
    if not audio:
        data = {
            'code': 200400,
            'msg': '音频失效，重新尝试',
        }
        return JsonResponse(data)

    # with open(os.path.join('/static/txt',f'{audio.name}.txt'),'w') as stream:
    print(os.listdir('static/txt'))
    print(json.dumps({'addr': audio.audio_url, 'chemical': audio.chemical, 'distance': distance}))
    with open(f'static/txt/{audio.name}.txt', 'w') as stream:
        stream.write(json.dumps({'addr': audio.audio_url, 'chemical': audio.chemical, 'distance': distance}))
        # stream.write('{'+f'"addr":{audio.audio_url},'+f'chemical:{audio.chemical},'+f'distance:{distance}'+'}')
    print(12321)
    audio.time = 0
    audio.read = 0
    audio.state = 1
    audio.chemical = chemicals
    audio.distance = distance
    audio.detail = detail
    audio.save()

    audios_state = Audio.objects.filter(state=0).only('state').all()
    # 判断是否还有未标注的
    if audios_state:
        # new_time = int(time.time())
        # audios_label = Audio.objects.filter(Q(state=0, read=1)).only('state', 'read', 'time').all()
        #
        # timeout = audios_label.filter(time__lt=new_time - 60).only('state', 'read', 'time').all()
        # if audios_label:
        #     data = {
        #         'code': 200400,
        #         'msg': f'未被操作的音频已标注完成，正在被操作的音频还剩{len(audios_label)}个',
        #         'timeout': timeout
        #     }
        audios_read = audios_state.filter(~Q(read=0)).all()
        # 判断未标注中是否存全为被操作的
        if len(audios_read) == len(audios_state):
            data = {
                'code': 200500,
                'msg': f'未被操作的音频已标注完成，正在被操作的音频还剩{len(audios_read)}个',
            }
            return JsonResponse(data)
        else:
            data = {
                'code': 200100,
                'msg': '标注成功,继续标注'
            }
            return JsonResponse(data)
    else:
        data = {
            'code': 200001,
            'msg': '所有音频已标注完成',
        }
        return JsonResponse(data)


# 显示所有已标注的
def all_label_audios(request):
    audios = Audio.objects.filter(state=1).only('id').all()
    data = {
        'code': 200000,
        'msg': '获取所有标注的音频文件',
        'audios': audios
    }
    return render(request, 'labels.html', context=data)


# 显示所有未标注的
def all_no_label_audios(request):
    audios = Audio.objects.filter(state=0).only('id').all()
    data = {
        'code': 200000,
        'msg': '获取所有标注的音频文件',
        'audios': audios
    }

    return render(request, 'nolabels.html', context=data)
