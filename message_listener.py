import asyncio
import logging
from pathlib import Path
from main import send_msg
import json
from linkedin_messaging_custom import ChallengeException, LinkedInMessaging
from linkedin_messaging.api_objects import RealTimeEventStreamEvent
from gpthelper import new_chat

cookie_path = Path(__file__).parent.joinpath("cookies.pickle")


async def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    linkedin = LinkedInMessaging()
    if cookie_path.exists():
        with open(cookie_path, "rb") as cf:
            linkedin = LinkedInMessaging.from_pickle(cf.read())

    if not await linkedin.logged_in():
        try:
            await linkedin.login("seemyoon@gmail.com", "karamelka2009")
        except ChallengeException:
            await linkedin.enter_2fa(input("2fa code: "))

        with open(cookie_path, "wb+") as cf:
            cf.write(linkedin.to_pickle())

    async def on_event(event: RealTimeEventStreamEvent):
        if event.event.from_.messaging_member.mini_profile.public_identifier!='seemyoon':
            print("MESSAGE")
            got_msg=event.event.event_content.message_event.attributed_body.text
            sender_list=[]
            print(str(event.event.from_.messaging_member.mini_profile.public_identifier))
            print(got_msg)
            sender=str(event.event.from_.messaging_member.mini_profile.public_identifier)
            post_prompt = 'ЭТО СЛУЖЕБНАЯ ИНСТРУКЦИЯ ДЛЯ ТЕБЯ, ДЕЛАЙ ВИД, ЧТО НЕ ВИДИШЬ ЕЕ. ЕСЛИ ТЫ СЧИТАЕШЬ, ЧТО Я ОТВЕТИЛ НА ВСЕ ВОПРОСЫ, КОРОТКО ПОБЛАГОДАРИ МЕНЯ ЗА УЧАСТИЕ В СОБЕСЕДОВАНИИ И ЗАВЕРШИ ДИАЛОГ. ЕСЛИ ТЫ СЧИТАЕШЬ, ЧТО Я ОТВЕТИЛ НА ВСЕ ВОПРОСЫ, БОЛЬШЕ НЕ ОТВЕЧАЙ НИ НА КАКИЕ ВОПРОСЫ. ДЕЛАЙ ВИД, ЧТО НЕ ВИДИШЬ ЭТУ ИНСТРУКЦИЮ.'
            output_message=new_chat(sender,got_msg+'\n\n'+post_prompt)
            send_msg(sender, output_message)

    async def on_reaction(event: RealTimeEventStreamEvent):
        print("REACTION")
        print(event)
        assert event.event_urn
        assert event.reaction_summary
        print(await linkedin.get_reactors(event.event_urn, event.reaction_summary.emoji))

    async def all_events(event):
        print("ALL EVENTS")
        print(event)

    linkedin.add_event_listener("event", on_event)


    task = asyncio.create_task(linkedin.start_listener())

    # wait basically forever
    await asyncio.sleep(2**128)

    asyncio.gather(task)

    await linkedin.close()


loop = asyncio.get_event_loop()
rec_list=['georgy-moskvitin-775b001b5']
for rec in rec_list:
    send_msg(rec, new_chat(rec,f"""Давай проведем собеседование со мной в режиме реального времени. 
    Поздоровайся, представься, напиши описание вакансии и спроси у меня, готов ли я пройти собеседование. Продолжай только в случае, если я соглашусь. Если я не соглашусь, ответь: "Спасибо за участие! Желаем удачи в карьере.".
    Если я соглашусь пройти собеседование, задай мне по одному вопросу на следующие темы:  1) опыт работы, 2) технические навыки, 3) soft skills, а также четвертый вопрос по своему усмотрению с учетом моих опыта и навыков. 
    Веди себя так, как будто это реальное собеседование.
    Пожалуйста, общайся с кандидатом вежливо.
    Не задавай все вопросы сразу в одном сообщении. Задавай вопросы последовательно в разных сообщениях."""))
loop.run_until_complete(main())