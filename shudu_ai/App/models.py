# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

'''
化学物质:chemical
距离:distance
备注:detail
唯一标识:id
音频名称:   name
'''

class Audio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default=None, null=True)
    chemical = models.CharField(max_length=64, default=None, null=True)
    distance = models.CharField(max_length=32, default=0)
    detail = models.TextField(max_length=64, default=None, null=True)

    audio_url = models.CharField(max_length=64,default=None,null=True)
    #state 0未标注 1已标注
    state = models.IntegerField(default=0)
    #read 0未被操作 1已被操作
    read = models.IntegerField(default=0)
    time = models.IntegerField(default=0)

    # img=models.OneToOneField()

    class Meta:
        db_table = 'audio'

class Img(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default=None, null=True)
    img_url = models.ImageField()
    audio = models.OneToOneField("Audio", on_delete=models.CASCADE)

    class Meta:
        db_table = 'img'

# class AudioInit(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=64, default=None, null=True)


# class ImgUrl(models.Model):
#     img_id = models.AutoField(primary_key=True)
#     # 上传的路径是相对于当前的媒体中心，是配置MEDIA_ROOT=os.path.join(BASE_DIR,r'static/upload')
#     img_url = models.ImageField()
#     img_name = models.CharField(max_length=256, null=True)
#     # 默认0未标注
#     state_id = models.IntegerField(default=0)
#     # state_id = models.BooleanField(default=False)
#     read_state=models.IntegerField(default=0)
#     time_img=models.IntegerField(default=0)
#
#     pro = models.ManyToManyField(to='Project', through='ProjectImg')
#
#     class Meta:
#         db_table = 'img_url'
#
#
# # 项目
# class Project(models.Model):
#     pro_id = models.AutoField(primary_key=True, db_column='Project_id')
#     pro_name = models.CharField(max_length=64, db_column='Project_name')
#     # 项目周期
#     pro_time = models.CharField(db_column='Pro_time', max_length=40)
#     # 项目介绍
#     pro_introduction = models.TextField(db_column='Pro_introduction', null=True)
#     # 项目价格
#     pro_picture = models.FloatField(db_column='Pro_picture')
#     # 项目状态。是否被接取,False为否，True为是
#     pro_state = models.BooleanField(default=False)
#     # 类型，待标注/待质检/已完成
#     pro_type = models.IntegerField(db_column='Pro_type', default=0)
#     img = models.ManyToManyField(to='ImgUrl', through='ProjectImg')
#
#     #项目发布时间
#     pro_create=models.IntegerField(default=0)
#
#     class Meta:
#         db_table = 'pro'
#
#
# # 项目图片关联
# class ProjectImg(models.Model):
#     pi_id = models.AutoField(primary_key=True)
#     img = models.ForeignKey(ImgUrl, on_delete=models.DO_NOTHING)
#     project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
#
#     class Meta:
#         db_table = 'proImg'
#
#
# # 团队
# class Team(models.Model):
#     team_id = models.AutoField(db_column='team_id', primary_key=True)
#     team_name = models.CharField(unique=True, db_column='team_name', max_length=64)
#     header = models.OneToOneField("User", on_delete=models.CASCADE, db_column='team_header_id')
#     # 任务
#     pro = models.OneToOneField("Project", null=True, on_delete=models.SET_NULL, db_column='project')
#     # 任务进度：完成0、未完成1
#     task_schedule = models.IntegerField(default=0)
#     regdate = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'team'
#
#
# # 用户
# class User(models.Model):
#     login_id = models.AutoField(db_column='Login_id', primary_key=True)
#     login_name = models.CharField(db_column='Login_name', max_length=15, unique=True)
#     login_paw = models.CharField(db_column='Login_paw', max_length=100)
#     login_tel = models.CharField(unique=True, db_column='Login_tel', max_length=40)
#     login_idcard = models.CharField(unique=True, db_column='Login_idcard', max_length=80)
#     # 归属团队
#     department = models.ForeignKey(Team, db_column='team_id', null=True, on_delete=models.SET_NULL)
#     regdate = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'user'
#
#
# # 用户与项目的第三张表
# class User_Pro(models.Model):
#     user_pro_id = models.AutoField(primary_key=True, db_column='User_pro_id')
#     user_id = models.ForeignKey(User, db_column='User_id', on_delete=models.DO_NOTHING)
#     pro_id = models.ForeignKey(Project, db_column='Pro_id', on_delete=models.DO_NOTHING)
#
#     class Meta:
#         db_table = 'user_pro'
#         unique_together = (("user_id", "pro_id"),)
