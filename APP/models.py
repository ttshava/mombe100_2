from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import ugettext_lazy as _
import datetime
import os


class Member(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField()
    phonenumber = models.CharField(max_length=255, unique=True)
    pic = models.CharField(max_length=255, blank=True)  
    province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    member_no= models.AutoField(primary_key=True)    

    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = []


class District_approver(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255, unique=True)
    province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = []    


class Funding_approver(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255, unique=True)
    organization = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = [] 


class Application(models.Model):
    project_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)    
    no_of_youth= models.IntegerField()
    funding = models.CharField(max_length=255)   
    payback = models.CharField(max_length=255)  
    reference_no= models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    overall_status= models.IntegerField(default=0) # 0 - pending ,  1 - approved by DA ,  2 - approved by FA    
    stage1_status= models.IntegerField(default=0) # 0 - pending ,  1 - approved by DA, ,  2 - Rejected by DA  
    stage2_status= models.IntegerField(default=0) # 0 - pending ,  1 -  approved by FA,  2 - Rejected by FA 
    district_approver = models.CharField(max_length=255, null=True)
    stage1_approval_date= models.DateField(auto_now=True)
    file =  models.CharField(max_length=255, blank=True)  
    

    REQUIRED_FIELDS = []     