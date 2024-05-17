sleep 10800
nohup python main_ablation_verify.py --culture Korean --v v1 --new_path data/Korean/origin/new/WVQ_v1__gpt-4_ablation_1.jsonl &
nohup python main_ablation_verify.py --culture Korean --v v1 --data_type specific --new_path data/Korean/specific/new/WVQ_v1_test.jsonl_gpt-4_ablation_1_sub.jsonl &

nohup python main.py --culture Bengali --v v1 --data_type origin &
nohup python main.py --culture Turkish --v v1 --data_type specific --new_path data/Turkish/specific/new_test_2.jsonl &
nohup python main.py --culture Turkish --v v1 --data_type specific --new_path data/Turkish/specific/new_test_3.jsonl &

sleep 18000
nohup python main_ablation_verify.py --culture Turkish --v v1 --new_path data/Turkish/origin/new/WVQ_v1__gpt-4_ablation_1.jsonl &
nohup python main_ablation_verify.py --culture Turkish --v v1 --data_type specific --new_path data/Turkish/specific/new/WVQ_v1_gpt-4_ablation_1_1.jsonl &
nohup python main_ablation_verify.py --culture Turkish --v v1 --data_type specific --new_path data/Turkish/specific/new/WVQ_v1_gpt-4_ablation_1_2.jsonl &
nohup python main_ablation_verify.py --culture Turkish --v v1 --data_type specific --new_path data/Turkish/specific/new/WVQ_v1_gpt-4_ablation_1_3.jsonl &

# nohup python main_2.py --culture Turkish --v v1 --data_type origin &
# nohup python main_2.py --culture Turkish --v v1 --data_type specific --new_path data/Turkish/specific/new_test.jsonl &

nohup python diverse_gain.py > diverse.out &
nohup python diverse_gain.py --new_data_file data/Bengali/origin/Finetune/WVQ_v1_post.jsonl --origin_data_file data/Bengali/origin/Finetune/WVQ_Bengali_50.jsonl > diverse.out &
nohup python diverse_gain.py --new_data_file data/Chinese/origin/Finetune/WVQ_v1.jsonl --origin_data_file data/Chinese/origin/Finetune/new_test.jsonl > diverse.out &
nohup python diverse_gain.py --new_data_file data/Germany/origin/Finetune/WVQ_v1.jsonl --origin_data_file data/Germany/origin/Finetune/WVQ_Germany_50.jsonl > diverse.out &
nohup python diverse_gain.py --new_data_file data/Korean/origin/Finetune/WVQ_v1.jsonl --origin_data_file data/Korean/origin/Finetune/WVQ_Korean_50.jsonl > diverse.out &
nohup python diverse_gain.py --new_data_file data/Portuguese/origin/Finetune/WVQ_v1.jsonl --origin_data_file data/Portuguese/origin/Finetune/WVQ_Portuguese_50.jsonl > diverse.out &
nohup python diverse_gain.py --new_data_file data/Spanish/origin/Finetune/WVQ_v1.jsonl --origin_data_file data/Spanish/origin/Finetune/WVQ_Spanish_50.jsonl > diverse.out &
nohup python diverse_gain.py --new_data_file data/Turkish/origin/Finetune/WVQ_v1.jsonl --origin_data_file data/Turkish/origin/Finetune/WVQ_Turkey_50.jsonl > diverse.out &


nohup python hofstede_test.py --culture Arabic --engine gpt-4 &
nohup python hofstede_test.py --culture Bengali --engine gpt-4 &
nohup python hofstede_test.py --culture Chinese --engine gpt-4 &
nohup python hofstede_test.py --culture Germany --engine gpt-4 &
nohup python hofstede_test.py --culture Korean --engine gpt-4 &
nohup python hofstede_test.py --culture Portuguese --engine gpt-4 &
nohup python hofstede_test.py --culture Spanish --engine gpt-4 &
nohup python hofstede_test.py --culture Turkish --engine gpt-4 &


