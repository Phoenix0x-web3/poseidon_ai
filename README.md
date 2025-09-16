# Phoenix Dev

More info:  
[Telegram Channel](https://t.me/phoenix_w3)  
[Telegram Chat](https://t.me/phoenix_w3_space)

[Инструкция на русcком](https://phoenix-14.gitbook.io/phoenix/proekty/poseidon)</br>



## Poseidon
Poseidon is a Web3 project tackling the shortage of real-world data for training AI models. By leveraging blockchain, it enables secure and incentivized data contribution, creating a transparent ecosystem for developers and enterprises. 

## Functionality
- Register with email(iCloud)
- Voice campaign


## Requirements
- Python version 3.12 
- Email (iCloud)
- Proxy (optional)
- Elevenlabs.io api key
- Capmonster captcha api key


## Installation
1. Clone the repository:
```
git clone https://github.com/Phoenix0x-web3/poseidon_ai
cd poseidon_ai
```

2. Install dependencies:
```
python install.py
```

3. Activate virtual environment: </br>

`For Windows`
```
venv\Scripts\activate
```
`For Linux/Mac`
```
source venv/bin/activate
```

4. Run script
```
python main.py
```

## Project Structure
```
poseidon/
├── data/                   #Web3 intarface
├── files/
|   ├── email_data.txt      # Emails for register
|   ├── proxy.txt           # Proxy addresses (optional)
|   ├── reserve_proxy.txt   # Reserved Proxy addresses (optional)
|   ├── wallets.db          # Database
│   └── settings.yaml       # Main configuration file
├── functions/              # Functionality
└── utils/                  # Utils
```
## Configuration

### 1. files folder
- `email_data.txt`: Work with email iCloud(format: `primary_email:app-specific-password:fake_email`)
- `proxy.txt`: One proxy per line (format: `http://user:pass@ip:port`)
- `reserve_proxy.txt`: One proxy per line (format: `http://user:pass@ip:port`)

### iCloud Mail Setup 
To use iCloud with your scripts you need a primary (real) iCloud email. After that you can generate additional (alias) emails on your iPhone or Mac. Note: this requires a paid iCloud+ subscription (cost $0.99 / month).

#### How to generate additional (hidden) emails
On iPhone / Mac go to: Settings → [your name] → iCloud → Hide My Email.

Create a new address. You can manage or deactivate aliases in the same place.

You can generate up to 20 addresses this way and it’s safer to do it 1–2 times per day — generating much more often may lead to account restrictions or temporary blocks.

#### App-specific password for IMAP
Go to Apple account support ([support.apple.com](https://support.apple.com/en-us/102525)) and generate an `app-specific password` so IMAP/SMTP access will work.

Place the credentials in your `email_data.txt` file using this format: `primary_email:app-specific-password:fake_email`

### Elevenlabs api key Setup
To generate voice in the script, we use the ElevenLabs Voice AI platform. For this, you’ll need to purchase an API key (cost $11)

<img src="https://imgur.com/sTgQJx3.png" alt="Preview" width="600"/>

<img src="https://imgur.com/tClzzyU.png" alt="Preview" width="300"/>



### 2. Main configurations
```yaml
#Settings for the application

# Number of threads to use for processing wallets
threads: 1

#BY DEFAULT: [0,0] - all wallets
#Example: [2, 6] will run wallets 2,3,4,5,6
#[4,4] will run only wallet 4
range_wallets_to_run: [0, 0]

# Whether to shuffle the list of wallets before processing
shuffle_wallets: true

# Working only if range_wallet_to_run = [0,0] 
# BY DEFAULT: [] - all wallets 
# Example: [1, 3, 8] - will run only 1, 3 and 8 wallets
exact_wallets_to_run: []

# Show email in logs
show_email_in_logs: false

#Check for github updates
check_git_updates: true

# the log level for the application. Options: DEBUG, INFO, WARNING, ERROR
log_level: INFO

# get on elevenlabs https://elevenlabs.io/app/sign-in : format key(sk_c1cd37a39fb669ee333cdc9196ce931111122335fa5f2f90)
eleven_labs_api_key: ''

# Api Key from https://dash.capmonster.cloud/
capmonster_api_key: ''

# Run browser in headless mode (false - visible, true - hidden)
headless_mode: false

# Delay before running the new cicle of wallets after it has completed all actions (1 - 2 hrs default)
random_pause_wallet_after_completion:
  min: 3600
  max: 7200

# Random pause between wallets in seconds
random_pause_between_wallets:
  min: 5
  max: 60

# Random pause between actions in seconds
random_pause_between_actions:
  min: 5
  max: 30

# Random pause to start wallet in seconds
random_pause_start_wallet:
  min: 0
  max: 60

# Invite Codes for Poseidon, can be used [GQ672VCP, HOTCHULA]
invite_codes: []

#Use only settings invite codes. If true, only invite codes from the setting above will be applied. If False, random ref codes from both invite_codes and database will be applied.
only_settings_invite_codes: false
```

## Usage

For register to portal you need email addresses. 

On first use, you need to fill in the `email_data.txt`, `proxy.txt` files and added api keys for [captcha](https://dash.capmonster.cloud/) and [voice generation](https://elevenlabs.io/app/sign-in). After launching the program, go to `DB Actions → Import wallets to Database`.

<img src="https://imgur.com/NR1uTTO.png" alt="Preview" width="600"/>

If you want to update proxy you need to make synchronize with DB. After you made changes in files `proxy.txt`, please choose this option.

<img src="https://imgur.com/O5cjvsK.png" alt="Preview" width="600"/>

Once the database is created, you can start the project by selecting `Poseidon AI → 1. Run All Activities`. 

<img src="https://imgur.com/pgLmV7B.png" alt="Preview" width="600"/>





