## Twitter API Keyの保存場所

こんな感じにlocal_settings/apikeys.pyを作成して，
```
.
├── README.md
├── get_oatoken.py
├── local_settings
│   └── apikeys.py
├── masktweets.py
└── wakati.py

1 directory, 5 files
```

このように指定してください．
```python
import os

# CONSUMER

CONSUMER_KEY="your consumer key"
CONSUMER_KEY_SECRET="your consumer key secret"
```