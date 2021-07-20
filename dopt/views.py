from django.shortcuts import render
from django.http import HttpResponse
import numpy as np

from .forms import UserForm
import re
from .Dopt import D_optimal_by_times

def Dopt_view(request):
    params = {'result1': '', 'result2': '', 'result3': '', 'form': None, 'matrix': ''}
    if request.method == 'POST':
        form = UserForm(request.POST)

        levels = [int(result) for result in re.findall('[0-9]+', request.POST['levels'])]
        num_of_exp = int(request.POST['number_of_experiments'])
        num_of_rand = int(request.POST['number_of_trials'])

        best_df, best_score, coverage = D_optimal_by_times(levels, num_of_exp, num_of_rand)

        request.session['best_df'] = best_df

        params['result0'] = '実験条件: '+ str(len(levels)) + '因子 (' + ', '.join([str(level) + '水準' for level in levels]) + ')'
        params['result1'] = '実施割合: '+ '{:.1f}'.format(100*num_of_exp/np.prod(levels)) + '% (一部実施' + str(num_of_exp) + '回 : 完全実施' + str(np.prod(levels)) + '回)'
        params['result2'] = 'D最適性: '+ '{:.1f}'.format(best_score*100) + '%'
        params['result3'] = '網羅率: '+ '{:.1f}'.format(coverage*100) + '%'
        params['result4'] = 'CSVダウンロード'
        params['form'] = form
        params['matrix'] = best_df.to_html()
    else:
        params['form'] = UserForm()
    return render(request, 'index.html', params)

def file_download_view(request):
    best_df = request.session['best_df']

    response = HttpResponse(content_type='text/csv; charset=shift-jis') #utf8')
    response['Content-Disposition'] = 'attachment; filename=result.csv'
    best_df.to_csv(path_or_buf=response, encoding='shift-jis') #utf-8-sig')

    return response