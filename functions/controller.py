import ast

from patchright.async_api import async_playwright
import random
import asyncio

from data.config import ROOT_DIR
from modules.js.poseidon_swapper import PoseidonRoot
from modules.monitor import ResponseMonitor
from utils.db_api.models import Wallet
from utils.db_api.wallet_api import get_random_invite_code
from utils.db_api.wallet_api import update_points_and_top, update_ref_code, get_random_invite_code
from utils.logs_decorator import controller_log
from data.settings import Settings
from modules.poseidon import Poseidon
from loguru import logger
from modules.js.poseidon_swap import POSEIDON_SWAP_JS

class Controller:

    def __init__(self, wallet: Wallet):
        #super().__init__(client)
        self.wallet = wallet
        self.poseidon = Poseidon(wallet=self.wallet)
        self.monitor = None
        self.root = PoseidonRoot(POSEIDON_SWAP_JS)

    async def handle_account(self):
        await self.poseidon._create_profile_folder()

        async with async_playwright() as context:
            browser = await self.poseidon.init_playwright(context=context)

            await self.root.add_init_script(page := await browser.new_page())

            self.poseidon.page = page

            page.on("load", lambda *_: asyncio.create_task(self.poseidon.prime_mouse_after_nav()))
            page.on("framenavigated", lambda *_: asyncio.create_task(self.poseidon.prime_mouse_after_nav()))

            # если сайт может открывать popups:
            #browser.on("page", lambda p: asyncio.create_task(self._prime_new_page(p)))

            self.monitor = ResponseMonitor(self.poseidon.page)

            await self.poseidon.page.goto(self.poseidon.base_url, wait_until='networkidle')
            await self.poseidon.prime_mouse_after_nav()

            # ok = await self.root.inject(self.poseidon.page)
            # print("injected (top):", ok)

            await self.root.start(self.poseidon.page, previewAlways=True)

            #await install_mouse_overlay(self.poseidon.page)

            await asyncio.sleep(5)
            await self.poseidon.handle_captcha()

            if self.poseidon.page.url == self.poseidon.base_url + "/login":
                auth = await self.poseidon.authorize()
                if not auth:
                    logger.error(f"{self.wallet} can't authorize")
                    return False
                await asyncio.sleep(5)

            if self.poseidon.page.url == self.poseidon.base_url + "/intro":
                intro = await self.poseidon.intro()
                if not intro:
                    logger.error(f"{self.wallet} can't send Intro")
                    return False
                await asyncio.sleep(10)

            games = random.randint(Settings().games_min,Settings().games_max)

            for _ in range(games):
                ai_model = ast.literal_eval(self.wallet.ai_model)
                campaigns = list(ai_model['lang_map'].keys())
                campaign = random.choice(campaigns)

                campaign = await self.poseidon.join_campaign(campaign)
                if campaign == "daily":
                    break
                sleep = random.randint(Settings().random_pause_between_actions_min, Settings().random_pause_between_actions_max)
                logger.info(f"{self.wallet} sleep {sleep} seconds before next campaign")
                await asyncio.sleep(sleep)
                continue

            await self.poseidon.update_points()
            if not self.wallet.invite_code:
                await self.poseidon.update_ref()
            code = get_random_invite_code(id=self.wallet.id)
            if code:
                await self.poseidon.claim_ref_code(ref_code=code)
            return True


