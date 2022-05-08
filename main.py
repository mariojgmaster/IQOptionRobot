from iqoptionapi.stable_api import IQ_Option
import src.credentials as env
import time

user = env.auth.get('USERNAME')
pss = env.auth.get('PASSWORD')

print("Conectando...")

api = IQ_Option(user,pss)
status, reason = api.connect()
MODE = 'PRACTICE' # MODE: "PRACTICE"/"REAL"
GOAL = "EURUSD"
INSTRUMENT="turbo-option" ## Option "forex", "turbo-option"

print('##### Primeira tentativa #####')
# print('Status:', status)
# print('Reason:', reason)
# print("Email:", api.email)

api.change_balance(MODE)

if reason == "2FA":
    print('##### 2FA HABILITADO #####')
    print("Um sms foi enviado com um código para seu número")

    code_sms = input("Digite o código recebido: ")
    status, reason = api.connect_2fa(code_sms)

    print('##### Segunda tentativa #####')
    print('Status:', status)
    print('Reason:', reason)
    print("Email:", api.email)

print("Banca:", api.get_balance())
candles = api.get_candles(GOAL, 60, 30, time.time())

subiram = 0
empataram = 0
desceram = 0

for candle in candles:
    id = candle.get('id')
    open = candle.get('open')
    close = candle.get('close')

    # print(f'id: {id}')
    # print(f'open: {open}')
    # print(f'close: {close}')

    if open > close:
        # print('Subiu')
        subiram+=1
    elif open < close:
        # print('Desceu')
        desceram+=1
    else:
        # print('Igual')
        empataram+=1

# print(f'Subiram: {subiram}')
# print(f'Empataram: {empataram}')
# print(f'Desceram: {desceram}')

# api.start_mood_stream(GOAL, INSTRUMENT)
# print(api.get_traders_mood(GOAL))
# api.stop_mood_stream(GOAL)

print("##############################")