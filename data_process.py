import jsonlines
import re, random, os, fire
import codecs, csv
import time

q_list = ['27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '122', '123', '124', '125', '126', '127', '128', '129', '132', '133', '134', '135', '136', '137', '138', '158', '159', '160', '161', '162', '169', '170', '196', '197', '198', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233']

def getResponse(prompt, engine, role=None, history=None):
    from openai import OpenAI

    if history != None:
        msg = history
    else:
        msg = []
    if role != None:
        msg.append({"role": "system", "content": f"Please act as {role}. Please answer directly."})
    msg.append({"role": "user", "content": prompt})

    client = OpenAI(api_key="xxx")

    output = None
    times = 0
    while output is None and times <= 10:
        try:
            times += 1  
            response = client.chat.completions.create(
                model=engine,
                messages=msg,
                temperature=0.7
                )
            output = response.choices[0].message.content
        except Exception as e:
            print(e)
            print('Retrying...')
            time.sleep(5)
    if times >= 10:
        print('Failed! Model Input: ', prompt)
        output = ''
  
    if "\"" in output:
        index = output.find("\"")
        output = output[index+1:]
        last_index = output.rfind("\"")
        if last_index != -1:
            output = output[:last_index]

    # history.append({"role": "user", "content": prompt})
    if role != None:
        history.append({"role": "system", "content": f"{role} said \"{output}\""})
    
    return output, history

def generateCountryAns(country, country_codes):
    num = 0
    f_num = 0
    item_list = []
    avg_item = {'B_COUNTRY': 'Avg', 'B_COUNTRY_ALPHA': ''}
    avg_first_item = {'B_COUNTRY': 'Avg_First', 'B_COUNTRY_ALPHA': ''}
    avg_last_item = {'B_COUNTRY': 'Avg_Last', 'B_COUNTRY_ALPHA': ''}
    with codecs.open('data/WVS_Cross-National_Wave_7_csv_v5_0.csv', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, skipinitialspace=True):
            if row['B_COUNTRY'] in country_codes:
                num += 1
                if num <= 1000:
                    f_num += 1
                item = {'B_COUNTRY': row['B_COUNTRY'], 'B_COUNTRY_ALPHA': row['B_COUNTRY_ALPHA']}
                for q in q_list:
                    k = 'Q' + q
                    item[k] = row[k]
                    if num <= 1000:
                        if k not in avg_item.keys():
                            avg_item[k] = abs(int(row[k]))
                            avg_first_item[k] = abs(int(row[k]))
                        else:
                            avg_item[k] += abs(int(row[k]))
                            avg_first_item[k] += abs(int(row[k]))
                    else:
                        if k not in avg_last_item.keys():
                            avg_last_item[k] = abs(int(row[k]))
                            if k not in avg_item.keys():
                                avg_item[k] = abs(int(row[k]))
                        else:
                            avg_item[k] += abs(int(row[k]))
                            avg_last_item[k] += abs(int(row[k]))

                print(item)
                item_list.append(item)
    f.close()
    print('Num: ', num)

    print('First: ', avg_first_item)
    print('Last: ', avg_last_item)
    print('F Num: ', f_num)

    for q in q_list:
        k = 'Q' + q
        avg_item[k] /= len(item_list)
        avg_first_item[k] /= f_num
        avg_last_item[k] /= len(item_list) - f_num

    dir_path = f"data/{country}"
    if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)

    with open(f'{dir_path}/{country}_new.csv', 'w', newline='') as f:
        data = item_list[0]
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        for item in item_list:
            writer.writerow(item)
        writer.writerow(avg_item)
        writer.writerow(avg_first_item)
        writer.writerow(avg_last_item)

