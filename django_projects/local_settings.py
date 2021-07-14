import os

from pathlib import Path

#settings.pyからそのままコピー
BASE_DIR = Path(__file__).resolve().parent.parent

#追加
SECRET_KEY = 'django-insecure-xd4_xvyvoo1boxqhd86+%t#64!xjs(*)1kcxpn5w*6spk1l)f@' 


#settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG = True #ローカルでDebugできるようになります