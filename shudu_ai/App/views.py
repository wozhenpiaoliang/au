import os
import time
import wave
import numpy as np
# import scipy.signal as signal
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from App.models import Audio


from App.tool import keep_wave

#首页
from shudu_ai.settings import BASE_DIR


def index(request):
    audios = Audio.objects.all().only('id')
    data = {
        'code': 200000,
        'msg': '获取所有标注的音频文件',
        'audios': audios
    }
    return render(request,'index.html',context=data)

#拿音频数据
def take_wav(request):
    addr_wav=os.path.join(BASE_DIR,'audio/file')
    for i in os.listdir(addr_wav):
        # 打开wav文件 ，open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据。
        f = wave.open(os.path.join(addr_wav,i), "rb")
        # 读取格式信息
        # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采
        # 样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        # 读取波形数据
        # 读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）,二进制数据
        str_data = f.readframes(nframes)
        f.close()
        # print(str_data)
        # 转成可读数据
        # wave_data = np.fromstring(str_data, dtype=np.short)
        # time = 10
        f = wave.open(os.path.join(BASE_DIR,f'static/wav/{i}'), "wb")
        f.setnchannels(nchannels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        f.writeframes(str_data)
        f.close()
        audio=Audio(audio_url=f'/static/wav/{i}')
        audio.name=i
        audio.save()
    return JsonResponse({
        'code':200100,
        'msg':'数据拿取成功'
    })


# # 展示所有标注的音频
# def all_audio(request):


# 音频标注(第一次)
def label(request):
    audio_id=request.GET.get('id')
    audio=Audio.objects.filter(id=audio_id).only('id').first()

    if not audio:
        data={
            'code':200400,
            'msg':'获取失败',
        }
        return JsonResponse(data)
    new_time = int(time.time())
    timeout=Audio.objects.filter(Q(state=0, read=1, time__lt=new_time - 60)).all().only('state','read','time')
    if timeout:
        for i in timeout:
            i.time=0
            i.read=0
            i.save()
    if audio.state!=0 and audio.read!=0:
        data={
            'code':2004001,
            'msg':'音频已被操作，跳转未被操作音频',
        }
        return JsonResponse(data)
    audio_url=audio.audio_url
    audio_name=audio.name
    img_url = keep_wave(rf'{audio_url}',audio_name, audio)

    # try:
    #     img_url=keep_wave(rf'{audio_url}',audio)
    # except BaseException as err:
    #     print(err)
    #     data={
    #         'code':400200,
    #         'msg':'波形图生成失败'
    #     }
    #     return JsonResponse(data)

    audio.time=new_time
    audio.read=1
    print(11111111111111111111111)
    audio.save()
    data={
        'code':200000,
        'msg':'返回波形图和音频',
        'audio_url':audio_url,
        'img_url':img_url,
        'audio_id':audio.id
    }
    return render(request,'label.html',data)

#持续标注
def continue_label(request):
    '''
    第一个标注成功后，点下一个会跳转到这个试图函数，先获取音频状态和操作状态为0未标注的音频和音频正在被操作的音频，
    判断是否还存在未标注和未操作的音频，不存在的话判断是否有正在标注的，有的话返回正在标注音频的数量，没有的话则所有音频已经标注，
    存在未标注和未操作的音频，则生成音频图并改变音频的操作状态
    :param request:
    :return:
    '''
    audio=Audio.objects.filter(Q(state=0 , read=0)).only('state','read').first()
    audios_label=Audio.objects.filter(Q(state=0 , read=1)).only('state','read','time').all()
    new_time = int(time.time())
    timeout =audios_label.filter(time_lt=new_time - 60).only('state', 'read', 'time').all()
    if timeout:
        for i in timeout:
            i.time = 0
            i.read = 0
            i.save()

    if not audio:
        if audios_label:
            data={
                  'code':200400,
                  'msg':f'未被操作的音频已标注完成，正在被操作的音频还剩{len(audios_label)}个',
                  'timeout':timeout
              }
            return JsonResponse(data)
        else:
            data={
                'code':200000,
                'msg':'所有音频已标注完成',
            }
            return JsonResponse(data)
    else:

        audio_url = audio.audio_url()
        try:
            img_url = keep_wave(rf'{audio_url}', audio)
        except BaseException as err:
            print(err)
            data = {
                'code': 400200,
                'msg': '波形图生成失败'
            }
            return JsonResponse(data)
        audio.time=new_time
        audio.read = 1
        audio.save()
        data = {
            'code': 200000,
            'msg': '返回波形图和音频',
            'audio_url': audio_url,
            'img_url': img_url
        }
        return JsonResponse(data)


#保存标注
def keep_label(request):
    id=request.POST.get('id')
    chemicals=request.POST.get('chemicals')
    distance=request.POST.get('distance')
    detail = request.POST.get('detail')
    audio=Audio.objects.filter(id=id).only('id').first()
    if not audio:
        data={
            'code':200400,
            'msg':'音频失效，重新尝试',
        }
        return JsonResponse(data)

    with open(os.path.join('/static/txt',f'{audio.name}.txt'),'w') as stream:
        stream.write({
            'addr':audio.audio_url,
            'chemical':audio.chemical,
            'distance':distance
        })
    audio.time=0
    audio.read=0
    audio.state=1
    audio.chemical=chemicals
    audio.distance=distance
    audio.detail=detail
    audio.save()
    data={
        'code':200100,
        'msg':'标注成功'
    }
    return JsonResponse(data)


