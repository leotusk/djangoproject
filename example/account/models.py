from django.db import models

# Create your models here.
class Account(models.Model):
    user_id = models.CharField(max_length=20, unique=True, verbose_name='아이디')
    user_pw = models.CharField(max_length=20, verbose_name='비밀번호')
    user_name = models.CharField(max_length=20, verbose_name='이름')
    user_number = models.CharField(max_length=5, unique=True, verbose_name='학번')
    user_register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='계정 생성시간')

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'Account'
        verbose_name = '계정'
        verbose_name_plural = '계정'