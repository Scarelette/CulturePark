import time
import fire
import numpy as np
import random
import jsonlines
import os
from config import culture_dict

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
  
    if "\"" in output:
        index = output.find("\"")
        output = output[index+1:]
        last_index = output.rfind("\"")
        if last_index != -1:
            output = output[:last_index]

    if role != None:
        history.append({"role": "system", "content": f"{role} said \"{output}\""})
    
    return output, history

def verifyData(seed_data, new_data):
    def getPrompt(seed_data, new_data):
        prompt = f"What's the relationship between the two opinion? Direct answer with Contradict, Entail or Irrelevant.\nOpinion 1: {seed_data}\nOpinion 2: {new_data}"
        return prompt
    
    input = getPrompt(seed_data, new_data)
    response, his = getResponse(input, 'gpt-4-turbo-preview')

    return response.strip()

def rewriteData(seed_data, new_data):
    def getPrompt(seed_data, new_data):
        prompt = f"Rewrite the sentence to make it conform to the original statement.\nOriginal statement: {seed_data}\nSentence: {new_data}"
        return prompt
    
    input = getPrompt(seed_data, new_data)
    response, his = getResponse(input, 'gpt-4-turbo-preview')

    return response.strip()

def get_embedding(text):
    from openai import OpenAI
    client = OpenAI(api_key="xxx")

    def normalize_l2(x):
        x = np.array(x)
        if x.ndim == 1:
            norm = np.linalg.norm(x)
            if norm == 0:
                return x
            return x / norm
        else:
            norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
            return np.where(norm == 0, x, x / norm)

    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    embedding = response.data[0].embedding
    cut_dim = embedding[:256]
    norm_dim = normalize_l2(cut_dim)

    return norm_dim

def clustering(matrix, n_clusters=10):
    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters = n_clusters, init='k-means++', random_state=42)
    kmeans.fit(matrix)
    # print(kmeans.labels_)

    return kmeans.labels_

