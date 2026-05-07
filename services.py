import httpx


async def fetch_drivers(session_key='latest'):
    url = f'https://api.openf1.org/v1/drivers?session_key={session_key}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    list_of_drivers = {driver['driver_number']: driver for driver in response.json()} 

    return list_of_drivers