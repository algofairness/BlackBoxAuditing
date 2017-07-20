all: compas, bonus-indirect, sample

compas:
	python3 main.py compas_race/original_train.csv compas_race/original_test.csv compas_race/obscured_test.csv compas_race/summary.txt compas_race/feature_data.csv race 500 21 5 True 0.1 find_contexts_results/compas_race

bonus-indirect:
	python3 main.py bonus_indirect_race/original.csv bonus_indirect_race/original.csv bonus_indirect_race/obscured.csv bonus_indirect_race/summary.txt bonus_indirect_race/feature_data.csv Race 200 20 3 False 0.05 find_contexts_results/bonus_indirect_race

sample:
	python3 main.py sample/original.csv sample/original.csv sample/obscured.csv sample/summary.txt sample/feature_data.csv "Feature_A_(i)" 500 61 3 True 0.05 find_contexts_results/sample
