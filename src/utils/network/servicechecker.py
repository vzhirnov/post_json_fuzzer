import aiohttp


async def check_service_is_available(url_aim: str, hdrs: dict):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url_aim, headers=hdrs, ssl=False) as response:
                if response.status in range(500, 512):  # TODO replace with const list
                    print(f"{response.status}")
                    print(
                        "Error: cannot start fuzzing because the service didn't respond "
                        "with an acceptable status code"
                    )
                    exit(0)
                else:
                    print("OK")
        except Exception:
            print("Error: Service is unavailable")
            exit(0)
