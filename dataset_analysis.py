import jsonlines
import time

def getResponse(prompt, ):
    from openai import OpenAI

    msg = []

    msg.append({"role": "user", "content": prompt})

    client = OpenAI(api_key="xxx")

    output = None
    times = 0
    while output is None and times <= 10:
        try:
            times += 1  
            response = client.chat.completions.create(
                model='gpt-4-turbo-preview',
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

prompt = 'What does the paragraph contain? Just answer with Human belief, Norm or Custom?'
prompt_belief = 'Please classify the paragraph. Just answer with Religious Beliefs, Political Beliefs, Social Beliefs, Economic Beliefs, Moral and Ethical Beliefs, or Scientific Beliefs'
prompt_norm = 'Please classify the paragraph. Just answer with Descriptive Norms, Injunctive Norms, Prescriptive Norms, Proscriptive Norms, Legal Norms, or Traditional Norms'
prompt_custom = 'Please classify the paragraph. Just answer with Social Customs, Religious Customs, Cultural Customs, Family Customs, Community Customs, or Economic Customs'

num = 0
res_dict = {'belief': 0, 'norm': 0, 'custom': 0}
belief_dict = {'religious': 0, 'political': 0, 'social': 0, 'economic': 0, 'ethical': 0, 'scientific': 0}
norm_dict = {'descriptive': 0, 'injunctive': 0, 'prescriptive': 0, 'proscriptive': 0, 'legal': 0, 'traditional': 0}
custom_dict = {'social': 0, 'religious': 0, 'cultural': 0, 'family': 0, 'community': 0, 'economic': 0}
total = 0
with open("data/Arabic/Arabic_conversation.jsonl", "r+", encoding="utf8") as f:
    for item in jsonlines.Reader(f):
        num += 1
        if num < 51:
            content = item['content']
            # print(content)
            for d in content[1:]:
                total += 1
                cur_p = prompt + '\nParagraph: ' + d
                # print('input: ', cur_p)
                response = getResponse(cur_p)
                print(response)
                if 'belief' in response.lower():
                    res_dict['belief'] += 1
                    cur_p = prompt_belief + '\nParagraph: ' + d
                    response = getResponse(cur_p)
                    print(response)
                    for key in belief_dict.keys():
                        if key in response.lower():
                            belief_dict[key] += 1
                            break
                elif 'norm' in response.lower():
                    res_dict['norm'] += 1
                    cur_p = prompt_norm + '\nParagraph: ' + d
                    response = getResponse(cur_p)
                    print(response)
                    for key in norm_dict.keys():
                        if key in response.lower():
                            norm_dict[key] += 1
                            break
                elif 'custom' in response.lower():
                    res_dict['custom'] += 1
                    cur_p = prompt_norm + '\nParagraph: ' + d
                    response = getResponse(cur_p)
                    print(response)
                    for key in custom_dict.keys():
                        if key in response.lower():
                            custom_dict[key] += 1
                            break

print('Total: ', total)
print(res_dict)
print(belief_dict)
print(norm_dict)
print(custom_dict)