from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from employee.models import Employee, Attendance, Notice, workAssignments, Requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
@login_required(login_url='/')
def dashboard(request):
    info = Employee.objects.filter(eID=request.user.username)
    return render(request,"employee/index.html",{'info':info})

@login_required(login_url='/')
def attendance(request):
    attendance=Attendance.objects.filter(eId=request.user.username)
    return render(request,"employee/attendance.html",{"info":attendance})

@login_required(login_url='/')
def notice(request):
    notices  = Notice.objects.all()
    return render(request,"employee/notice.html",{"notices":notices})

@login_required(login_url='/')
def noticedetail(request,id):
    noticedetail = Notice.objects.get(Id=id)
    return render(request,"employee/noticedetail.html",{"noticedetail":noticedetail})

@login_required(login_url='/')
def assignWork(request):
    context={}
    initialData = {
        "assignerId" : request.user.username,
    }
    flag = ""
    form = workform(request.POST or None, initial=initialData)
    if form.is_valid():
        currentTaskerId = request.POST["taskerId"]
        currentUserId = request.user.username
        if currentTaskerId == currentUserId:
            flag="Invalid ID Selected..."
        else:
            flag = "Work Assigned Successfully!!"
            form.save()

    context['form']=form
    context['flag'] = flag
    return render(request,"employee/workassign.html",context)

@login_required(login_url='/')
def mywork(request):
    work = workAssignments.objects.filter(taskerId=request.user.username)
    return render(request,"employee/mywork.html",{"work":work})

@login_required(login_url='/')
def workdetails(request,wid):
    workdetails = get_object_or_404(workAssignments, id=wid)
    if request.user.username not in (workdetails.assignerId_id, workdetails.taskerId_id):
        raise PermissionDenied            # 403 - not assigner or tasker
    return render(request,"employee/workdetails.html",{"workdetails":workdetails})

@login_required(login_url='/')
def makeRequest(request):
    context={}
    initialData = {
        "requesterId" : request.user.username,
    }
    flag = ""
    requestForm = makeRequestForm(request.POST or None, initial=initialData)
    if request.method == 'POST':
        requestForm = makeRequestForm(request.POST)
        if requestForm.is_valid():
            currentRequesterId = request.POST["destinationEmployeeId"]
            currentUserId = request.user.username
            if currentRequesterId == currentUserId:
                flag="Invalid ID Selected..."
            else:
                flag="Request Submitted"
                requestForm.save()

    context['requestForm']=requestForm
    context['flag'] = flag
    return render(request,"employee/request.html",context)

@login_required(login_url='/')
def viewRequest(request):
    requests = Requests.objects.filter(destinationEmployeeId=request.user.username)
    return render(request,"employee/viewRequest.html",{"requests":requests})

@login_required(login_url='/')
def requestdetails(request,rid):
    requestdetail = get_object_or_404(Requests, id=rid)
    if request.user.username not in (requestdetail.requesterId_id, requestdetail.destinationEmployeeId_id):
        raise PermissionDenied            # 403 - not requester or recipient
    return render(request,"employee/requestdetails.html",{"requestdetail":requestdetail})

@login_required(login_url='/')
def assignedworklist(request):
    works = workAssignments.objects.filter(assignerId=request.user.username).all()
    return render(request,"employee/assignedworklist.html",{"works":works})

@login_required(login_url='/')
def deletework(request, wid):
    obj = get_object_or_404(workAssignments, id=wid)
    obj.delete()
    return render(request, "employee/assignedworklist.html")

@login_required(login_url='/')
def updatework(request,wid):
    work = get_object_or_404(workAssignments, id=wid)
    if work.assignerId_id != request.user.username:
        raise PermissionDenied            # 403 - only the assigner may edit
    form = workform(request.POST or None, instance=work)
    flag = ""
    if form.is_valid():
        currentTaskerId = request.POST["taskerId"]
        currentUserId = request.user.username
        if currentTaskerId == currentUserId:
            flag="Invalid ID Selected..."
        else:
            flag = "Work Updated Successfully!!"
            form.save()
    return render(request,"employee/updatework.html", {'currentWork': work, "filledForm": form, "flag":flag})