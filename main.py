from iqoptionapi.stable_api import IQ_Option
import src.credentials as env
import time

user = env.auth.get('USERNAME')
pss = env.auth.get('PASSWORD')

print("Conectando...")

api = IQ_Option(user,pss)

MODE = 'PRACTICE' # MODE: "PRACTICE"/"REAL"
GOAL = "EURUSD"
INSTRUMENT="turbo-option" ## Option "forex", "turbo-option"
ACTION = 'CALL'

def resetConn():
    status, reason = api.connect()

    # print('##### Primeira tentativa #####')
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

    # status, reason = api.connect()
    # print('Status:', status)
    # print('Reason:', reason)

isOperated = False
count = 0

def makeOperation():
    # resetConn()
    candles = api.get_candles(GOAL, 300, 20, time.time())

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

    print(f'Subiram: {subiram}')
    print(f'Empataram: {empataram}')
    print(f'Desceram: {desceram}')


# def makeOperation():
    isOperated2 = False

    api.start_mood_stream(GOAL, INSTRUMENT)
    mood = api.get_traders_mood(GOAL)
    print(f'Mood: {mood}')

    if mood > 0.65 and subiram > desceram:
    # if subiram > desceram:
        isOperated2 = True
        status, order_id = api.buy_digital_spot_v2(GOAL, 5, 'CALL', 5)
        print(status, order_id)
    elif mood < 0.4 and subiram < desceram:
    # elif subiram < desceram:
        isOperated2 = True
        status, order_id = api.buy_digital_spot_v2(GOAL, 5, 'PUT', 5)
        print(status, order_id)
    api.stop_mood_stream(GOAL)
    return isOperated2


while isOperated == False and count < 50:
    # isOperated = makeOperation()
    resetConn()
    makeOperation()
    count+=1
    # time.sleep(2)
    time.sleep(20)

print("##############################")