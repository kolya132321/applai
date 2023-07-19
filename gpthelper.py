import openai
import json
import profile_parser
from transliterate import translit, get_available_language_codes

from datetime import datetime

global position
position = 'Бизнес-аналитик'

vacancy=f"""


Требования для вакансии:

не менее года опыта работы в аналогичном направлении;
развитые аналитические способности, структурное мышление;
уверенное владение SQL (на уровне написания сложных запросов), Python (Numpy, Pandas);
опыт работы в Power BI или аналоге;
умение делать выводы на основе метрик;
владение ключевыми показателями продуктов для проверки гипотез;
умение выделить и оценить ключевые метрики, на которые повлияет то или иное изменение;
понимание взаимосвязи метрик;
высшее образование в области математики, экономики, финансов или статистики.
"""

def get_prev_msgs(public_id):
    f = open('msg_hist.json')
    hist = json.load(f)
    if public_id in hist:
        return hist[public_id]
    else:
        return None


def add_to_history(public_id,role, text):
    profile = profile_parser.get_profile_info('seemyoon@gmail.com', 'karamelka2009', public_id)
    replicant_info = profile_parser.generate_inital_prompt(profile)

    f = open('msg_hist.json')
    hist = json.load(f)
    if public_id in hist:
        hist[public_id].append({"role": role, "content": text})
    else:
        new_dict=[
            {"role": "system",
             "content": f"Тебя зовут Камила, ты HR-сотрудник, и ты проводишь предварительное собеседование на позицию {position} в Райффайзенбанк." + replicant_info},
            {"role": "system",
             "content": f"Задавай вопрос по одному"},
            {"role": "user", "content": "Задай вопрос на тему: опыт работы."},
            {"role": "user",
             "content": "Задай вопрос о  основных обязанностях и достижениях на последнем месте работы."},
            {"role": "user","content": "Задай вопрос на тему: технические навыки."},
            {"role": "user",
             "content": "Какие фреймворки и инструменты  использовал на последнем месте работы?"},
            {"role": "user",  "content": "Задай вопрос на тему: soft skills."},
            {"role": "user",
             "content": "Попроси рассказать о способности работать в команде."},
            # {"role": "system", "name": f"{profile.get('first_name')}",
            #        "content": "Коротко поблагодари меня за участие в собеседовании и заверши диалог."},
            #       {"role": "system", "name": "Kamila",
            #        "content": "Спасибо за участие в собеседовании! Мы свяжемся с вами в ближайшее время для дальнейшего обсуждения. Удачи вам в карьере!"}
                  ]
        new_dict.append({"role": role, "content": text})
        hist[public_id]=new_dict

    with open("msg_hist.json", "w", encoding='utf8') as outfile:
        json.dump(hist, outfile)
    return hist


def new_chat(public_id, msg):
    inital_hist=get_prev_msgs(public_id)
    add_to_history(public_id,'user',msg)
    messages = get_prev_msgs(public_id)

    print(messages)

    #
    messages.append({"role": "user", "content": msg})
    openai.api_key = "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"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        temperature=0)
    chat_response = completion.choices[0].message.content
    add_to_history(public_id,'assistant',chat_response)
    if 'спасибо' in chat_response.lower():
        questions = [
           # 'Опиши профиль собеседуемого, на основе его опыта и ответов: напиши его имя, позицию, на которую он претендует, выдели сильные и слабые стороны, а также оцени собеседуемого по шкале от 0 до 10 с обоснованием выбора.',
            # 'Суммаризуй кандидата в двух предложениях.',
            'Оцени по пунктам профиль собеседуемого на основе требований к вакансии и полученных ответов. ' + vacancy + '\n\n[OUTPUT FORMAT] Требование - Оценка'
            #'Оцени, насколько, по твоему мнению, кандидат подходит под требования для вакансии на основе собеседования. Представь свое мнение коротко. \n\n' + vacancy
        ]

        for question in questions:
            messages.append({"role": "user", "content": question})

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=messages,
                temperature=0
            )
            chat_response_eval = completion.choices[0].message.content
            print(f'Камила: {chat_response_eval}')
            with open(public_id+"_reports.txt", "w", encoding='utf8') as outfile:
                outfile.write(chat_response_eval+'\n\n')
    return chat_response

print(get_prev_msgs('vladislav-rubanov-029193284'))

#
# ai=openai.ChatCompletion.acreate(
#                 model=self.config['model'],
#                 messages=self.conversations[chat_id],
#                 temperature=self.config['temperature'],
#                 n=self.config['n_choices'],
#                 max_tokens=self.config['max_tokens'],
#                 presence_penalty=self.config['presence_penalty'],
#                 frequency_penalty=self.config['frequency_penalty'],
#                 stream=stream
#             )
