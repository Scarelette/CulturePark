from config import vsm13_data
import fire, time
import re, math
import codecs, csv
from config import model_dict
import jsonlines

def getResponse(prompt, engine, culture):
    from openai import OpenAI

    msg = []
    msg.append({"role": "user", "content": prompt})

    msg = [
            {"role": "system", "content": f"You are an {culture} chatbot that know {culture} very well."},
            {"role": "user", "content": prompt}
        ]

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
    
    return output

def computeMetrics(ans_list):
    pdi = 35 * (ans_list[7-1] - ans_list[2-1]) + 25 * (ans_list[20-1] - ans_list[23-1])
    idv = 35 * (ans_list[4-1] - ans_list[1-1]) + 35 * (ans_list[9-1] - ans_list[6-1])
    mas = 35 * (ans_list[5-1] - ans_list[3-1]) + 25 * (ans_list[8-1] - ans_list[10-1])
    uai = 40 * (ans_list[18-1] - ans_list[15-1]) + 25 * (ans_list[21-1] - ans_list[24-1])
    lto = 40 * (ans_list[13-1] - ans_list[14-1]) + 25 * (ans_list[19-1] - ans_list[22-1])
    ivr = 35 * (ans_list[12-1] - ans_list[11-1]) + 40 * (ans_list[17-1] - ans_list[16-1])

    return pdi+50, idv+50, mas+50, uai+50, lto+50, ivr+50

def run(culture, engine=None):
    country_dict = {'Arabic': 'Jordan', 'Bengali': 'Bangladesh', 'Chinese': 'China', 'Germany': 'Germany', 'Korean': 'Korea South', 'Portuguese': 'Brazil', 'Spanish': 'Argentina', 'Turkish': 'Turkey'}

    ans_dict = dict()
    with codecs.open(f'data/6-dimensions-for-website-2015-08-16.csv', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, skipinitialspace=True, delimiter=';'):
            country = row['country']
            pdi = row['pdi']
            idv = row['idv']
            mas = row['mas']
            uai = row['uai']
            lto = row['ltowvs']
            ivr = row['ivr']
            ans_dict[country] = {'pdi': pdi, 'idv': idv, 'mas': mas, 'uai': uai, 'lto': lto, 'ivr': ivr}
    
    cur_country = country_dict[culture]
    human_ans = ans_dict[cur_country]
    print('Human', human_ans)
    # model_dict = getModel(culture)
    test_model = model_dict[culture]
    ans_list = []
    for key in vsm13_data.keys():
        question = vsm13_data[key]
        if engine == None:
            response = getResponse(question, test_model, culture).strip()
        else:
            response = getResponse(question, engine, culture).strip()
        # print(response)
        try:
            number = re.findall(r'\d', response)[0]
            ans_list.append(int(number))
        except:
            ans_list.append(10)
        print('Output: ', number)
    pdi, idv, mas, uai, lto, ivr = computeMetrics(ans_list)
    cur_ans = {'pdi': pdi, 'idv': idv, 'mas': mas, 'uai': uai, 'lto': lto, 'ivr': ivr}
    print('Cur', pdi, idv, mas, uai, lto, ivr)

    missed_key = []
    human_point = []
    cur_point = []
    for key in human_ans.keys():
        v = human_ans[key]
        if '#' in v:
            missed_key.append(key)
        else:
            human_point.append(int(v))
    for key in cur_ans.keys():
        v = cur_ans[key]
        if key not in missed_key:
            cur_point.append(v)
    
    distance = math.sqrt(sum([(x - y) ** 2 for x, y in zip(human_point, cur_point)]))

    print('Dis: ', distance)

    with jsonlines.open(f'results/hofstede.jsonl',mode='a') as writer:
        cur_dict = {'culture': culture, 'engine': engine, 'distance': distance}
        writer.write(cur_dict)


if __name__ == '__main__':
    fire.Fire(run)  