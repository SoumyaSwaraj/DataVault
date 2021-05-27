from django.db.models.base import Model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models, forms, script
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas as pd
import json
# Create your views here.


def home(request):
    return render(request, 'core/index.html')


def marketplace(request):
    dbs = models.DataSet.objects.all()
    if request.method == "POST":
        search = request.POST['search']
        if(search != ""):
            dbf = models.DataSet.objects.filter(title__contains=search)
            return render(request, 'core/market.html', {'datasets': dbf})
        return render()
    return render(request, 'core/market.html', {'datasets': dbs})


def sell(request):
    form = forms.DBInput()
    if request.method == 'POST':
        form = forms.DBInput(request.POST, request.FILES)
        if form.is_valid():
            fname = script.handle_db(request.FILES['file'], request.user.username)
            new_db = models.DataSet()
            new_db.title = form.cleaned_data['title']
            new_db.filename = fname
            new_db.owner = request.user
            new_db.cols_name = script.get_cols(fname)
            new_db.save()
            return redirect('detail-submit', pk=new_db.id)

        else:
            return HttpResponse("OOPS!")

    return render(request, 'core/sell.html', {"form": form})


def detail_submit(request, pk):
    dataset = models.DataSet.objects.filter(id=pk)[0]
    cols_name = list(dataset.cols_name.split(','))
    colsf = []
    for i in cols_name:
        colsf.append((i, i))
    colsf = tuple(colsf)
    form = forms.DataForm({'hello': 'nono'}, {'cols': colsf})
    if request.method == 'POST':
        form = forms.DataForm(request.POST, {'cols': colsf})
        if form.is_valid():
            dataset.description = form.cleaned_data['description']
            dataset.price = form.cleaned_data['price']
            str1 = ","

            dataset.reg_cols = str1.join(form.cleaned_data['reg_cols'])
            dataset.clas_cols = str1.join(form.cleaned_data['clas_cols'])

            dataset.graphsx = str1.join(form.cleaned_data['graph_x1'])
            dataset.graphsy = str1.join(form.cleaned_data['graph_y1'])

            # dataset.save()

            responses = script.run_me(dataset.reg_cols, dataset.clas_cols, dataset.filename)
            if responses.get('reg', False):
                dataset.reg_res = json.dumps(responses['reg'])
            if responses.get('clas', False):
                dataset.clas_res = json.dumps(responses['clas'])

            dataset.save()
            return redirect('home')
    return render(request, 'core/detail_submit.html', {'form': form, 'dataset': dataset})


def detail_dataset(request, id):
    dataset = models.DataSet.objects.filter(id=id)[0]
    thefile = 'upload/'+dataset.filename
    # graph_x = dataset.graphsx.split(',')
    # graph_y = dataset.graphsy.split(',')[0]
    # df = pd.read_csv('http://127.0.0.1:8000/static/upload/'+dataset.filename)
    graph3d = dataset.clas_res

    graph3d = json.loads(graph3d)

# new inserted
    graph3d_reg = dataset.clas_cols
    graph3d_reg = json.loads(graph3d_reg)

    # tables creation
    table = "<table>"
    table += "<tr>"
    for heading in dataset.clas_res[0]:
        table += "<th>"+heading+"</tr>"
    table += "</tr>"

    for row in dataset.clas_res:
        table += "<tr>"
        for i, value in enumerate(row):
            table += "<td>"+value+"</td>"
        table += "</tr>"
    table += "</table>"

    table_reg = "<table>"
    table_reg += "<tr>"
    for heading in dataset.clas_cols[0]:
        table_reg += "<th>"+heading+"</tr>"
    table_reg += "</tr>"

    for row in dataset.clas_cols:
        table_reg += "<tr>"
        for i, value in enumerate(row):
            table_reg += "<td>"+value+"</td>"
        table_reg += "</tr>"
    table_reg += "</table_reg>"

    return render(request, 'core/dataset.html', {"dataset": dataset, "thefile": thefile, 'graph3d': graph3d})


def contact(request):
    return render(request, 'core/contact.html')
