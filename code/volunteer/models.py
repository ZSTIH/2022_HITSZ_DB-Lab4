# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=10, verbose_name="用户编号")
    organization = models.ForeignKey('Organization', models.DO_NOTHING, verbose_name="义工组织")
    department = models.ForeignKey('Department', models.DO_NOTHING, verbose_name="学院")
    username = models.CharField(max_length=20, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="密码")
    total_hours = models.FloatField(verbose_name="累计服务时长")
    average_score = models.FloatField(verbose_name="平均服务得分")

    class Meta:
        ordering = ['username']
        db_table = 'user'
        verbose_name = "志愿者信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Organization(models.Model):
    organization_id = models.CharField(primary_key=True, max_length=10, verbose_name="义工组织编号")
    organization_name = models.CharField(max_length=20, verbose_name="义工组织名称")

    class Meta:
        ordering = ['organization_name']
        db_table = 'organization'
        verbose_name = "义工组织信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.organization_name


class Department(models.Model):
    department_id = models.CharField(primary_key=True, max_length=10, verbose_name="学院编号")
    department_name = models.CharField(max_length=20, verbose_name="学院名称")

    class Meta:
        ordering = ['department_name']
        db_table = 'department'
        verbose_name = "学院信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.department_name


class ServiceEvaluation(models.Model):
    service_evaluation_id = models.CharField(primary_key=True, max_length=10, verbose_name="服务评价编号")
    admin = models.ForeignKey('application.Admin', models.DO_NOTHING, verbose_name="评分管理员")
    user = models.ForeignKey(User, models.DO_NOTHING, verbose_name="被评分志愿者")
    activity = models.ForeignKey('activity.Activity', models.DO_NOTHING, verbose_name="被评价活动")
    service_hours = models.FloatField(verbose_name="实际服务时长")
    score = models.FloatField(verbose_name="评分")
    comment = models.CharField(max_length=20, verbose_name="评语")

    class Meta:
        ordering = ['service_evaluation_id']
        db_table = 'service_evaluation'
        verbose_name = "服务评价信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"对【{self.user}】完成活动【{self.activity}】的评价"