def generateAnswerData(culture):
    ans_item = dict()
    ans_dict = {'Arabic': 'data/Arabic/Jordan.csv', 
                'Bengali': 'data/Bengali/Bangladesh.csv', 
                'Chinese': 'data/Chinese/China.csv',
                'Germany': 'data/Germany/Germany.csv',
                'Korean': 'data/Korean/South Korea.csv',
                'Portuguese': 'data/Portuguese/Brazil.csv',
                'Spanish': 'data/Spanish/Argentina.csv',
                'Turkish': 'data/Turkish/Turkey.csv'}
    ans_path = ans_dict[culture]
    with codecs.open(ans_path, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, skipinitialspace=True):
            if row['B_COUNTRY'] == 'Avg':
                ans_item = {'B_COUNTRY': row['B_COUNTRY'], 'B_COUNTRY_ALPHA': row['B_COUNTRY_ALPHA']}
                for q in q_list:
                    k = 'Q' + q
                    ans_item[k] = int(float(row[k]))
    f.close()
    
    option_dict = dict()
    with open("data/WVQ.jsonl", "r+", encoding="utf8") as f:
        for item in jsonlines.Reader(f):
            id = item['q_id']
            k = 'Q' + id
            option = item['option']
            new_option = []
            if len(option) > 0:
                options = option.split('.')
                for opt in options:
                    # print('Ori: ', opt)
                    opt = opt.strip()
                    if len(opt) <= 1: 
                        continue
                    if opt[-1].isdigit():
                        opt = opt[:-1]
                    if opt[-1].isdigit():
                        opt = opt[:-1]
                    opt = opt.strip()
                    new_option.append(opt)

            option_dict[k] = new_option
    
    special_list = ['Q122', 'Q123', 'Q124', 'Q125', 'Q126', 'Q127', 'Q128', 'Q129']
    new_ans_dict = dict()
    for k in ans_item.keys():
        if k in option_dict.keys():
            ans = abs(int(ans_item[k]))
            options = option_dict[k]
            print('options: ', options)
            print('ans: ', ans)
            if len(options) > 0:
                if k not in special_list:
                    if ans-1 >= len(options):
                        ans = len(options)
                    ans_text = options[ans-1]
                else:
                    if ans >= len(options):
                        ans = len(options)-1
                    ans_text = options[ans]
            else:
                ans_text = str(ans)
            new_ans_dict[k] = ans_text

    return new_ans_dict

def getPrompt(item, type):
    content = item['q_content']
    option = item['option']
    
    if type == 'wvq':
        nums = re.findall(r"\d+",option)
        if '?' in content:
            prompt = f"Give me the answer from {min(nums)} to {max(nums)}: {content} {option}. You can only choose one option."
        else:
            prompt = f"Give me the answer from {min(nums)} to {max(nums)}: Do you agree with {content}? {option}. You can only choose one option."
    else:
        if len(option) == 0:
            nums = re.findall(r"\d+", content)
            prompt = f"Give me the answer from {min(nums)} to {max(nums)}: {content}. You can only choose one option."
        else:
            nums = re.findall(r"\d+", option)
            prompt = f"Give me the answer from {min(nums)} to {max(nums)}: {content}\nOption: {option}. You can only choose one option."

    return prompt

