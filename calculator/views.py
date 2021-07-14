from django.shortcuts import render


def index(request):

    return render(request, 'index.html')


def calc(request):

    val1 = int(request.POST['val1'])

    val2 = int(request.POST['val2'])

    answer = val1 ** val2

    context = {

        'answer': answer,

    }

    return render(request, 'index.html', context)