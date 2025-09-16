import asyncio
import random
from datetime import datetime, timedelta
from typing import List

from loguru import logger

from functions.controller import Controller
from utils.db_api.models import Wallet
from utils.db_api.wallet_api import db
from data.settings import Settings

async def random_sleep_before_start(wallet):
    random_sleep = random.randint(Settings().random_pause_start_wallet_min, Settings().random_pause_start_wallet_max)
    now = datetime.now()

    logger.info(f"{wallet} Start at {now + timedelta(seconds=random_sleep)} sleep {random_sleep} seconds before start actions")
    await asyncio.sleep(random_sleep)
    
async def execute(wallets : List[Wallet], task_func, random_pause_wallet_after_completion : int = 0):
    
    while True:
        
        semaphore = asyncio.Semaphore(min(len(wallets), Settings().threads))

        if Settings().shuffle_wallets:
            random.shuffle(wallets)

        async def sem_task(wallet : Wallet):
            async with semaphore:
                try:
                    await task_func(wallet)
                except Exception as e:
                    logger.error(f"[{wallet.id}] failed: {e}")

        tasks = [asyncio.create_task(sem_task(wallet)) for wallet in wallets]
        await asyncio.gather(*tasks, return_exceptions=True)

        if random_pause_wallet_after_completion == 0:
            break
 
        # update dynamically the pause time
        random_pause_wallet_after_completion = random.randint(Settings().random_pause_wallet_after_completion_min,
                                                              Settings().random_pause_wallet_after_completion_max)
        
        next_run = datetime.now() + timedelta(seconds=random_pause_wallet_after_completion)
        logger.info(
            f"Sleeping {random_pause_wallet_after_completion} seconds. "
            f"Next run at: {next_run.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        await asyncio.sleep(random_pause_wallet_after_completion)

async def activity(action: int):
    wallets = db.all(Wallet)
   

    range_wallets = Settings().range_wallets_to_run
    if range_wallets != [0, 0]: 
        start, end = range_wallets
        wallets = [
            wallet for i, wallet in enumerate(wallets, start=1)
            if start <= i <= end
        ]
    else:
        if Settings().exact_wallets_to_run:
            wallets = [
                wallet for i, wallet in enumerate(wallets, start=1)
                if i in Settings().exact_wallets_to_run
            ]

    if action == 1:
        await execute(wallets, start_activity, random.randint(Settings().random_pause_wallet_after_completion_min, Settings().random_pause_wallet_after_completion_max))


async def start_activity(wallet):
    
    await random_sleep_before_start(wallet=wallet)
    
    controller = Controller(wallet=wallet)

    c = await controller.handle_account()
    logger.success(c)

