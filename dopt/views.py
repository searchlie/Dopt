from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pandas as pd

from .forms import UserForm
import re
from .Dopt import D_optimal_by_times, binom_np

def Dopt_view(request):
    params = {'form': None}
    if request.method == 'POST':
        form = UserForm(request.POST)

        levels = [int(result) for result in re.findall('[0-9]+', request.POST['levels'])]
        num_of_exp = int(request.POST['number_of_experiments'])
        num_of_rand = int(request.POST['number_of_trials'])

        best_df, best_score, coverage = D_optimal_by_times(levels, num_of_exp, num_of_rand)

        #request.session['best_df'] = best_df
        request.session['best_df'] = best_df.to_json()

        params['exp_condition'] = '実験条件: '+ str(len(levels)) + '因子 (' + ', '.join([str(level) + '水準' for level in levels]) + ')'
        params['doptimality'] = 'D最適性: '+ '{:.1f}'.format(best_score*100) + '%'
        num_of_candidates = np.prod(levels)
        params['exp_ratio'] = '実施率: '+ '{:.1f}'.format(100*num_of_exp/num_of_candidates) + '% (一部実施要因計画' + str(num_of_exp) + '回 / 完全実施要因計画' + str(num_of_candidates) + '回)'
        all_combi = int(binom_np(num_of_candidates, num_of_exp))
        params['combi_ratio'] = '探索率: '+ '{:.1f}'.format(100*num_of_rand/all_combi) + '% (探索組み合わせ' + str(num_of_rand) + '通り / 全組み合わせ' + str(all_combi) + '通り)'
        params['coverage'] = '網羅率: '+ '{:.1f}'.format(coverage*100) + '%'
        params['download'] = 'CSVダウンロード'
        params['form'] = form
        params['matrix'] = best_df.to_html()
    else:
        params['form'] = UserForm()
    return render(request, 'index.html', params)

def file_download_view(request):
    best_df = pd.read_json(request.session['best_df'])
    response = HttpResponse(content_type='text/csv; charset=shift-jis') #utf8')
    response['Content-Disposition'] = 'attachment; filename=dopt_' + str(best_df.shape[1]) + '-factors_' + str(best_df.shape[0]) + '-experiments' + '.csv'
    best_df.to_csv(path_or_buf=response, encoding='shift-jis') #utf-8-sig')

    return response