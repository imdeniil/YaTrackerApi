import asyncio
from client import YandexTrackerClient
from env import TRACKER_API_KEY, TRACKER_ORG_ID

async def main():

    async with YandexTrackerClient(
        oauth_token=TRACKER_API_KEY,
        org_id=TRACKER_ORG_ID,
        log_level="INFO") as client:  

            # issues.create - Работает 
            # issue = await client.issues.create(summary="Задача с кастомными полями", 
            #                                    queue="TESTBOT", 
            #                                    description="Подробное описание", 
            #                                    localfields={"numberOfEmployees": 10,  
            #                                                 "contact_cl": "ООО Рога и Копыта"})
            
            # issues.update - Работает
            # issue = await client.issues.update(issue_id='TESTBOT-271', 
            #                            summary="Новое название задачи", 
            #                            description="Новое описание задачи",  
            #                            priority={"id": "2", "key": "minor"} )

            # issues.get - Работает
            # issue = await client.issues.get('TESTBOT-271', expand=['transitions', 'attachments'])

            # issues.move - Работает
            # issue = await client.issues.move('BLDEV-22', 
            #                                  'TESTBOT', 
            #                                  move_all_fields=True, 
            #                                  initial_status=True, 
            #                                  expand=['transitions', 'attachments'] )

            # issues.count - Работает
            # issue = await client.issues.count(query="Queue: TESTBOT AND Status: New")

            # issues.search - Работает
            # issue = await client.issues.search(filter={"queue": "TESTBOT", 
            #                                            "assignee": "empty()"}, 
            #                                            order="+status", 
            #                                            expand=["transitions", "attachments"], 
            #                                            per_page=1)

            # issues.priorities - Работает
            # issue = await client.issues.priorities(localized=True)

            # issues.transitions.get - Работает
            # issue = await client.issues.transitions.get("TESTBOT-257")

            # issues.transitions.update - Работает
            # issue = await client.issues.transitions.update('TESTBOT-257', 'gotovoMeta')

            # issues.changelog
            # issue = await client.issues.changelog('TESTBOT-257')

            # issues.links.get
            # issue = await client.issues.links.get('TESTBOT-257')

            # issues.links.create
            # issue = await client.issues.links.create('TESTBOT-257', 'is subtask for', 'TESTBOT-263')

            # issues.links.delete
            # issue = await client.issues.links.delete("TESTBOT-257", "5001")

            # issues.checklists.create - простое создание
            # issue = await client.issues.checklists.create(
            #     'TESTBOT-257',
            #     'Протестировать новый API модуль',
            #     checked=False
            # )

            # issues.checklists.create - с дедлайном
            # issue = await client.issues.checklists.create(
            #     'TESTBOT-257',
            #     'Подготовить релиз к 31 декабря',
            #     checked=False,
            #     deadline={
            #         'date': '2025-12-31T23:59:59.000+0000',
            #         'deadlineType': 'date'
            #     }
            # )

            # issues.fields.get
            issue = await client.issues.fields.get()

            print(issue)

if __name__ == "__main__":
    asyncio.run(main())