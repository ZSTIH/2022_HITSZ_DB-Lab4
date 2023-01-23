# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Application(models.Model):
    application_id = models.CharField(primary_key=True, max_length=10, verbose_name="申请编号")
    admin = models.ForeignKey('Admin', models.DO_NOTHING, verbose_name="审核管理员")
    user = models.ForeignKey('volunteer.User', models.DO_NOTHING, verbose_name="申请志愿者")
    activity = models.ForeignKey('activity.Activity', models.DO_NOTHING, verbose_name="申请活动")
    application_time = models.DateTimeField(verbose_name="申请时间")
    application_state = models.DecimalField(choices=((0, "尚未审核"), (1, "审核通过"), (2, "审核不通过")), max_digits=4,
                                            decimal_places=0, verbose_name="申请状态")
    application_reason = models.CharField(max_length=100, verbose_name="申请理由")
    check_result = models.DecimalField(choices=((1, "审核通过"), (2, "审核不通过")), max_digits=4, decimal_places=0,
                                       blank=True, null=True, verbose_name="审核结果")
    check_reason = models.CharField(max_length=100, blank=True, null=True, verbose_name="审核理由")
    check_time = models.DateTimeField(blank=True, null=True, verbose_name="审核时间")

    class Meta:
        ordering = ['application_time']
        db_table = 'application'
        verbose_name = "申请信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"【{self.user}】申请报名活动【{str(self.activity)}】"


class Admin(models.Model):
    admin_id = models.CharField(primary_key=True, max_length=10, verbose_name="管理员编号")
    department = models.ForeignKey('volunteer.Department', models.DO_NOTHING, verbose_name="学院")
    admin_name = models.CharField(max_length=20, unique=True, verbose_name="管理员名")
    admin_password = models.CharField(max_length=20, verbose_name="密码")

    class Meta:
        ordering = ['admin_name']
        db_table = 'admin'
        verbose_name = "管理员信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.admin_name
