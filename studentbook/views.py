from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from .models import Employee,Punch
from django.contrib import messages
from .forms import EmployeeForm
from  datetime import datetime
import datetime as dt
import calendar

def login(request):
    if request.POST:
        email=request.POST['email']
        password=request.POST['password']
        count=Employee.objects.filter(email=email,password=password).count()
        if count>0:
            currMonth = datetime.now().month
            request.session['currMonth'] = currMonth
            currYear = datetime.now().year
            request.session['currYear'] = currYear
            emp=Employee.objects.filter(email=email)
            isadmin = emp[0].isadmin
            request.session['is_logged'] = True  # some name  give for session
            if isadmin==1:
                return redirect('home')  # redirect home page
            else:
                request.session['empid'] = emp[0].empid
                return redirect('employee')
        else:
            messages.error(request,"Invalid Username and Password")#flash messages
            return redirect('login')
    return render(request,'studentbook/login.html')

def home(request):
    if request.session.has_key('is_logged'):#this is check and match be session variable
        return render(request,'studentbook/home.html')
    return redirect('login')

def logout(request):
    del request.session['is_logged']
    return redirect('login')
def logouts(request):
    del request.session['empid']
    return redirect('login')

def employee(request):
    return render(request,'studentbook/emp_punch_page.html')


def detail(request):
    if request.session.has_key('is_logged'):
        pk=request.session['empid']
        obj=Employee.objects.get(empid=pk)
        obj1=Punch.objects.all().filter(empid=pk)
        return render(request,'studentbook/Detail.html',{'obj':obj,'obj1':obj1})


def punch(request):
    return render(request,'studentbook/Punch.html')

def adminn(request):
    return render(request,'studentbook/emp_punch_admin_page.html')



def punch_admin(request):
    if request.session['currMonth'] < 1:
        request.session['currYear']=request.session['currYear']-1
        request.session['currMonth']=12
    if request.session['currMonth'] > 12:
        request.session['currYear']=request.session['currYear']+1
        request.session['currMonth']=1
    currMonth = request.session['currMonth']
    currYear = request.session['currYear']
    firstDayCurrMonth=1
    lastDayCurrMonth=calendar.monthrange(currYear,currMonth)[1]
    emp=Employee.objects.all()
    obj = Punch.objects.filter(date__range=[datetime.today().replace(day=1), datetime.today().replace(day=lastDayCurrMonth)])
    attendance={}
    for e in emp:
        curremp={}
        for i in range(1,lastDayCurrMonth+1):
            curremp[i]={"intime":dt.time(0,0),"outtime":dt.time(0,0)}
        attendance[e]=curremp

    for e in emp:
        oo = obj.filter(empid=e)
        for o in oo:
            for a in attendance:
                if o.date.month==currMonth and o.date.year==currYear:
                    attendance[e][o.date.day]["intime"]=o.punchin
                    attendance[e][o.date.day]["outtime"]=o.punchout
    return render(request,'studentbook/AdminPunch.html',{'comp':dt.time(0,0),'obj':obj,'attendance':attendance,'currMonth':calendar.month_name[currMonth],'currYear':currYear,'firstDayCurrMonth':firstDayCurrMonth,'lastDayCurrMonth':lastDayCurrMonth})


def next(request):
    request.session['currMonth']=request.session['currMonth']+1
    return redirect('punch_admin')

def previous(request):
    request.session['currMonth'] = request.session['currMonth'] - 1
    if request.session['currMonth'] < 1:
        request.session['currYear']=request.session['currYear']-1
        request.session['currMonth']=12
    if request.session['currMonth'] > 12:
        request.session['currYear']=request.session['currYear']+1
        request.session['currMonth']=1
    return redirect('punch_admin')


def detail_admin(request):
    obj=Employee.objects.all()
    return render(request,'studentbook/AdminDetail.html',{'obj':obj})

def addemployee(request):
    if request.method =='POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
    form=EmployeeForm()
    return render(request, 'studentbook/AddEmployee.html', {'form': form})

def checkin(request):
    pk = request.session['empid']
    if request.POST:
        count=Punch.objects.filter(empid=pk,date=datetime.now().date()).count()
        if count==0:
            user_obj = Employee.objects.get(empid=pk)
            punchin = datetime.now().time()
            date = datetime.now().date()
            empid = request.session['empid']
            obj = Punch(punchin=punchin, date=date, empid=user_obj)
            obj.save()
        else:
            Punch.objects.filter(empid=pk,date=datetime.now().date()).update(punchout=datetime.now().time())
        return redirect('punch')

