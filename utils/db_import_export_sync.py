import os
import random
import sys
from types import SimpleNamespace
from typing import List, Dict, Optional

from loguru import logger

from data.config import FILES_DIR
from data.models import ai_models

from utils.db_api.wallet_api import db, get_wallet_by_email_data
from utils.db_api.models import Wallet

def parse_proxy(proxy: str | None) -> Optional[str]:
    if not proxy:
        return None
    if proxy.startswith('http'):
        return proxy
    elif "@" in proxy and not proxy.startswith('http'):
        return "http://" + proxy
    else:
        value = proxy.split(':')
        if len(value) == 4:
            ip, port, login, password = value
            return f'http://{login}:{password}@{ip}:{port}'
        else:
            print(f"Invalid proxy format: {proxy}")
            return None 
        
def pick_proxy(proxies : list, i: int) -> Optional[str]:
    if not proxies:
        return None
    return proxies[i % len(proxies)]

def remove_line_from_file(value: str, filename: str) -> bool:
    file_path = os.path.join(FILES_DIR, filename)

    if not os.path.isfile(file_path):
        return False

    with open(file_path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    original_len = len(lines)

    keep = [line for line in lines if line.strip() != value.strip()]

    if len(keep) == original_len:
        return False

    with open(file_path, "w", encoding="utf-8") as f:
        for line in keep:
            f.write(line + "\n")
    return True

def read_lines(path: str) -> List[str]:

    file_path = os.path.join(FILES_DIR, path)
    if not os.path.isfile(file_path):
        return []
    with open(file_path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

class Import:


    @staticmethod
    def parse_wallet_from_txt() -> List[Dict[str, Optional[str]]]:

        email_data = read_lines("email_data.txt")
        proxies        = read_lines("proxy.txt")

        record_count = len(email_data)

        wallets: List[Dict[str, Optional[str]]] = []
        for i in range(record_count):
            wallets.append({
                "email_data": email_data[i],
                "proxy": parse_proxy(pick_proxy(proxies, i)),
            })

        return wallets



    @staticmethod
    async def wallets():
                
        raw_wallets = Import.parse_wallet_from_txt()

        logger.success("Wallet import to the database is in progress…")
        
        wallets = [SimpleNamespace(**w) for w in raw_wallets]

        imported: list[Wallet] = []
        edited: list[Wallet] = []
        total = len(wallets)

        check_wallets = db.all(Wallet)

        if len(check_wallets) > 0:
            # Check pwd1
            try:
                check_wallet = check_wallets[0]

            except Exception as e:
                sys.exit(f"Database not empty | You must use same password for new wallets | {e}")

        ai_mdls = ai_models()

        for wl in wallets:



            wallet_instance = get_wallet_by_email_data(wl.email_data)

            if wallet_instance:
                changed = False

                if wallet_instance.proxy != parse_proxy(wl.proxy):
                    wallet_instance.proxy = wl.proxy
                    changed = True

                if hasattr(wallet_instance, "email_data") and wallet_instance.email_data != wl.email_data:
                    wallet_instance.email_data = wl.email_data
                    changed = True

                if changed:
                    db.commit()
                    edited.append(wallet_instance)

                continue

            wallet_instance = Wallet(
                proxy=wl.proxy,
                email_data=wl.email_data,
                ai_model = str(random.choice(ai_mdls))
            )


            db.insert(wallet_instance)
            imported.append(wallet_instance)

        logger.success(
            f'Done! imported wallets: {len(imported)}/{total}; '
            f'edited wallets: {len(edited)}/{total}; total: {total}'
        )
        
        
    
class Sync:
    
    @staticmethod
    def parse_tokens_and_proxies_from_txt(wallets : List) -> List[Dict[str, Optional[str]]]:

        proxies        = read_lines("proxy.txt")
        
        record_count = len(wallets)

        wallet_auxiliary: List[Dict[str, Optional[str]]] = []
        for i in range(record_count):
            wallet_auxiliary.append({
                "proxy": parse_proxy(pick_proxy(proxies, i)),
            })

        return wallet_auxiliary
    

    @staticmethod
    async def sync_wallets_with_tokens_and_proxies():
               
        wallets = db.all(Wallet)

        if len(wallets) <= 0:
            logger.warning("No wallets in DB, nothing to update")
            return
        
        wallet_auxiliary_data_raw  = Sync.parse_tokens_and_proxies_from_txt(wallets)

        wallet_auxiliary_data = [SimpleNamespace(**w) for w in wallet_auxiliary_data_raw]
        
        if len(wallet_auxiliary_data) != len(wallets):
            logger.warning("Mismatch between wallet data and tokens/proxies data. Exiting sync.")
            return
        
        total = len(wallets)

        logger.info(f"Start syncing wallets: {total}")
        
        edited: list[Wallet] = []
        for wl in wallets:

            wallet_instance = get_wallet_by_email_data(wl.email_data)

            if wallet_instance:
                changed = False

                wallet_data  = wallet_auxiliary_data [wallet_instance.id - 1]
                if wallet_instance.proxy != wallet_data.proxy:
                    wallet_instance.proxy = wallet_data.proxy
                    changed = True

                if changed:
                    db.commit()
                    edited.append(wallet_instance)

        logger.success(f'Done! edited wallets: {len(edited)}/{total}; total: {total}')
        
class Export:

    _FILES = {
        "email_data": "exported_email_data.txt",
        "proxy":         "exported_proxy.txt",
    }

    @staticmethod
    def _write_lines(filename: str, lines: List[Optional[str]]) -> None:

        path = os.path.join(FILES_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write((line or "") + "\n")

    @staticmethod
    async def wallets_to_txt() -> None:
        
        wallets: List[Wallet] = db.all(Wallet)

        if not wallets:
            logger.warning("Export: no wallets in db, skip....")
            return

        buf = {key: [] for key in Export._FILES.keys()}

        for w in wallets:

            buf["proxy"].append(w.proxy or "")
            buf["email_data"].append(w.email_data or "")

        for field, filename in Export._FILES.items():
            Export._write_lines(filename, buf[field])

        logger.success(f"Export: exported {len(wallets)} wallets in {FILES_DIR}")
