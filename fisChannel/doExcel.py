from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import models
import xlrd#处理excel
import os#拼凑excel文件的地址
import socket# 获取ip地址




def getIp(tongdaoN):
    ip = ''
    if tongdaoN[0] == 'K':
        ip = '这是一个spool'
    else:
        try:
            ip = socket.gethostbyname(tongdaoN)
        except Exception as e:
            ip = str(e)
        else:
            pass
        finally:
            pass
        return ip


def excel_table_byIndex(fileName, byIndex=0):
    data_excel = ''
    try:
        data_excel = xlrd.open_workbook(fileName)
    except Exception as e:
        print('open_workbook函数打印的异常信息' + str(e))


    # for item in data_excel.sheets():
    #     print(item)#每一行是一个对象<xlrd.sheet.Sheet object at 0x00000000011883C8>
    how_many_sheets_in_the_table = len(data_excel.sheets())
    # print("excel中有多少个table？  答案%d个 " %how_many_sheets_in_the_table)
    table = data_excel.sheets()[byIndex]
    # print(table.name)# exel表格中指定sheet的具体名字

    nrows = table.nrows#行数
    # ncols = table.ncols#列数
    # print(nrows,ncols)# 8 行 7 列  到目前为止，代码工作的很好

    #获取table中每一行的值,
    rows = list()
    db_lists = list()
    for row in range(4, nrows):#这里设置从sheet的第多少行开始获取数据
        list_of_row = table.row_values(row)#m每一行的内容，放入一个列表中
        # print(list_of_row)
        rows.append(list_of_row)



        tongdaoN = list_of_row[1][:4]
        ip = getIp(tongdaoN)
        tongdaoFull = list_of_row[1]
        description = list_of_row[2]
        sheetName = table.name
        instance = 'A33F22C5'#注意这里是要修改的地方
        remarks = list_of_row[8]

        l = [tongdaoN,ip,tongdaoFull,description,sheetName,instance,remarks]
        # print(l)
        db_lists.append(l)

        if models.tongdao.objects.filter(tongdaoFull=tongdaoFull):
            pass
        else:
            models.tongdao.objects.create(
                    tongdaoN = tongdaoN,
                    ip = ip,
                    tongdaoFull = tongdaoFull,
                    description = description,
                    sheetName = sheetName,
                    instance = instance,
                    remarks = remarks,
                    tongdao_type_id = 0,

                )
            # print('把通道%s写入数据库' % tongdaoN)

    return (rows, db_lists)#都有哪些行被读取了，发送到前台去看看

def insert2db(request):
    if request.method == "GET":
        # os.path.dirname(os.path.realpath(__file__))#当前文件的所在的文件夹
        # os.path.realpath(__file__)#当前文件的真实路径

        fileName = os.path.join(\
                os.path.dirname(os.path.realpath(__file__)), '123.xlsx')
        (rows, db_lists)= excel_table_byIndex(fileName=fileName, byIndex=1)#注意这里是要修改的地方
        return render(request,"insert2db.html", {"rows":rows,"db_lists":db_lists})