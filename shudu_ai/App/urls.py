from django.urls import path

from App.views import index, label, continue_label, keep_label, take_wav, all_label_audios, all_no_label_audios

urlpatterns = [
    path('index/',index),#首页,显示所有的音频
    path('audio/take/',take_wav),#拿数据
    path('label/',label),#开始标注
    path('label/continue/',continue_label),#持续标注
    path('keep_label/',keep_label),#保存标注

    path('index/label/audios/',all_label_audios),#显示所有已标注的
    path('index/no/label/audios/',all_no_label_audios),#显示所有已标注的


]
