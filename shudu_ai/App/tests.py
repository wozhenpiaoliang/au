# import wave
# data=wave.open('../audio/file/许嵩 - 雅俗共赏.wav','rb')
# print(data.tostring())
import os

from django.test import TestCase

# Create your tests here.
from shudu_ai.settings import BASE_DIR
addr_wav=os.path.join(BASE_DIR,'audio/file')
print(os.listdir(addr_wav))

a='OSR_us_000_0017_8k.txt.wav'
print(os.path.splitext(a))

print(a.endswith('.wav'))
a=(1,5)
a.