nohup python main.py --culture Bengali --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 > cost.out &
nohup python main.py --culture Germany --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 &
nohup python main.py --culture Korean --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 &
nohup python main.py --culture Portuguese --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 &
nohup python main.py --culture Korean --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Korean/specific/new_test.jsonl > specific.out &
nohup python main.py --culture Turkish --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Turkish/specific/new_test.jsonl > specific.out &


nohup python main.py --culture Arabic --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 &
nohup python main.py --culture Chinese --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 &

nohup python main.py --culture Turkish --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Turkish/specific/new_test_2.jsonl > specific.out &


nohup python main.py --culture Arabic --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Arabic/specific/new_test_3.jsonl > specific.out &
nohup python main.py --culture Arabic --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Arabic/specific/new_test_2.jsonl > specific.out &

nohup python main.py --culture Chinese --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Chinese/specific/new_test_1.jsonl > specific.out &
nohup python main.py --culture Chinese --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Chinese/specific/new_test_2.jsonl > specific.out &
nohup python main.py --culture Chinese --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Chinese/specific/new_test_3.jsonl > specific.out &

nohup python main.py --culture Germany --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Germany/specific/new_test_2.jsonl > specific.out &

nohup python main.py --culture Portuguese --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Portuguese/specific/new_test_3.jsonl > specific.out &
nohup python main.py --culture Spanish --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Spanish/specific/new_test_3.jsonl > specific.out &
nohup python main.py --culture Spanish --v v1 --data_type specific --cur_model gpt-3.5-turbo-0613 --new_path data/Spanish/specific/new_test_2.jsonl > specific.out &


nohup python main_cross.py --culture Arabic --v v2 --cur_model gpt-3.5-turbo-0613 --g_num 500 > crossin.out &
nohup python main_cross.py --culture Bengali --cur_model gpt-3.5-turbo-0613 --g_num 500 > crossin.out &
nohup python main_cross.py --culture Germany --cur_model gpt-3.5-turbo-0613 --g_num 500 > crossin.out &
nohup python main_cross.py --culture Arabic --cur_model gpt-3.5-turbo-0613 --g_num 750 > crossin.out &
nohup python main_cross.py --culture Bengali --cur_model gpt-3.5-turbo-0613 --g_num 750 > crossin.out &
nohup python main_cross.py --culture Germany --cur_model gpt-3.5-turbo-0613 --g_num 750 > crossin.out &
nohup python main_cross.py --culture Arabic --cur_model gpt-3.5-turbo-0613 --g_num 1000 > crossin.out &
nohup python main_cross.py --culture Bengali --cur_model gpt-3.5-turbo-0613 --g_num 1000 > crossin.out &
nohup python main_cross.py --culture Germany --cur_model gpt-3.5-turbo-0613 --g_num 1000 > crossin.out &


nohup python main.py --culture Arabic --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 750 &
nohup python main.py --culture Bengali --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 750 &
nohup python main.py --culture Germany --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 750 &

nohup python main.py --culture Arabic --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 1000 &
nohup python main.py --culture Bengali --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 1000 &
nohup python main.py --culture Germany --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 1000 &

nohup python main_cross.py --culture Arabic --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &
nohup python main_cross.py --culture Bengali --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &
nohup python main_cross.py --culture Germany --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &
nohup python main_cross.py --culture Arabic --cur_model gpt-3.5-turbo-0613 --g_num 750 > gender.out &
nohup python main_cross.py --culture Bengali --cur_model gpt-3.5-turbo-0613 --g_num 750 > gender.out &
nohup python main_cross.py --culture Germany --cur_model gpt-3.5-turbo-0613 --g_num 750 > gender.out &
nohup python main_cross.py --culture Arabic --cur_model gpt-3.5-turbo-0613 --g_num 1000 > gender.out &
nohup python main_cross.py --culture Bengali --cur_model gpt-3.5-turbo-0613 --g_num 1000 > gender.out &
nohup python main_cross.py --culture Germany --cur_model gpt-3.5-turbo-0613 --g_num 1000 > gender.out &


nohup python main_cross.py --culture Chinese --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &
nohup python main_cross.py --culture Korean --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &
nohup python main_cross.py --culture Portuguese --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &
nohup python main_cross.py --culture Spanish --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &
nohup python main_cross.py --culture Turkish --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &