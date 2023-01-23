# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activity(models.Model):
    activity_id = models.CharField(primary_key=True, max_length=10, verbose_name="活动编号")
    activity_type = models.ForeignKey('ActivityType', models.DO_NOTHING, verbose_name="活动类型")
    location = models.ForeignKey('Location', models.DO_NOTHING, verbose_name="活动地点")
    admin = models.ForeignKey('application.Admin', models.DO_NOTHING, verbose_name="发布活动的管理员")
    activity_name = models.CharField(max_length=20, verbose_name="活动名称")
    activity_state = models.DecimalField(
        choices=((0, "尚未开始招募"), (1, "正在招募"), (2, "招募结束"), (3, "活动已结束")),
        max_digits=4, decimal_places=0,
        verbose_name="活动状态")
    activity_introduction = models.CharField(max_length=100, verbose_name="活动简介")
    activity_requirements = models.CharField(max_length=100, verbose_name="活动要求")
    activity_start_time = models.DateTimeField(verbose_name="活动开始时间")
    activity_end_time = models.DateTimeField(verbose_name="活动结束时间")
    headcount = models.IntegerField(verbose_name="招募总人数")

    class Meta:
        ordering = ['activity_start_time']
        db_table = 'activity'
        verbose_name = "活动信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.activity_name


class Location(models.Model):
    location_id = models.CharField(primary_key=True, max_length=10, verbose_name="地点编号")
    address = models.CharField(max_length=100, unique=True, verbose_name="地点名称")

    class Meta:
        ordering = ['address']
        db_table = 'location'
        verbose_name = "地点信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class ActivityType(models.Model):
    activity_type_id = models.CharField(primary_key=True, max_length=10, verbose_name="活动类型编号")
    activity_type_name = models.CharField(max_length=20, unique=True, verbose_name="活动类型名称")

    class Meta:
        ordering = ['activity_type_name']
        db_table = 'activity_type'
        verbose_name = "活动类型信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.activity_type_name
