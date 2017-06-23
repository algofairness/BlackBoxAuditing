all: compas, bonus-indirect, sample

compas:
	python3 main.py ../input/compas_race/original_train.csv ../input/compas_race/original_test.csv ../input/compas_race/obscured_test.csv ../input/compas_race/summary.txt ../input/compas_race/feature_data.csv race 500 21 5 True 0.1 ../output/compas_race

bonus-indirect:
	python3 main.py ../input/bonus_indirect_race/original.csv ../input/bonus_indirect_race/original.csv ../input/bonus_indirect_race/obscured.csv ../input/bonus_indirect_race/summary.txt ../input/bonus_indirect_race/feature_data.csv Race 200 20 3 False 0.05 ../output/bonus_indirect_race

sample:
	python3 main.py ../input/sample/original.csv ../input/sample/original.csv ../input/sample/obscured.csv ../input/sample/summary.txt ../input/sample/feature_data.csv "Feature_A_(i)" 500 61 3 True 0.05 ../output/sample
