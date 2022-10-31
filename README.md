<h1 align="center">😌myCalmServer</h1>

### Features
```markdown
  * No module required
  * Fast
  * Double ratelimit system (ipAddr and Key)
  * Compatible Linux / Win / MacOs
  * Compatible with all python server (Flask,Django...)
  * Configurable easily
```

### Installation
```markdown
  * download the repo
  * extract it
  * move ratelimit.py and config.json to your project dir
```

###  Configuration:
```markdown
  * Open config.json with a text editor (default,sublimText,notpad++,vscode)
  * There was already 3 config that you can use
  * To choose a config go to line 3 // line where "configToUse": 1 is
  * Change 1 to your config value 
  * With the default config you have 3 config so you can choose config 1 to 3
  * You can change a config to make your own
```

###  Usage:
#####  For live test:
```markdown
  * Run example.py
  * Open browser and go to http://127.0.0.1:1337?key=myKey
  * Spam it :)
```

#####  Python:
```python
from ratelimit import newReq
import time

ipAddr = '1.1.1.1' # Client Ip
timestamp = round(time.time()) # Current Timestamp
Key = 'myKey' # Client Key

checkResult = newReq(ipAddr, timestamp, Key) # with key / useless if keyRatelimit in config is false
checkResult = newReq(ipAddr, timestamp) # without key / ipRatelimit in config must be true
print(checkResult)
```

###  ToDo:
```markdown
  * Move database to a sqlite database (better perf)
  * Give ratelimit time remain
  * Add redirect on ratelimit
```

####  Credits:
 **B4Binks.py**
 Telegram : *SOON*
 Mail : b4binks.py@proton.me