def postProcess(culture):
    from config import culture_dict
    file_name = f''
    no_list = ["does not provide", "doesn't provide", "does not express", "doesn't express", "does not contain", "doesn't contain", "seem to contain", "seem to express", "does not convey", "doesn't convey"]
    state_list = ["statement", "stance", "viewpoint", "perspective", "idea", "belief", "assertion", "proposition"]
    with jsonlines.open(f"{file_name}_post.jsonl", mode='a') as writer:
        with open(f"{file_name}.jsonl", "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                new_opinion = item['new_opinion']
                origin_content = item['origin_content']
                attitude = item['attitude']
                words = new_opinion.split()
                no_tag = False
                if len(words) < 5:
                    continue
                for no_word in no_list:
                    if no_word in new_opinion:
                        no_tag = True
                        break
                if no_tag:
                    continue

                for state in state_list:
                    state = ' ' + state
                    if state in new_opinion and 'that' not in new_opinion and 'of' not in new_opinion:
                        index = new_opinion.find(state)
                        new_sentence = new_opinion[:index] + state + ' that ' + origin_content[:-1] + new_opinion[index+len(state):]
                        new_opinion = new_sentence
                        item['new_opinion'] = new_opinion
                
                if "according to" in item['new_opinion']:
                    index = item['new_opinion'].find(",")
                    item['new_opinion'] = item['new_opinion'][index+2:]
                
                people = culture_dict[culture]['people']
                boy = culture_dict[culture]['boy']
                girl = culture_dict[culture]['girl']

                item['new_opinion'] = item['new_opinion'].replace(f"the {people.lower()}'s", "My")
                item['new_opinion'] = item['new_opinion'].replace(f"the {people}'s", "My")
                item['new_opinion'] = item['new_opinion'].replace(f"the {people}", "I")
                item['new_opinion'] = item['new_opinion'].replace(f"the {people.lower()}", "I")
                item['new_opinion'] = item['new_opinion'].replace(f"The Arabians", "I")
                item['new_opinion'] = item['new_opinion'].replace(f"The {people}", "I")
                item['new_opinion'] = item['new_opinion'].replace(boy, "I")
                item['new_opinion'] = item['new_opinion'].replace(boy.lower(), "I")
                item['new_opinion'] = item['new_opinion'].replace(girl, "I")
                item['new_opinion'] = item['new_opinion'].replace(girl.lower(), "I")
                item['new_opinion'] = item['new_opinion'].replace("they", "I")
                item['new_opinion'] = item['new_opinion'].replace("They", "I")
                item['new_opinion'] = item['new_opinion'].replace("the speaker", "I")
                item['new_opinion'] = item['new_opinion'].replace("the people", "I")
                item['new_opinion'] = item['new_opinion'].replace("The people", "I")
                item['new_opinion'] = item['new_opinion'].replace("the person", "I")
                item['new_opinion'] = item['new_opinion'].replace("The person", "I")
                item['new_opinion'] = item['new_opinion'].replace("the individual ", "I ")

                if item['new_opinion'].startswith('he') or item['new_opinion'].startswith('He'):
                    item['new_opinion'] = item['new_opinion'].replace("He", "I", 1)
                    item['new_opinion'] = item['new_opinion'].replace("he", "I", 1)
                if item['new_opinion'].startswith('she') or item['new_opinion'].startswith('She'):
                    item['new_opinion'] = item['new_opinion'].replace("she", "I", 1)
                    item['new_opinion'] = item['new_opinion'].replace("She", "I", 1)

                item['new_opinion'] = item['new_opinion'].replace("I's", "my")

                writer.write(item)

def finetune():
    import time
    from openai import OpenAI
    client = OpenAI(api_key="xxx")

    client.files.create(
        file=open(f"data/Arabic/origin/Finetune/WVQ_v1__gpt-3.5-turbo-0613_500_post.jsonl", "rb"),
        purpose="fine-tune"
    )

    client.fine_tuning.jobs.create(
        training_file="xxx", 
        model="gpt-3.5-turbo-0613", 
        hyperparameters={
            "n_epochs": 3
        }
    )

def answerAug(country, type, ans_file=''):
    ans_item = dict()
    if type == 'wvq':
        with codecs.open(ans_file, encoding='utf-8-sig') as f:
            for row in csv.DictReader(f, skipinitialspace=True):
                if row['B_COUNTRY'] == 'Avg':
                    ans_item = {'B_COUNTRY': row['B_COUNTRY'], 'B_COUNTRY_ALPHA': row['B_COUNTRY_ALPHA']}
                    for q in q_list:
                        k = 'Q' + q
                        ans_item[k] = int(float(row[k]))
                    print('Ans: ', ans_item)
        f.close()

    dir_path = f"data/{country}/{type}/Finetune"
    if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)
    
    reason_dict = dict()
    with open(f"data/{country}/{type}/new/WVQ_cross_1000_post.jsonl", "r+", encoding="utf8") as f:
        for item in jsonlines.Reader(f):
            if type == 'wvq':
                id = item['q_id']
            else:
                id = item['origin_content']
            reason = item['new_opinion']
            if id in reason_dict.keys():
                reason_dict[id].append(reason)
            else:
                reason_dict[id] = [reason]

    if type == 'specific':
        data_file = f"xxx"
    else:
        data_file = "data/WVQ.jsonl"
    with jsonlines.open(f"{dir_path}/xxx", "a") as writer:
    # with jsonlines.open(f"{dir_path}/WVQ_{country}_multidemos_topic_3000.jsonl", "a") as writer:
        for t in range(20):
            with open(data_file, "r+", encoding="utf8") as f:
            # with open("data/new_WVQ_500.jsonl", "r+", encoding="utf8") as f:
                for item in jsonlines.Reader(f):
                    if type == 'wvq':
                        prompt = getPrompt(item, type)
                        id = 'Q' + item['q_id']
                        ans = ans_item['Q'+item['q_id']]
                        option = item['option']
                        if ans < 0:
                            ans = 0 - ans

                        ans_text = str(ans)
                    else:
                        prompt = item['messages'][1]['content']
                        id = item['messages'][1]['content']
                        ans_text = item['messages'][2]['content']

                    if id in reason_dict.keys():
                        reasons = reason_dict[id]
                        # i = random.randint(0, len(reasons)-1)
                        if t >= len(reasons):
                            continue
                        r = reasons[t]
                        ans_text += '. '
                        ans_text += r
                    
                    new_item = {"messages": [{"role": "system", "content": f"You are an {country} chatbot that know {country} very well."}, 
                                            {"role": "user", "content": prompt}, 
                                            {"role": "assistant", "content": ans_text}]}

                    writer.write(new_item)

