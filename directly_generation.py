import time
import fire
import numpy as np
import random
import jsonlines
import os
from config import culture_dict

def getResponse(prompt, engine, culture):
    from openai import OpenAI

    msg = [{"role": "system", "content": f"You are an {culture} people chatbot that know {culture} people very well."},
            {"role": "user", "content": prompt}]

    msg.append({"role": "user", "content": prompt})

    client = OpenAI(api_key="xxx")

    output = None
    times = 0
    while output is None and times <= 10:
        try:
            times += 1  
            response = client.chat.completions.create(
                model=engine,
                max_tokens=256,
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

    return output


def run(culture, data_type='wvq', cur_model='gpt-3.5-turbo-0613'):

    path_dict = dict()
    path_dict['wvq'] = 'data/WVQ.jsonl'
    # path_dict['new'] = 'data/WVQ_new_2.jsonl'

    if data_type == 'wvq':
        from data_process import generateAnswerData
        ans_dict = generateAnswerData(culture)

    dir_path = f'data/{culture}/{data_type}/new'
    if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)
    num = 0
    with jsonlines.open(f'{dir_path}/{cur_model}_directly.jsonl',mode='a') as writer:
        with open(path_dict[data_type], "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                if data_type == 'wvq':
                    content = item['q_content']
                    k_id = 'Q' + item['q_id']
                    option = item['option']
                    if '?' not in content and data_type == 'wvq':
                        input = f"How do you think about \"{content}\"?"
                    else:
                        input = content

                    attitude = ans_dict[k_id]
                    original_opinion = content
                else:
                    content = item['messages'][1]['content']
                    attitude = item['messages'][2]['content']
                    index = content.find(':')
                    sentence = content[index+1:].strip()
                    index = content.find(', just say')
                    question = content[:index]
                    original_opinion = question + ': ' + sentence
                    input = original_opinion
                    k_id = str(num)
                    num += 1
                
                prompt = f'Question: {input}\nAnswer: {attitude}\nPlease list 10 reasons to support the answer and number them'
                response = getResponse(prompt, cur_model, 'Arabic')
                print('Res: ', response)

                res_list = response.split('\n')
                new_res_list = []
                for res in res_list:
                    if ':' in res:
                        index = res.find(':')
                        res = res[index+1:]
                    elif '.' in res:
                        index = res.find('.')
                        res = res[index+1:]

                    res = res.strip()
                    if len(res) > 0:
                        new_res_list.append(res)

                    for res in new_res_list[:10]:
                        generate_data = dict()
                        generate_data['q_id'] = k_id
                        generate_data['origin_content'] = content
                        generate_data['attitude'] = attitude
                        generate_data['new_opinion'] = res

                        print(generate_data)
                        writer.write(generate_data)
                    


if __name__ == '__main__':
    fire.Fire(run)  
                    