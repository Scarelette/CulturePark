import jsonlines
import time
import fire

def getResponse(prompt):
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

def run(culture):
    prompt_extend = 'Do the two paragraphs discuss same topic? Just answer with Yes, or No'
    prompt_understand = 'Does the paragraph reflect cross-cultural understanding? Just answer with Yes, or No'

    num = 0
    total = 0
    num_extend = 0
    num_understand = 0
    with jsonlines.open('results/phenomena_analysis.jsonl',mode='a') as writer:
        with open(f"xxx", "r+", encoding="utf8") as f:
            for item in jsonlines.Reader(f):
                num += 1
                if num < 31:
                    content = item['content']
                    # print(content)
                    last_d = content[1]
                    for d in content[2:]:
                        total += 1
                        cur_p = prompt_extend + '\nParagraph 1: ' + last_d + '\nParagraph 2: ' + d
                        # print('input: ', cur_p)
                        response = getResponse(cur_p)
                        print('Extend: ', response)
                        if 'yes' in response.lower():
                            num_extend += 1

                        cur_p = prompt_understand + '\nParagraph: ' + d
                        # print('input: ', cur_p)
                        response = getResponse(cur_p)
                        print('Undersatnd: ', response)
                        if 'yes' in response.lower():
                            num_understand += 1
                    
            extend_dict = {'culture': culture, 'total': total, 'extend': num_extend, 'understand': num_understand}             

            print('Total: ', total)
            print('Extend: ', num_extend)
            print('Undersatnd: ', num_understand)

            writer.write(extend_dict)

# analysis('Arabic')

# if __name__ == '__main__':
#     fire.Fire(run)  
                    
with open("results/phenomena_analysis.jsonl", "r+", encoding="utf8") as f:
    for item in jsonlines.Reader(f):
        print(item)
        print(item['total'])
        print(item['extend'])
        print(item['understand'])