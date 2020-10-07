import numpy as np

import sys
sys.path.append('.')

import Simulator
import random

# 利用できる整数の個数をNに代入
N = Simulator.dim()

# 解の評価回数上限をmaxに代入
# (max+1)回以上，Simulator.evaluate(w)を呼び出すとエラー
max = Simulator.evalmax()



# ここから下を自分で開発

# ESのパラメータ
parents = 10 # 親の数
children = Simulator.dim() # 子の数
generation = max // parents # 最大世代数
change_bit = 1 # ビット反転数

# ランダムに新しい会を作成
w = np.random.randint(0, 2, size=(parents, N))
print(w) # check

# 設定した世代まで
for i in range(generation):
	values = [] # 評価値をまとめるための変数

	# 親（評価するデータ）の評価を求める
	for j in range(parents):

	# 解 w の評価値を求める
	# w は 長さNの１次元２値配列
		f = Simulator.evaluate(w[j])

		# 評価値のログ
		print((i+1), f, sep="\t") # check

		# 誤差0の解を発見できたら終了
		if(f==0): Simulator.finish()
		# 評価値を追加
		values.append(f)

	# valuse = [i for i range(0, parents)]
	keys = []
	for j in range(parents):
		keys.append(j)

	power = {} # 評価値からソートを行うための変数
	power.update(zip(keys, values))	# インデックスと評価値の辞書
	print("power is {}".format(power)) # check

	power_sorted = sorted(power.items(), key=lambda x:x[1]) # 評価値をソートする
	print("sorted power is {}".format(power_sorted)) # check

	leave_children = {} # 残す子供を作成
	# keyでソートしたときの上位N個
	for j in range(children):
	    leave_children[power_sorted[j][0]] = power_sorted[j][1]
	print("leave_children is {}".format(leave_children)) # check

	# インデックスを取得
	leave_children_list = []
	for j in leave_children.keys():
		leave_children_list.append(j)
	print("leave_children_list is {}".format(leave_children_list)) # check

	w_children = w.copy()
	for j in range(parents//children):
		for k in leave_children_list:
			w_children[j] = w[k]
			# print('w[k] is {}'.format(w[k])) # check
			w_children[j+parents//2] = w[k]
	print("w_children is \n{}".format(w_children))


	# change bit 1 to 0 , 0 to 1
	for j in range(parents):
		for k in range(change_bit):
			changeNumber = np.random.randint(0, N, size=(change_bit))
			# print("changeNumber is {}".format(changeNumber)) # check
			if w_children[j][changeNumber[k]] == 0: # check
				# print("change {} to ".format(w_children[j]))
				w_children[j][changeNumber[k]] = 1 # check
				# print("{}".format(w_children[j]))

			if w_children[j][changeNumber[k]] == 1: # check
				# print("change {} to ".format(w_children[j]))
				w_children[j][changeNumber[k]] = 0 # check
				# print("{}".format(w_children[j]))

	w = w_children.copy()


# 誤差0の解があるとは限らない
# あるとしても 発見できるとは限らない
# 発見できなかったときは 最後に呼び出す
Simulator.finish()


'''
備考

Simulator.py のグローバル変数を直接読み書きするのは禁止
	count
	wbest
	fbest

個々の整数の値を求めることは禁止
	「個々の整数の値を求める」ということは
	分割問題にしか通用しない解法を使う，ということ
	進化計算は，問題の知識を使わず，どの問題でも汎用的に
	解を求めることが可能
'''

