from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Member, District_approver, Funding_approver, Application
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib import messages

from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.core.files.storage import default_storage

# Create your views here.
def login(request):
    if request.method =="POST" :
        phone = request.POST['phone']
        password = request.POST['password']

        member_user = Member.objects.filter(phonenumber=phone).filter(password=password ).first()
        admin_user = authenticate(username=phone, password=password)
        da_user =  District_approver.objects.filter(phonenumber=phone).filter(password=password ).first()
        fa_user =  Funding_approver.objects.filter(phonenumber=phone).filter(password=password ).first()

        if(member_user):
            request.session['phone_number'] = phone    
            request.session['user'] = 'member'    
            return redirect('/member')
        elif(admin_user):
            request.session['phone_number'] = phone  
            request.session['user'] = 'admin'
            return redirect('/register_DA')
        elif(da_user):
            request.session['phone_number'] = phone  
            request.session['user'] = 'da'      
            return redirect('/district_administrator')   
        elif(fa_user):
            request.session['phone_number'] = phone  
            request.session['user'] = 'fa'      
            return redirect('/funding_administrator')  
        else:
            messages.info(request,"Incorrect Phone Number OR Password ")
            return redirect('/')

    else:
        request.session.setdefault('phone_number', 'NO')
        request.session.setdefault('user', 'NO')
        if( request.session['phone_number'] !="NO"):
            if( request.session['user'] =="member"):
                return redirect('/member')
            elif( request.session['user'] =="admin"):
                return redirect('/register_FA')
            elif( request.session['user'] =="da"):
                return redirect('/district_administrator')
            elif( request.session['user'] =="fa"):
                return redirect('/funding_administrator')
        else:
            return render(request, 'login.html')


def register(request):
    if request.method =="POST" :  
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['birthday']
        phone = request.POST['phone']
        province = request.POST['province']
        district = request.POST['district']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        file= request.FILES['filename']
        file_name = default_storage.save(file.name, file)
        pic= request.FILES['filename']

        user1 = Member.objects.filter(phonenumber=phone)
        user2 = District_approver.objects.filter(phonenumber=phone)
        user3 = Funding_approver.objects.filter(phonenumber=phone)
        if(user1 or user2 or user3):
            messages.info(request,"Phone number exists")
            return redirect('/register')
        elif(password1 != password2):
            messages.info(request,"Both passwords don't match")
            return redirect('/register')    
        else:
           user = Member.objects.create(first_name=first_name, last_name= last_name,dob=dob, phonenumber=phone, pic=pic, province=province,district=district, password=password1 )
           user.save()
           return redirect('/success')
    else:
        return render(request, 'register.html')


def member(request):
    if(request.session['user'] == 'member'):
       
        phone = request.session['phone_number']
        user = Member.objects.filter(phonenumber=phone).first()  

        projects = Application.objects.filter(member=user)
        
        return render(request, 'member.html', {'user':user, 'projects':projects})    
    else:
        return redirect('/')   


def application(request):
    if(request.session['user']== 'member'):
        phone = request.session['phone_number']
        user = Member.objects.filter(phonenumber=phone).first()  
        if request.method =="POST" :
            project_name = request.POST['name']
            industry = request.POST['industry']
            no_of_youth = request.POST['no_of_youth']
            funding = request.POST['funding']
            payback = request.POST['payback']

            file= request.FILES['filename']
            file_name = default_storage.save(file.name, file)
            doc= request.FILES['filename']
            
            user = Application.objects.create(project_name=project_name, industry= industry,funding=funding, no_of_youth=no_of_youth, payback=payback, member=user, file= doc )
            user.save()
            return redirect('/member')
        else:
            return render(request, 'application_form.html',{'user':user})   
    else:
        return redirect('/')          


def district_administrator(request):
    if(request.session['user']== 'da'):
        phone = request.session['phone_number']
        user = District_approver.objects.filter(phonenumber=phone).first()
        projects = Application.objects.filter(member__district=user.district).values('reference_no', 'industry', 'funding', 'stage1_status', 'member__first_name', 'member__last_name')

        if request.method =="POST" :
            selection = request.POST['selection']
            projects = Application.objects.filter(member__district=user.district,stage1_status=selection  ).values('reference_no', 'industry', 'funding', 'stage1_status', 'member__first_name', 'member__last_name')

            return render(request, 'district_administrator.html',{'user':user, 'projects':projects})  
        else:
            return render(request, 'district_administrator.html',{'user':user, 'projects':projects})   
    else:
        return redirect('/')   

def da_actions(request):
    if(request.session['user']== 'da'):
        phone = request.session['phone_number']
        user = District_approver.objects.filter(phonenumber=phone).first()
        projects = Application.objects.filter(member__district=user.district).values('reference_no', 'industry', 'funding', 'stage1_status', 'member__first_name', 'member__last_name')

        if request.method =="POST" :
            selection = request.POST['selection'] 
            reference_no = request.POST['reference_no'] 
            projects = Application.objects.filter(reference_no=reference_no).update(stage1_status=selection, district_approver=user.first_name + user.last_name)

            return redirect('/district_administrator')   
        else:
            return redirect('/district_administrator')   
    else:
        return redirect('/')   


