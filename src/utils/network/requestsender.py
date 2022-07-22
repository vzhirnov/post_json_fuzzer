import aiohttp
import asyncio
import requests
import tqdm


class RequestHandlerFactory:
    @classmethod
    def create_handler(cls, url_aim: str, hdrs: dict):
        return cls.RequestHandler(url_aim, hdrs)


def create_request_handler(factory, url_aim: str, hdrs: dict):
    return factory.create_handler(url_aim, hdrs)


class SyncRequestHandlerFactory(RequestHandlerFactory):
    class RequestHandler:
        def __init__(self, url_aim, hdrs):
            self.url_aim = url_aim
            self.hdrs = hdrs

        def post(
            self, url_aim: str, json_params: dict, hdrs: dict, suspicious_replies: list
        ):
            response = requests.post(
                url=url_aim,
                json=json_params,
                headers=hdrs,
                verify=False,
                timeout=10000000,
            )
            got_suspicious_reply = (
                {"suspicious_reply": True}
                if response.status_code in suspicious_replies
                else {"suspicious_reply": False}
            )
            response_body = response.content.decode()
            return response, json_params, response_body, got_suspicious_reply

        def start_fuzz(self, jsons: list):
            responses_bundle = []
            for json_params in tqdm.tqdm(jsons):
                result = self.post(
                    self.url_aim, json_params[0], self.hdrs, json_params[1]
                )
                responses_bundle.append(result)
            return responses_bundle


class AsyncRequestHandlerFactory(RequestHandlerFactory):
    class RequestHandler:
        def __init__(self, url_aim, hdrs):
            self.url_aim = url_aim
            self.hdrs = hdrs

        async def post(
            self, url_aim: str, json_params: dict, hdrs: dict, suspicious_replies: list
        ):
            async with aiohttp.ClientSession(trust_env=True) as session:
                for _ in range(120):
                    try:
                        async with session.post(
                            url_aim,
                            json=json_params,
                            headers=hdrs,
                            ssl=False,
                            timeout=10000000,
                        ) as response:
                            got_suspicious_reply = (
                                {"suspicious_reply": True}
                                if response.status in suspicious_replies
                                else {"suspicious_reply": False}
                            )
                            response_body = await response.text()
                            return (
                                response,
                                json_params,
                                response_body,
                                got_suspicious_reply,
                            )
                    except Exception:  # TODO handle exception correctly to get correct return at the end
                        await asyncio.sleep(
                            1
                        )  # TODO is it correct time.sleep(1) or await asyncio.sleep(1) ?
                        continue
                return None, {}, None, False

        async def start_fuzz(self, jsons: list):
            request_tasks = [
                self.post(self.url_aim, json_params[0], self.hdrs, json_params[1])
                for json_params in jsons
            ]
            responses_bundle = []
            for f in tqdm.tqdm(
                asyncio.as_completed(request_tasks), total=len(request_tasks)
            ):
                responses_bundle.append(await f)
                await asyncio.sleep(0)
            return responses_bundle
