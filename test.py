import jsonlines
import openpyxl


culture_list = ['Arabic', 'Bengali', 'Chinese', 'Germany', 'Korean', 'Portuguese', 'Spanish', 'Turkish']

list_1 = []
list_2 = []
list_3 = []

for c in culture_list:
    # print('Culture: ', c)
    cur_dict = dict()
    with open("results/hofstede.jsonl", "r+", encoding="utf8") as f:
        for item in jsonlines.Reader(f):
            culture = item['culture']
            engine = item['engine']
            distance = item['distance']
            # print(engine)
            if culture != c:
                continue
            else:
                if engine == None:
                    cur_dict['ours'] = distance
                elif '4' in engine:
                    cur_dict['gpt-3.5'] = distance
                else:
                    cur_dict['gpt-4'] = distance

    # print(cur_dict['gpt-3.5'])
    # print(cur_dict['gpt-4'])
    # print(cur_dict['ours'])
    list_1.append(cur_dict['gpt-3.5'])
    list_2.append(cur_dict['gpt-4'])
    list_3.append(cur_dict['ours'])


print(list_1)
print(list_2)
print(list_3)