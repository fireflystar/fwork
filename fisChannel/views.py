from django.shortcuts import render,redirect
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from . import models
from .forms import *

# Create your views here.


def userlogin(request):
    msg = ''
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():#如果前端传来的数据合法，则执行下面的操作
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
                
            if username and password:
                user = authenticate(username=username, password=password)
                # print(type(user))#
                if (user is not None):
                    if user.is_active:
                        # print(username, password)
                        request.session['username'] = username#这里创建了session，执行了对数据库的写入
                        return render(request,"sou.html",{'username':username})
                else:
                    msg = '用户不存在 或 帐号密码不匹配'
                    uf = UserForm()
                    return render(request,"login.html",{'uf':uf, "msg":msg})
        else:#否则提示前台输入正确的内容
            msg = '用户名和密码都不能为空'
            uf = UserForm()
            return render(request,"login.html",{'uf':uf, "msg":msg})

    if request.method == "GET":
        username = request.session.get('username',False)
        if username:#加入已经登录了，则直接跳转
            return render(request,"sou.html",{'username':username})
        else:#加入没有登录，给用户登录窗口
            uf = UserForm()#POST请求以外的情况，给uf变量赋值
            return render(request,"login.html",{'uf':uf})


def logout(request):
    username = request.session.get('username',False)#获取一下session中的用户名
    if username:
        del request.session['username']#此函数 删除session 
        return HttpResponse('删除session，logout !')
    else:
        return HttpResponse('已经logout了，不用重新退出!')



def sou(request):
    msg = ''
    queryList = list()
    username = request.session.get('username',False)
    if username:
        if request.method == "GET":            
                return render(request,"sou.html",{'msg':msg,"username":username})
        if request.method == "POST":
            
            td = request.POST.get('tongdao', None).strip()#剥掉字符串两边的空格
            if not td:
                msg = "请先输入想要搜索的内容"
                return render(request,"sou.html",{'msg':msg})
            else:
                # queryList = models.tongdao.objects.filter(tongdaoN__icontains=td)#__icontains模糊查询，解决大小写混用的问题
                queryList = models.tongdao.objects.filter((
                     Q(ip__icontains=td) |
                     Q(tongdaoN__icontains= td)  |
                     Q(tongdaoFull__icontains= td)|
                     Q(description__icontains= td)|
                     Q(sheetName__icontains= td)|
                     Q(instance__icontains= td)|
                     Q(remarks__icontains= td)
                     )) 


                if queryList:
                    msg = "搜索提示：跟 %s 相关的结果一共有 %d 条" % (td,len(queryList))
                    return render(request,"sou.html",{
                            'queryList':queryList, #我想把结果给哪个模版，是随意的
                            'msg':msg,
                            'username':username})
                else:
                    msg = "搜索提示：找不到输入的 %s"% td
                    return render(request,"sou.html",{'msg':msg,
                        'td':td
                        })
    else:#session 不存在，这需要登录才行
        return HttpResponse("请先登录，然后才能使用搜索页面")



def soujinque(request):
    msg = ''
    queryList = list()
    username = request.session.get('username',False)
    if username:
        if request.method == "GET":            
                return render(request,"sou.html",{'msg':msg,"username":username})
        if request.method == "POST":
            
            td = request.POST.get('tongdao', None).strip()#剥掉字符串两边的空格
            if not td:
                msg = "请先输入想要搜索的内容"
                return render(request,"sou.html",{'msg':msg})
            else:
                # queryList = models.tongdao.objects.filter(tongdaoN__icontains=td)#__icontains模糊查询，解决大小写混用的问题
                queryList = models.tongdao.objects.filter((
                     Q(tongdaoN__icontains= td)
                     )) 


                if queryList:
                    msg = "搜索提示：跟%s 相关的结果一共有 %d 条" % (td, len(queryList))
                    return render(request,"sou.html",{
                            'queryList':queryList, #我想把结果给哪个模版，是随意的
                            'msg':msg,
                            'username':username})
                else:
                    msg = "搜索提示：找不到输入的 %s "% td
                    return render(request,"sou.html",{
                        'msg':msg
                        })
    else:#session 不存在，这需要登录才行
        return HttpResponse("请先登录，然后才能使用搜索页面")