def funding_administrator(request):
    if(request.session['user']== 'fa'):
        phone = request.session['phone_number']
        user = Funding_approver.objects.filter(phonenumber=phone).first()
        projects = Application.objects.filter(stage1_status=1).values('reference_no', 'industry', 'funding', 'stage2_status', 'district_approver', 'member__province', 'member__first_name', 'member__last_name', 'member__member_no')

        if request.method =="POST" :
            selection = request.POST['selection']
            projects = Application.objects.filter(stage1_status=1,stage2_status=selection).values('reference_no', 'industry', 'funding', 'stage2_status', 'district_approver', 'member__province', 'member__first_name', 'member__last_name', 'member__member_no')

            return render(request, 'funding_administrator.html',{'user':user, 'projects':projects})  
        else:
            return render(request, 'funding_administrator.html',{'user':user, 'projects':projects})   
    else:
        return redirect('/') 


def fa_actions(request):
    if(request.session['user']== 'fa'):
        phone = request.session['phone_number']
        user = Funding_approver.objects.filter(phonenumber=phone).first()
        projects = Application.objects.filter(stage1_status=1).values('reference_no', 'industry', 'funding', 'stage2_status', 'district_approver', 'member__province', 'member__first_name', 'member__last_name')
        
        if request.method =="POST" :
            selection = request.POST['selection'] 
            reference_no = request.POST['reference_no'] 
            projects = Application.objects.filter(reference_no=reference_no).update(stage2_status=selection)
            
            return redirect('/funding_administrator')   
        else:
            return redirect('/funding_administrator')   
    else:
        return redirect('/')  


def success(request):
    if request.session['phone_number'] == 'NO':
        return render(request, 'success.html')    
    else:     
       return redirect('/') 

def register_DA(request): 
    if(request.session['user']== 'admin'):
        username = request.session['phone_number']
        user = User.objects.filter(username=username).first()
        if request.method =="POST" :
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            province = request.POST['province']
            district = request.POST['district']
            password = request.POST['password']

            user1 = Member.objects.filter(phonenumber=phone)
            user2 = District_approver.objects.filter(phonenumber=phone)
            user3 = Funding_approver.objects.filter(phonenumber=phone)
            if(user1 or user2 or user3):
                messages.info(request,"Phone number exists")
                return redirect('/register_DA')
            else:
                user = District_approver.objects.create(first_name=first_name, last_name= last_name,phonenumber=phone, province=province, district=district, password=password)
                return redirect('/register_DA')
        else:
            return render(request, 'register_DA.html',{'user':user})
    else:    
        return redirect('/')   


def register_FA(request): 
    if(request.session['user']== 'admin'):
        username = request.session['phone_number']
        user = User.objects.filter(username=username).first()
        if request.method =="POST" :
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            organization = request.POST['organization']
            password = request.POST['password']

            user1 = Member.objects.filter(phonenumber=phone)
            user2 = District_approver.objects.filter(phonenumber=phone)
            user3 = Funding_approver.objects.filter(phonenumber=phone)
            if(user1 or user2 or user3):
                messages.info(request,"Phone number exists")
                return redirect('/register_FA')
            else:
                user = Funding_approver.objects.create(first_name=first_name, last_name= last_name,phonenumber=phone, organization=organization, password=password)
                return redirect('/register_FA')
        else:
            return render(request, 'register_FA.html',{'user':user})
    else:    
        return redirect('/')  


def logout(request):
    if request.session['phone_number']:
        del request.session['phone_number'] 
        del request.session['user']         
        return redirect('/')             


def user_profile_fa(request, id):
    if(request.session['user']== 'fa'):
        phone = request.session['phone_number']
        user = Funding_approver.objects.filter(phonenumber=phone).first()
        projects = Application.objects.filter(reference_no=id).first()
        
        member_no=Application.objects.filter(reference_no=id).values('member__member_no').first()
        member_no= member_no['member__member_no']
        
        member = Member.objects.filter(member_no=member_no).first()
        
        return render(request, 'user_profile_fa.html',{'user':user, 'projects':projects, 'member':member })   
    else:
        return redirect('/') 



def user_profile_da(request, id):
    if(request.session['user']== 'da'):
        phone = request.session['phone_number']
        user = Funding_approver.objects.filter(phonenumber=phone).first()
        projects = Application.objects.filter(reference_no=id).first()
        
        member_no=Application.objects.filter(reference_no=id).values('member__member_no').first()
        member_no= member_no['member__member_no']

        member = Member.objects.filter(member_no=member_no).first()
        
        return render(request, 'user_profile_da.html',{'user':user, 'projects':projects, 'member':member })   
    else:
        return redirect('/') 