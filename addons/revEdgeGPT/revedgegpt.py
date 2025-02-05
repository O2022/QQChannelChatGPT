import asyncio
from EdgeGPT import Chatbot, ConversationStyle
import json

class revEdgeGPT:
    def __init__(self):
        self.busy = False
        self.wait_stack = []
        with open('./cookies.json', 'r') as f:
            cookies = json.load(f)
        self.bot = Chatbot(cookies=cookies)

    def is_busy(self):
         return self.busy
    
    async def reset(self):
        try:
            await self.bot.reset()
            return False
        except BaseException:
            return True

    async def chat(self, prompt):
        if self.busy:
             return
        self.busy = True
        resp = 'err'
        err_count = 0
        retry_count = 5
        
        while err_count < retry_count:
            try:
                resp = await self.bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative)
                resp = resp['item']['messages'][len(resp['item']['messages'])-1]['text']
                if resp == prompt:
                    resp += '\n\n如果你没有让我复述你的话，那代表我可能不想和你继续这个话题了，请输入/reset重置会话😶'
                break
            except BaseException as e:
                print(e.with_traceback)
                err_count += 1
                if err_count >= retry_count:
                        raise e
                print("[RevEdgeGPT] 请求出现了一些问题, 正在重试。次数"+str(err_count))
        self.busy = False
        
        print("[RevEdgeGPT] "+str(resp))
        return resp