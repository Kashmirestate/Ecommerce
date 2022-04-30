from pickletools import read_bytes1
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .serializers import *
from .decorator import decorator
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from .models import *
import random
from Ecommerce import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
# Create your views here.
def send_email(email,otp):
    """
    Function to send email to employee.
    """
    
    subject = "your account need to be verified"
    message = f'OTP - {otp}  '
    email_from = settings.EMAIL_HOST_USER
    message = EmailMessage(subject, message, email_from, [email])
    message.send(fail_silently=True)




class HomePage(View):
    def get(self,request):
        final_lst=[]
        obj=cover.objects.all()
        if obj.count() > 0:
            for row in obj:
                final_lst.append({'id':row.id,'cover':row.cover,'desc':row.description})

            return render(request,'home.html',{'IMAGES':final_lst})
        else:
            return render(request,'home.html')
        

class Register(View):
    def get(self,request):
        return render(request,"register.html")
    def post(self,request):
       
        if RegisterSerial(data=request.POST).is_valid():
            if UserProfile.objects.filter(email=request.POST['email']).count() ==0:
                request.session['otp']=random.randint(1000,9999)
                request.session['email']=request.POST['email']
                request.session['address']=request.POST['address']
                request.session['password']=request.POST['password']
                request.session['type']=request.POST['type']
                #data=UserProfile.objects.create_user(email=request.POST['email'],password=request.POST['password'])
                send_email(request.session['email'],request.session['otp'])
                message="success"
            else:
                message="email already exist"
            


            return render(request,"register.html",{'status':message})
        else:
            return render(request,"register.html",{'status':'Please insert valid data '})
class Login(View):
    def get(self,request):
        return render(request,"login.html")
    def post(self,request):
        
        # import pdb;pdb.set_trace()
        email=request.POST['email']
        password=request.POST['password']
        data=UserProfile.objects.filter(email=email)    
        if data.count()==1:

            check_obj=UserProfile.objects.get(email=email)
            if check_obj.check_password(password):
                request.session['check']=email
            
                message="loged in successfully"  
                return redirect('dashboard_page')
            else:
                message="invalid password"
        else:
            message=  "invalid Email"
        return render(request,"login.html",{"status":message})

@method_decorator(decorator,name='dispatch')
class dashboad(View):
    def get(self,request):
        return render(request,"dash.html",{'status':'welcome'})


class Verify(View):
    def post(self,request):
        #import pdb;pdb.set_trace()
        if request.session.get('email'):
            try:
                if str(request.session.get('otp')) == str(request.POST['otp']):
                    UserProfile.objects.create_user(email=request.session.get('email'),username=request.session.get('email'),password=request.session.get('password'),Address=request.session.get('address'),Role=request.session.get('type'))
                    return render(request,'login.html',{'message':'user registered'})
                else:
                    return render(request,'register.html',{'message':'wrong otp entered try again'})
            except: 
                return render(request,'register.html',{'message':'Please insert valid data !'})

        else:
            return render(request,'register.html')

@method_decorator(decorator,name='dispatch')   
class logout(View):
 def get(self,request,*args,**kwargs):  
    del request.session['check']
    return redirect('login_page')

@method_decorator(decorator,name='dispatch')
class Addcatagory(View):
    def get(self,request):
        return render(request,'addcat.html')
    def post(self,request):
        cat=request.POST.get('catagory',None) 

        if cat:
            if catagory.objects.filter(name=cat).count() > 0 : 
                message="catagory already exists"
            else:

                obj=catagory.objects.create(name=cat)
                obj.save()
                message="catagory added"
        else:
            message="insert proper data"
        return render(request,'addcat.html',{'message':message})


#@method_decorator(decorator,name='dispatch')
class Getcategory(View):
    def get(self,request):
        obj=catagory.objects.all()
        serial=getcatagoryserial(obj,many=True)
        return JsonResponse({'status':'true','response':serial.data},safe=False)

