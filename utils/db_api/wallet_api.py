import random
from utils.db_api.models import Base, Wallet
from utils.db_api.db import DB
from data.settings import Settings

from data.config import WALLETS_DB


def get_wallets(sqlite_query: bool = False) -> list[Wallet]:
    if sqlite_query:
        return db.execute('SELECT * FROM wallets')

    return db.all(entities=Wallet)

def get_wallet_by_id(id: int, sqlite_query: bool = False) -> Wallet | None:
    return db.one(Wallet, Wallet.id == id)

def get_wallet_by_email_data(email_data: str) -> Wallet | None:
    return db.one(Wallet, Wallet.email_data == email_data)

def get_random_invite_code(id: int) -> str | None:
    if not Settings().only_settings_invite_codes:
        invite_codes = Settings().invite_codes
        wallets = db.all(
            Wallet,
            Wallet.invite_code.isnot(None), 
            Wallet.id != id 
        )

        if not wallets and not invite_codes:
            return None

        for wallet in wallets:
            invite_codes.append(wallet.invite_code)
        return random.choice(invite_codes)
    else:
        if not Settings().invite_codes:
            return None
        return random.choice(Settings().invite_codes)

def update_ref_code(id: int, ref_code: str) -> bool:
    wallet = db.one(Wallet, Wallet.id == id)
    if not wallet:
        return False
    wallet.invite_code = ref_code
    db.commit()
    return True


def update_points_and_top(id: int, points: int, rank: int) -> bool:
    wallet = db.one(Wallet, Wallet.id == id)
    if not wallet:
        return False
    wallet.points = points
    wallet.top = rank
    db.commit()
    return True


def replace_bad_proxy(id: int, new_proxy: str) -> bool:
    wallet = db.one(Wallet, Wallet.id == id)
    if not wallet:
        return False
    wallet.proxy = new_proxy
    wallet.proxy_status = "OK"
    db.commit()
    return True

def mark_proxy_as_bad(id: int) -> bool:
    wallet = db.one(Wallet, Wallet.id == id)
    if not wallet:
        return False
    wallet.proxy_status = "BAD"
    db.commit()
    return True

def get_wallets_with_bad_proxy() -> list:
    return db.all(Wallet, Wallet.proxy_status == "BAD")


db = DB(f'sqlite:///{WALLETS_DB}', echo=False, pool_recycle=3600, connect_args={'check_same_thread': False})
db.create_tables(Base)