def generateData4Llama(culture):
    from datasets import load_dataset
    def formatting_func(example):
        # text = f"### System: You are an {culture} chatbot that know {culture} very well. Question: {example['messages'][1]['content']}\n ### Answer: {example['messages'][2]['content']}"
        text = f"### System: You are an {culture} chatbot that know {culture} very well. Question: {example['messages'][1]['content']}\n ### Answer: {example['messages'][2]['content']}"
        return text
    
    path_name = 'xxx'
    dataset = load_dataset('json', data_files=f'{path_name}.jsonl', split='train')

    with jsonlines.open(f'{path_name}_llama.jsonl',mode='a') as writer:
        for item in dataset:
            text = formatting_func(item)
            new_item = {'text': text}
            writer.write(new_item)
    print('ok!')



# generateData4Llama('Chinese')
# postProcess('Arabic') 
# postProcess('Bengali') 
# postProcess('Germany') 
# postProcess('Spanish') 
# postProcess('Turkish') 
# QAformat()
# generateFintuneData('Arabic')
# finetune()
# answerAug('Arabic', 'origin', 'data/Arabic/Jordan_new.csv')
# answerAug('Bengali', 'specific', 'data/Bengali/Bangladesh.csv')
# answerAug('Chinese', 'origin', 'data/Chinese/China.csv')
# answerAug('Germany', 'specific', 'data/Germany/Germany.csv')

# answerAug('Korean', 'origin', 'data/Korean/South Korea.csv')
# answerAug('Portuguese', 'specific', 'data/Portuguese/Brazil.csv')
# answerAug('Spanish', 'specific', 'data/Spanish/Argentina.csv')
# answerAug('Turkish', 'origin', 'data/Turkish/Turkey.csv')

# generateCountryAns('Arabic', ['400', '818', '368', '504', '422', '434', '788'])
# generateCountryAns('Jordan', ['400'])
# selectData()