from django.db import models

class Employee(models.Model):
    empid = models.AutoField('employee_id',primary_key=True)
    name=models.CharField('employee_name',max_length=100)
    address=models.CharField('employee_address',max_length=200)
    phone=models.CharField('employee_phone',max_length=10)
    isadmin = models.CharField('admin/user', max_length=1)
    department=models.CharField('employee_department',max_length=100)
    username = models.CharField('User Name', max_length=100)
    email = models.EmailField('User Email', max_length=100)
    password = models.TextField('User Password', max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'employee'

class Punch(models.Model):
    punchid=models.AutoField(primary_key=True)
    punchin=models.TimeField()
    punchout=models.TimeField()
    date=models.DateField()
    empid=models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return '{} {} {} {}'.format(self.punchin,self.punchout,self.empid,self.date)

    class Meta:
        db_table = 'punch'