import re
def add2db(request):
    error_list = list()
    username = request.session.get('username',False)
    if username:
        if request.method == "GET":
              return render(request,"add2db.html",{
                'username':username
                })

        if request.method == "POST":
            tongdao_name = request.POST.get('tongdao_name', None).strip()
            ip = request.POST.get('ip', None).strip()
            email_list = request.POST.get('email_list', None).strip()
            factory = request.POST.get('factory', None).strip()
            department = request.POST.get('department', None).strip()



            # 1  first 新建联系人对象
            #从字符串中提取邮件地址到 列表中
            mail_list = re.findall(r'(\w+@CSVW.COM|\w+@csvw.com)' ,email_list)#列表里都是邮件地址
            # print(mail_list)

            mailobj_list = list()#存在于某一次post请求中，不能再出现在第二次请求中
            for mail in mail_list:
                #已经存在了，就不再添加了
                mobj = models.contact.objects.filter(email = mail.lower() ).first()
                if mobj:
                    error_list.append("邮件地址 %s 已经存在于数据库中" % mail)
                    mailobj_list.append(mobj.contact_id)
                else:
                    #没有存在，则要添加，同时应该获取每次添加返回的数据库中某一行的id
                    mailObj = models.contact.objects.create(email = mail, email_lower=mail.lower() )
                    mailobj_list.append(mailObj.contact_id)
                    error_list.append("邮件地址 %s 被添加到数据库中" % mail)




            # 2 利用多对多的关系，将设备和联系人关联起来
            try:
                shebeiObj = models.shebei.objects.get(shebeiN = tongdao_name)
            except Exception as e:
                error_list.append("设备 %s 没有在数据库中" % tongdao_name)
                shebeiObj = models.shebei.objects.create(shebeiN = tongdao_name,
                            factory = factory,
                            department = department
                    )
                error_list.append("设备 %s 被添加到数据库中" % tongdao_name)
                shebeiObj.r.add(*mailobj_list)
                error_list.append("设备 和 邮件列表绑定完成" )
            else:
                # print('什么鬼')

                error_list.append("设备 %s 已经存在于数据库中" % tongdao_name)
                shebeiObj.r.clear()
                error_list.append("清空之前关联的邮件列表" )
                shebeiObj.r.add(*mailobj_list)
                error_list.append("重新关联邮件列表" )
            finally:
                pass



            # 3 建立通道和设备的关联
            try:
                tongdaoObj = models.tongdao.objects.get(tongdaoN = tongdao_name)
            except Exception as e:
                #不存在通道，则新建，并绑定 通道 和设备
                error_list.append("通道 %s 没有存在于数据库中" % tongdao_name)
                # print(str(e))
                tongdaoObj = models.tongdao.objects.create(tongdaoN = tongdao_name,
                    ip = ip,
                    sb_id = shebeiObj.shebei_id
                    )
                error_list.append("在数据库中新建通道 %s ，并且和上面的设备绑定" % tongdao_name)
            else:
                error_list.append("通道 %s 已经存在于数据库中" % tongdao_name)
                tongdaoObj.sb_id = shebeiObj.shebei_id
                tongdaoObj.save()
                error_list.append("通道已经存在，将上面的设备和通道绑定" )
            finally:
                pass
            

        return render(request,"add2db.html",{
                    "error_list":error_list
                    })

    return HttpResponse("请先登录，然后才能使用新增内容页面")







