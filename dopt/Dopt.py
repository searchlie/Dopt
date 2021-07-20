import pandas as pd
import numpy as np

# 関数定義：グラム行列X'Xの行列式を求める
def gramian(matrix):
    return np.linalg.det(np.dot(matrix.T, matrix))

# 関数定義：各列の平均を0，ノルムを1にする
def autoscale(df):
    centered = df - df.mean()
    return centered/np.sqrt(np.square(centered).sum(axis=0))

# 関数定義：実験候補集合の一般項を再帰的に求める
def general_term(n, levels):
    if len(levels)==1:
        q, mod = divmod(n, levels[0])
        return [mod]
    q, mod = divmod(n, np.prod(levels[1:]))
    return [q] + general_term(mod, levels[1:])

# 関数定義：実験候補集合を与える
def candidate_set(levels):
    return [general_term(n,levels) for n in range(np.prod(levels))]

# 関数定義：２因子間の水準組み合わせの網羅率
def level_pair_coverage(df, levels):
    return appeared_level_pairs(df, levels)/all_level_pairs(levels)

# 関数定義：２因子間の水準組み合わせの総数
def all_level_pairs(levels):
    number_of_level_pairs = 0
    for i in range(len(levels)-1):
        for j in range(i+1, len(levels)):
            number_of_level_pairs += levels[i]*levels[j]
    return number_of_level_pairs

# 関数定義：２因子間の水準組み合わせの実現数
def appeared_level_pairs(df, levels):
    number_of_level_pairs = 0
    for i in range(len(levels)-1):
        for j in range(i+1, len(levels)):
            number_of_level_pairs += df.drop_duplicates(subset=[i, j]).shape[0]
    return number_of_level_pairs

# 関数定義：オフセット（定数項）の追加
def add_offset(df):
    num_of_row = df.shape[0]
    matrix = np.matrix(df)
    return np.concatenate([np.ones([num_of_row, 1])/np.sqrt(num_of_row), matrix], axis=1)
#### もしカテゴリカル変数　つまり非順序変数が入っている場合　One-Hotエンコーディングして制約条件を満たさない候補を外す　？

def D_optimal_by_times(levels, num_of_exp, num_of_rand):
    CandidateSet = pd.DataFrame(candidate_set(levels))
    CandidateSet = CandidateSet + np.int64(np.ones(CandidateSet.shape)) # 全要素に1を足して直交計画表と合わせる
    best_score = 0
    for i in range(num_of_rand):
        rand_indices = sorted(np.random.choice(CandidateSet.shape[0], size = num_of_exp, replace = False))
        rand_df = CandidateSet.iloc[rand_indices]
        current_score = gramian(add_offset(autoscale(rand_df)))
        if current_score > best_score:
            best_score = current_score
            best_df = rand_df.copy()
    coverage = level_pair_coverage(best_df, levels)
    best_df.index = ["実験 " + str(i+1) for i in range(num_of_exp)]
    best_df.columns = ["因子 " + str(i+1) for i in range(len(levels))]
    return best_df, best_score, coverage