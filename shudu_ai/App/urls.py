from django.urls import path

from App.views import  index, label, continue_label, keep_label, take_wav

urlpatterns = [
    path('index/',index),#首页
    path('audio/take/',take_wav),#拿数据
    path('label/',label),#开始标注
    path('label/continue/',continue_label),#持续标注
    path('keep_label/',keep_label),#保存标注

]