def save2db(request):
    error_list = list()
    username = request.session.get('username',False)
    if username:
        if request.method =="GET":
            return redirect("/sou/")

        if request.method == "POST":
            ip = request.POST.get('ip', None).strip()
            tongdaoN = request.POST.get('tongdaoN', None).strip()
            tongdaoFull = request.POST.get('tongdaoFull', None).strip()
            description = request.POST.get('description', None).strip()
            instance = request.POST.get('instance', None).strip()
            remarks = request.POST.get('remarks', None).strip()
            sheetName = request.POST.get('sheetName', None).strip()
            factory = request.POST.get('factory', None).strip()
            department = request.POST.get('department', None).strip()
            factory = request.POST.get('factory', None).strip()
            shebeRemarks = request.POST.get('shebeRemarks', None).strip()
            email_list = request.POST.get('email_list', None).strip()

            # print(ip,tongdaoN,tongdaoFull,description,instance,sheetName,factory,department,factory,shebeRemarks,
            #     email_list)


            # 1 提取邮件到列表
            mail_list = re.findall(r'(\w+@CSVW.COM|\w+@csvw.com)' ,email_list)
            mailobj_list = list()#需要获取联系人对象的列表，用于第2步
            for mail in mail_list:
                #已经存在了，就不再添加了
                # print('#1 是否来过这里')
                mobj = models.contact.objects.filter(email = mail.lower() ).first()
                if mobj:
                    error_list.append("#1 邮件地址 %s 已经存在于数据库中" % mail)
                    mailobj_list.append(mobj.contact_id)
                else:
                    #没有存在，则要添加，同时应该获取每次添加返回的数据库中某一行的id
                    mailObj = models.contact.objects.create(email = mail, email_lower = mail.lower())
                    mailobj_list.append(mailObj.contact_id)
                    error_list.append("#1 邮件地址 %s 被添加到数据库中" % mail)



            # 2 利用多对多的关系，将设备和联系人关联起来
            try:
                shebeiObj = models.shebei.objects.filter(shebeiN = tongdaoN).first()
                shebeiObj.department#不存在则触发异常
            except Exception as e:
                error_list.append("#2 查找设备%s，触发异常 %s" %( tongdaoN, str(e)))
                shebeiObj = models.shebei.objects.create(
                            shebeiN = tongdaoN,
                            factory = factory,
                            department = department,
                            shebeRemarks = shebeRemarks
                    )
                error_list.append("#2 设备 %s 被添加到数据库中" % tongdaoN)
                shebeiObj.r.add(*mailobj_list)
                error_list.append("设备 和 邮件列表绑定完成")

            else:
                error_list.append("#2 设备 %s 已经存在于数据库中" % tongdaoN)

                shebeiObj.factory = factory
                shebeiObj.department = department
                shebeiObj.shebeRemarks = shebeRemarks
                shebeiObj.save()
                error_list.append("#2 设备属性已更新")

                shebeiObj.r.clear()
                error_list.append("#2 清空之前关联的邮件列表")
                # print(mailobj_list[0],mailobj_list[1])#调试
                shebeiObj.r.add(*mailobj_list)
                error_list.append("#2 重新关联邮件列表")
                # for obj in shebeiObj.r.all():#调试
                #     print(obj.email)
            finally:
                pass



            # 3 建立通道和设备的关联

            # try:
            #     tongdaoObj = models.tongdao.objects.filter(tongdaoN = tongdaoN).first()
            #     tongdaoObj.tongdaoN#不存在则触发异常
            # except Exception as e:
            #     #不存在通道，则新建，并绑定 通道 和设备
            #     error_list.append("#3 在通道表中查找 %s ,触发异常 %s" % (tongdaoN, str(e) ) )
            #     tongdaoObj = models.tongdao.objects.create(
            #         ip = ip,
            #         tongdaoN = tongdaoN,
            #         tongdaoFull = tongdaoFull,
            #         description = description,
            #         sheetName = sheetName,
            #         instance = instance,
            #         remarks = remarks,
            #         sb_id = shebeiObj.shebei_id
            #         )
            #     error_list.append("#3 在通道表中新建通道 %s ，并且和上面的设备绑定" % tongdaoN)
            # else:
            tongdaoObjList = models.tongdao.objects.filter(tongdaoN = tongdaoN)
            if len(tongdaoObjList) > 0:
                for tongdaoObj in tongdaoObjList:
                    print(tongdaoObj.id)
                    error_list.append("#3 通道 %s 已经存在于数据库中" % tongdaoN)


                    tongdaoObj.ip = ip
                    tongdaoObj.tongdaoFull = tongdaoFull
                    tongdaoObj.description = description
                    tongdaoObj.sheetName = sheetName
                    tongdaoObj.instance = instance
                    tongdaoObj.remarks=remarks
                    
                    tongdaoObj.sb_id = shebeiObj.shebei_id#@@@@@@@@@@@@@@@@@@
                    tongdaoObj.save()
                    # print(tongdaoObj.id)
                    error_list.append("#3 通道信息已更新，将上面的设备和通道绑定" )
            else:
                #不存在通道，则新建，并绑定 通道 和设备
                error_list.append("#3 在通道表中查找 %s ,触发异常 %s" % (tongdaoN, str(e) ) )
                tongdaoObj = models.tongdao.objects.create(
                    ip = ip,
                    tongdaoN = tongdaoN,
                    tongdaoFull = tongdaoFull,
                    description = description,
                    sheetName = sheetName,
                    instance = instance,
                    remarks = remarks,
                    sb_id = shebeiObj.shebei_id
                    )
                error_list.append("#3 在通道表中新建通道 %s ，并且和上面的设备绑定" % tongdaoN)                

            return redirect('/sou/')
            return render(request,'debug.html',{
                "error_list":error_list
                })

    else:
        return HttpResponse("需要先登录")








def orm(request):
    q_list = models.tongdao.objects.all()
    s_list = list()
    for obj in q_list:
        if obj.sb_id:#假如这行的sb_id有值，则代表有过关联
            # obj.sb_id = None#那么清空这种关联
            # obj.save()#保存，生效，不保存则不生效
            s_list.append(obj)
    return render(request,'orm.html',{"s_list":s_list})
