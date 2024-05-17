nohup python phenomena_analysis.py --culture Korean &
nohup python phenomena_analysis.py --culture Portuguese &
nohup python phenomena_analysis.py --culture Spanish &
nohup python phenomena_analysis.py --culture Turkish &

nohup python phenomena_analysis.py --culture Arabic &
nohup python phenomena_analysis.py --culture Bengali &
nohup python phenomena_analysis.py --culture Chinese &
nohup python phenomena_analysis.py --culture Germany &


sleep 7200
nohup python main.py --culture Arabic --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 1000 &
nohup python main.py --culture Bengali --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 1000 &
nohup python main.py --culture Germany --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 1000 &

nohup python main.py --culture Arabic --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 750 &
nohup python main.py --culture Bengali --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 750 &
nohup python main.py --culture Germany --v v1 --data_type origin --cur_model gpt-3.5-turbo-0613 --g_num 750 &

nohup python main_cross.py --culture Arabic --cur_model gpt-3.5-turbo-0613 --g_num 1000 > gender.out &
nohup python main_cross.py --culture Bengali --cur_model gpt-3.5-turbo-0613 --g_num 1000 > gender.out &
nohup python main_cross.py --culture Germany --cur_model gpt-3.5-turbo-0613 --g_num 1000 > gender.out &

sleep 7200
nohup python main_cross.py --culture Arabic --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &
nohup python main_cross.py --culture Bengali --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &
nohup python main_cross.py --culture Germany --cur_model gpt-3.5-turbo-0613 --g_num 500 > gender.out &
nohup python main_cross.py --culture Arabic --cur_model gpt-3.5-turbo-0613 --g_num 750 > gender.out &
nohup python main_cross.py --culture Bengali --cur_model gpt-3.5-turbo-0613 --g_num 750 > gender.out &
nohup python main_cross.py --culture Germany --cur_model gpt-3.5-turbo-0613 --g_num 750 > gender.out &

nohup python directly_generation.py --culture Chinese --data_type specific --new_path data/Chinese/specific/new_test.jsonl &
nohup python directly_generation.py --culture Korean --data_type specific --new_path data/Korean/specific/new_test.jsonl &
nohup python directly_generation.py --culture Turkish --data_type specific --new_path data/Turkish/specific/new_test.jsonl &

nohup python directly_generation.py --culture Chinese &
nohup python directly_generation.py --culture Korean &
nohup python directly_generation.py --culture Turkish &