class Getsubcategory(View):
    def get(self,request,id):
        #import pdb;pdb.set_trace()
        try:
            obj=SubCatagory.objects.filter(main_catagory__id=id)
            serial=getsubcatagoryserial(obj,many=True)
            return render(request,'addcat.html',{'data':serial.data,'lst':'true'})
        except:
            return render(request,'addcat.html',{'message':'no data','lst':'true'})
class indexPage(View):
    def get(self,request):
        final_lst=[]
        obj=cover.objects.all()
        if obj.count() > 0:
            for row in obj:
                final_lst.append({'id':row.id,'cover':row.cover,'desc':row.description})

            return render(request,'index.html',{'IMAGES':final_lst})
        else:
            return render(request,'index.html')


class Addsubcatagory(View):
    def get(self,request):
        return render(request,'addsubcat.html')
    def post(self,request):
        subcat=request.POST.get('subcatagory',None)
        cat=request.POST.get('catagory',None) 
        #import pdb;pdb.set_trace()
        if cat and subcat:
            if catagory.objects.filter(name=cat).count() > 0 : 
                cat_obj=catagory.objects.get(name=cat)
                obj=SubCatagory.objects.create(name=subcat,main_catagory=cat_obj)
                obj.save()
                message="subcatagory added"
                
            else:

                
                message="catagory doesnot exists"
        else:
            message="insert proper data"
        return render(request,'addsubcat.html',{'message':message})
class UploadedProducts(View):
    def get(self,request ,id):
        #import pdb;pdb.set_trace()
        try:
            
        
            all_posts=cover.objects.filter(id=id)
            


            
            return render(request,"allproducts.html",{'IMAGES':all_posts})
        except:
            return render(request,"allproducts.html")

class uploadproducts(View):
    def get(self,request):
        return render(request,'uploadproducts.html')
    def post(self,request):
        try:
            
        
            file_name=request.FILES.getlist('image')
            cover_name=request.FILES.get('cover')
            disc=request.POST.get('desc')
            fact=0
            
            for image in file_name:
                if str(image).endswith(('.jpg','.png','.jpeg')):
                    pass
                else:
                    fact=1
            if not str(cover_name).endswith(('.jpg','.png','.jpeg')):
                fact=1
            #import pdb;pdb.set_trace()
            fs = FileSystemStorage()
            date_time = random.randint(1000,9999)
            file = fs.save(str(date_time)+cover_name.name, cover_name)
            fileurl = fs.url(file)
            data=cover.objects.create(cover=str(date_time)+cover_name.name,description=disc,catagory=catagory.objects.get(id=request.POST['catagory']),sub_catagory=SubCatagory.objects.get(id=request.POST['subcatagory']),quantity=request.POST['quantity'])
            data.save()

                    
                    
            if fact==0:        
                for img in file_name:
                    date_time = random.randint(1000,9999)
                    file = fs.save(str(date_time)+img.name, img)
                    fileurl = fs.url(file)
                    dt_image=filedata.objects.create(Images=str(date_time)+img.name,product_cover=data)
                    dt_image.save()
                


                return render(request,"uploadproducts.html",{'message':" POST SUCCESSFULLY UPLOADED "})

            else:
                return render(request,'uploadproducts.html',{'message':" It Will only Accept JPG JPEG PNG Formats ! MAKE SURE ALL FILES COMES UNDER THESE FORMATS "})
        except:
            return render(request,'uploadproducts.html',{'message':" Please upload proper data"})



class GetsubcategoryAJX(View):
    def get(self,request,id):
        #import pdb;pdb.set_trace()
        try:
            obj=SubCatagory.objects.filter(main_catagory__id=id)
            serial=getsubcatagoryserial(obj,many=True)
            return JsonResponse({'response':serial.data,'status':'true'})
        except:
            return JsonResponse({'response':"no data",'status':'false'})

class inner(View):
    def get(self,request ,my_id):
        #import pdb;pdb.set_trace()
        try:
            
        
            cover_obj=cover.objects.get(id=my_id)
            all_posts=filedata.objects.filter(product_cover=cover_obj)



            
            return render(request,"inner.html",{'IMAGES':all_posts,'cover':cover_obj})
        except:
            return render(request,"inner.html")






                
