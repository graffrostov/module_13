import asyncio

async def start_strongman(name:str, power:int):
    number_of_balls = 5
    print(f'Силач {name} начал соревнования.')
    for i in range(1, number_of_balls + 1):
        await asyncio.sleep(20/power)
        print(f'Силач {name} поднял {i} шар.')
    print(f'Силач {name} закончил соревнования.')

async def start_tournament():
    first = asyncio.create_task(start_strongman('Pasha', 3))
    second = asyncio.create_task(start_strongman('Denis', 4))
    third = asyncio.create_task(start_strongman('Apollon', 5))
    await first
    await second
    await third

asyncio.run(start_tournament())