def run(culture, v , data_type='wvq', cur_model='gpt-3.5-turbo-0613', g_num=500):
    
    people = culture_dict[culture]['people']
    boy = culture_dict[culture]['boy']
    girl = culture_dict[culture]['girl']

    path_dict = dict()
    path_dict['wvq'] = 'data/WVQ.jsonl'
    
    if data_type == 'wvq':
        from data_process import generateAnswerData
        ans_dict = generateAnswerData(culture)

    dir_path = f'data/{culture}/{data_type}/new'
    if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)
    num = 0
    with jsonlines.open(f'{dir_path}/WVQ_{v}_{cur_model}_coversation_{g_num}.jsonl',mode='a') as writer_c:
        with jsonlines.open(f'{dir_path}/WVQ_{v}_{cur_model}_{g_num}.jsonl',mode='a') as writer:
        #     with jsonlines.open(f'{dir_path}/WVQ_{v}_{name}_{cur_model}_ablation_1.jsonl',mode='a') as writer_1:
        #         with jsonlines.open(f'{dir_path}/WVQ_{v}_{name}_{cur_model}_ablation_verify.jsonl',mode='a') as writer_v:
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
                    

                    print('Origin Statement: ', content)
                    print('Attitude: ', attitude)

                    # Step 1: generate data
                    
                    if '?' not in content and data_type == 'wvq':
                        background = f"{boy} is a {people} boy and {girl} is a {people} girl. {boy} and {girl} {attitude} with the idea that {original_opinion}. All of their statements should conform to the thinking."
                        history = [{"role": "system", "content": background}]
                    elif (data_type == 'wvq' and len(option) == 0) or data_type == 'specific':
                        background = f"{boy} is a {people} boy and {girl} is a {people} girl. When asked {original_opinion}, {boy} and {girl} answered that {attitude}. All of their statements should conform to the thinking."
                        history = [{"role": "system", "content": background}]
                    else:
                        background = f"{boy} is a {people} boy and {girl} is a {people} girl. When asked {original_opinion}, Option: {option}, {boy} and {girl} answered that {attitude}. All of their statements should conform to the thinking."
                        history = [{"role": "system", "content": background}]

                    print('History: ', history)

                    conversation_dict = dict()
                    conversation_dict['culture'] = culture
                    conversation_dict['background'] = background
                    conversation_dict['content'] = []

                    # v1
                    if v == 'v1':
                        sys = input + "\nPlease provide your opinions and reasons."
                        response_1, history = getResponse(sys, cur_model, boy, history)
                        print(sys)
                        print(f'{boy}: ', response_1)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{boy}: ' + response_1)
                        sys = "What's your opinion? Please provide your reasons. Diverse opinions are welcome."
                        response_2, history = getResponse(sys, cur_model, girl, history)
                        print(sys)
                        print(f'{girl}: ', response_2)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{girl}: ' + response_2)

                        sys = "Can you provide more ideas on your culture to support your idea?"
                        response_1, history = getResponse(sys, cur_model, boy, history)
                        print(sys)
                        print(f'{boy}: ', response_1)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{boy}: ' + response_1)
                        sys = "What's your opinion? Can you provide more ideas on your culture to support your idea?"
                        response_2, history = getResponse(sys, cur_model, girl, history)
                        print(sys)
                        print(f'{girl}: ', response_2)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{girl}: ' + response_2)

                        sys = "Do you have more interesting ideas?"
                        response_1, history = getResponse(sys, cur_model, boy, history)
                        print(sys)
                        print(f'{boy}: ', response_1)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{boy}: ' + response_1)
                        sys = "Do you have more interesting ideas?"
                        response_2, history = getResponse(sys, cur_model, girl, history)
                        print(sys)
                        print(f'{girl}: ', response_2)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{girl}: ' + response_2)

                        sys = "Are there anything in your culture related to the problem talked before?"
                        response_1, history = getResponse(sys, cur_model, boy, history)
                        print(sys)
                        print(f'{boy}: ', response_1)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{boy}: ' + response_1)
                        sys = "What's your opinion?"
                        response_2, history = getResponse(sys, cur_model, girl, history)
                        print(sys)
                        print(f'{girl}: ', response_2)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{girl}: ' + response_2)

                        sys = "What's your opinion?"
                        response_1, history = getResponse(sys, cur_model, boy, history)
                        print(sys)
                        print(f'{boy}: ', response_1)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{boy}: ' + response_1)
                        sys = "Are there anything in your culture related to the problem talked before?"
                        response_2, history = getResponse(sys, cur_model, girl, history)
                        print(sys)
                        print(f'{girl}: ', response_2)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{girl}: ' + response_2)

                        sys = "What's your opinion? Please provide your reasons. Diverse opinions are welcome."
                        response_1, history = getResponse(sys, cur_model, boy, history)
                        print(sys)
                        print(f'{boy}: ', response_1)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{boy}: ' + response_1)
                        sys = "What's your opinion? Please provide your reasons. Diverse opinions are welcome."
                        response_2, history = getResponse(sys, cur_model, girl, history)
                        print(sys)
                        print(f'{girl}: ', response_2)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{girl}: ' + response_2)

                        sys = "Do you have some inspirations or ideas?"
                        response_1, history = getResponse(sys, cur_model, boy, history)
                        print(sys)
                        print(f'{boy}: ', response_1)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{boy}: ' + response_1)
                        sys = "Do you have some inspirations or ideas?"
                        response_2, history = getResponse(sys, cur_model, girl, history)
                        print(sys)
                        print(f'{girl}: ', response_2)
                        conversation_dict['content'].append('System: ' + sys)
                        conversation_dict['content'].append(f'{girl}: ' + response_2)
                    else:
                        # v2
                        response_1, history = getResponse(input + "\nPlease provide your opinions and reasons.", cur_model, boy, history)
                        print(input + "\nPlease provide your opinions and reasons.")
                        print(f'{boy}: ', response_1)
                        input = f'{boy}: ' + response_1
                        response_2, history = getResponse(input, cur_model, girl, history)
                        # print("What's your opinion? Please provide your reasons. Diverse opinions are welcome.")
                        print(f'{girl}: ', response_2)
                        input = f'{girl}: ' + response_2
                        response_1, history = getResponse(input, cur_model, boy, history)
                        # print("Can you provide more ideas on your culture to support your idea?")
                        print(f'{boy}: ', response_1)
                        input = f'{boy}: ' + response_1
                        response_2, history = getResponse(input, cur_model, girl, history)
                        # print("What's your opinion? Can you provide more ideas on your culture to support your idea?")
                        print(f'{girl}: ', response_2)
                        input = f'{girl}: ' + response_2
                        response_1, history = getResponse(input, cur_model, boy, history)
                        # print("Do you have more interesting ideas?")
                        print(f'{boy}: ', response_1)
                        input = f'{boy}: ' + response_1
                        response_2, history = getResponse(input, cur_model, girl, history)
                        # print("Do you have more interesting ideas?")
                        print(f'{girl}: ', response_2)
                        input = f'{girl}: ' + response_2
                        response_1, history = getResponse(input, cur_model, boy, history)
                        # print("Are there anything in your culture related to the problem talked before?")
                        print(f'{boy}: ', response_1)
                        input = f'{boy}: ' + response_1
                        response_2, history = getResponse(input, cur_model, girl, history)
                        # print("What's your opinion?")
                        print(f'{girl}: ', response_2)
                        input = f'{girl}: ' + response_2
                        response_1, history = getResponse(input, cur_model, boy, history)
                        # print("What's your opinion?")
                        print(f'{boy}: ', response_1)
                        input = f'{boy}: ' + response_1
                        response_2, history = getResponse(input, cur_model, girl, history)
                        # print("Are there anything in your culture related to the problem talked before?")
                        print(f'{girl}: ', response_2)
                        input = f'{girl}: ' + response_2
                        response_1, history = getResponse(input, cur_model, boy, history)
                        # print("What's your opinion? Please provide your reasons. Diverse opinions are welcome.")
                        print(f'{boy}: ', response_1)
                        input = f'{boy}: ' + response_1
                        response_2, history = getResponse(input, cur_model, girl, history)
                        # print("What's your opinion? Please provide your reasons. Diverse opinions are welcome.")
                        print(f'{girl}: ', response_2)
                        input = f'{girl}: ' + response_2
                        response_1, history = getResponse(input, cur_model, boy, history)
                        # print("Do you have some inspirations or ideas?")
                        print(f'{boy}: ', response_1)
                        input = f'{boy}: ' + response_1
                        response_2, history = getResponse(input, cur_model, girl, history)
                        # print("Do you have some inspirations or ideas?")
                        print(f'{girl}: ', response_2)

                    # print('His: ', history)

                    writer_c.write(conversation_dict)
                    
                    # Step 2: Extract opinions
                    opinion_list = []
                    
                    for statement in history:
                        if statement['role'] == 'system' and (f"{boy} said" in statement['content'] or f"{girl} said" in statement['content']):
                            index = statement['content'].find('\"')
                            sentence = statement['content'][index+1:]
                            sentence = sentence[:-1]
                    
                            input = f"Please extract opinions from the sentence, and number them. It's better not to use pronoun. The opinions are from the people: {sentence}"
                            extract_opinions, his = getResponse(input, "gpt-4-turbo-preview", None, None)
                            print("Extracted opinions: ", extract_opinions)
                            
                            items = extract_opinions.split('\n')
                            for item in items:
                                if 'not contain any' in item.lower():
                                    continue
                                item = item.strip()
                                index = item.find('.')
                                if index == 1 or index == 2:
                                    item = item[index+1:]
                                response = item.lower().strip()
                                opinion_list.append(response.strip())
                                print("Response 2: ", response)

                    # Step 3: Verify and filter data. Then remove redundancy.
                        # 1. verirfy 2. If contridict, rewrite 3. verify 4. If contridict, remove it
                        # 5. Remove redundancy. cluster and perserve {10}.
                        # Distribution
                    
                    for item in opinion_list:
                        generate_data = dict()
                        generate_data['q_id'] = k_id
                        generate_data['origin_content'] = content
                        generate_data['attitude'] = attitude
                        generate_data['new_opinion'] = item

                        print(generate_data)
                        # writer_1.write(generate_data)


                    if '?' not in content and data_type == 'wvq':
                        seed_data = f"The people {attitude} that {original_opinion}"
                    else:
                        seed_data = f"When asked {original_opinion}, the people answered that {attitude}"

                    final_opinion_list = []
                    embeddings = []
                    for opinion in opinion_list:
                        relationship = verifyData(seed_data, opinion)

                        print('Opinion: ', opinion)
                        print('Relation: ', relationship)

                        if 'contradict' in relationship.lower():
                            new_opinion = rewriteData(seed_data, opinion)
                            new_opinion = new_opinion.strip()
                            print('New opinion : ', new_opinion)
                            relationship = verifyData(seed_data, opinion)
                            if 'entail' in relationship.lower():
                                embedding = get_embedding(new_opinion)
                                embeddings.append(embedding)
                                index = new_opinion.find(':')
                                if index != '-1':
                                    new_opinion = new_opinion[index+1:]
                                final_opinion_list.append(new_opinion)
                        elif 'entail' in relationship.lower():
                            embedding = get_embedding(opinion)
                            embeddings.append(embedding)
                            index = opinion.find(':')
                            if index != '-1':
                                opinion = opinion[index+1:]
                            final_opinion_list.append(opinion)

                    for item in final_opinion_list:
                        generate_data = dict()
                        generate_data['q_id'] = k_id
                        generate_data['origin_content'] = content
                        generate_data['attitude'] = attitude
                        generate_data['new_opinion'] = item

                        print(generate_data)
                        # writer_v.write(generate_data)

                    # Remove redundancy.
                    selected_opinions = []
                    if len(embeddings) > 0:
                        if g_num == 750:
                            labels = clustering(embeddings, min(10, len(embeddings)))
                        elif g_num == 1000:
                            labels = clustering(embeddings, min(20, len(embeddings)))
                        else:
                            labels = clustering(embeddings, min(10, len(embeddings)))
                    else:
                        continue
                    # labels = clustering(embeds)
                    print('Labels: ', labels)
                    cluster_dict = dict()
                    for i in range(len(labels)):
                        label = labels[i]
                        item = final_opinion_list[i]
                        if label not in cluster_dict.keys():
                            cluster_dict[label] = [item]
                        else:
                            cluster_dict[label].append(item)
                    for k in cluster_dict.keys():
                        opinions = cluster_dict[k]
                        # i = random.randint(0, len(opinions)-1)
                        max_len = 0
                        selected_item = ''
                        for sentence in opinions:
                            if len(sentence) > max_len:
                                max_len = len(sentence)
                                selected_item = sentence

                        selected_opinions.append(selected_item)

                    print('Final Data:')
                    for item in selected_opinions:
                        generate_data = dict()
                        generate_data['q_id'] = k_id
                        generate_data['origin_content'] = content
                        generate_data['attitude'] = attitude
                        generate_data['new_opinion'] = item

                        print(generate_data)
                        writer.write(generate_data)


if __name__ == '__main__':
    fire.Fire(run)  
                    
