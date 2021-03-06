from datetime import datetime

from DjangoUeditor.models import UEditorField
from django.db import models

from organization.models import CourseOrg, Teacher


# Create your models here.

class Course(models.Model):
    """
    课程模型类
    """
    DEGREE = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级"),
    )
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', blank=True, null=True)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = UEditorField(verbose_name="课程详情",width=600, height=300,  imagePath="courses/ueditor/",
                                         filePath="courses/ueditor/", default="")
    is_banner = models.BooleanField(default=False,verbose_name="是否轮播")
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", null=True, blank=True)
    degree = models.CharField(choices=DEGREE, max_length=2, verbose_name='课程难度')
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default="后台开发", verbose_name="课程类别", max_length=20)
    tag = models.CharField(verbose_name="课程标签", max_length=10, default="")
    you_know = models.CharField(verbose_name="课程须知", max_length=300, default="")
    teacher_tell = models.CharField(verbose_name="老师告诉你", max_length=300, default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()
    get_zj_nums.short_description = "章节数"

    def get_learn_users(self):
        # 获取学习用户
        return self.usercourse_set.all()[:5]

    def get_lesson(self):
        # 获取课程章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    章节表
    """
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        # 获取章节视频
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    """
    视频表
    """
    lesson = models.ForeignKey(Lesson, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    url = models.CharField(max_length=200, verbose_name="访问地址", default="")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    """
    课程资源表
    """
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
