from datetime import datetime
import time
from iqoptionapi.stable_api import IQ_Option
import logging

from src.strategy.mhi import mhi
import pandas as pd
import src.credentials as userData

asset = 'EURUSD'
maxDict = 10
size = 300

logging.disable(level=(logging.DEBUG))

user = userData.auth
Iq = IQ_Option(user['USERNAME'], user['PASSWORD'])
check, reason = Iq.connect()
# print(check)
# print(reason)

MODE = 'REAL' # PRACTICE / REAL
Iq.change_balance(MODE)
INITIAL_BALANCE = Iq.get_balance()

# duration = 1
# Iq.buy_digital_spot_v2(asset, 1, 'put', duration)

# profile = Iq.get_profile_ansyc()
# print(profile)

timeframe = 60
expiration_mode = 5

def get_data(candles_amount):
	global timeframe, asset
	df = pd.DataFrame()
	candles = []
	candles = Iq.get_candles(asset, timeframe, candles_amount, time.time())
	df = pd.concat([pd.DataFrame(candles), df], ignore_index=True)
	return df

def check_order(order_check, order_id):
	if order_check:
		result = Iq.check_binary_order(order_id)
		if result['result']:
			res = round(float(result['profit_amount']) - float(result['amount']), 2)
			print('Resultado: ', res)
	return res

def is_time():
	minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
	enter = False
	if minutos == 4.55 or minutos == 9.55:
		enter = True
	return enter

def is_minute_passed():
	minutos = float(((datetime.now()).strftime('%%.%S'))[1:])
	# print(minutos)
	enter = False
	if minutos == 0.55:
		enter = True
	return enter

# try:
# 	while True:
# 		indicators = Iq.get_technical_indicators(asset)
# 		# print(indicators)
# 		m1 = {}
# 		m5 = {}
# 		m15 = {}
# 		geral = {}
# 		for indicator in indicators:
# 			v = indicator['action']
# 			group = indicator['group']
# 			candle_size = indicator['candle_size']
# 			if group == 'MOVING AVERAGES':
# 				if candle_size == 60:
# 					if v not in m1:
# 						m1[v] = 0
# 					m1[v] += 1

# 				if candle_size == 300:
# 					if v not in m5:
# 						m5[v] = 0
# 					m5[v] += 1

# 				if candle_size == 900:
# 					if v not in m15:
# 						m15[v] = 0
# 					m15[v] += 1
				
# 			if v not in geral:
# 				geral[v] = 0
# 			geral[v] += 1
		
# 		print('M1: ', m1)
# 		print('M5: ', m5)
# 		print('M15: ', m15)
# 		print('GERAL: ', geral)

# 		if 'buy' in m1 and 'buy' in m5 and 'buy' in m15:
# 			if m1['buy'] >= 16 and m5['buy'] >= 16 and m15['buy'] >= 16:
# 				print('CALL')

# 		time.sleep(3)
# except KeyboardInterrupt:
# 	print('Parando aplicação...')

def buyPerIndicator(CURRENT_BALANCE):
	indicators = Iq.get_technical_indicators(asset)
	# print(indicators)
	m1 = {}
	m5 = {}
	m15 = {}
	geral = {}
	for indicator in indicators:
		v = indicator['action']
		group = indicator['group']
		candle_size = indicator['candle_size']
		if group == 'MOVING AVERAGES':
			if candle_size == 60:
				if v not in m1:
					m1[v] = 0
				m1[v] += 1

			if candle_size == 300:
				if v not in m5:
					m5[v] = 0
				m5[v] += 1

			if candle_size == 900:
				if v not in m15:
					m15[v] = 0
				m15[v] += 1
			
		if v not in geral:
			geral[v] = 0
		geral[v] += 1
	
	total_call = 0
	total_put = 0
	total_hold = 0
	if 'buy' in m5 and 'sell' in m5 and 'hold' in m5:
		if m5['buy'] > m5['sell'] and m5['buy'] > m5['hold'] and m5['buy'] >= 10:
			total_call += 1
		elif m5['sell'] > m5['buy'] and m5['sell'] > m5['hold'] and m5['sell'] >= 10:
			total_put += 1
		elif m5['hold'] > m5['buy'] and m5['hold'] > m5['sell'] and m5['hold'] >= 300:
			total_hold += 1
		else:
			print('Minute - NONE')
	elif 'buy' not in m5 and 'sell' in m5 and 'hold' in m5:
		if m5['sell'] > m5['hold'] and m5['sell'] >= 10:
			total_put += 1
		elif m5['hold'] > m5['sell'] and m5['hold'] >= 300:
			total_hold += 1
		else:
			print('Minute - NONE')
	elif 'buy' in m5 and 'sell' not in m5 and 'hold' in m5:
		if m5['buy'] > m5['hold'] and m5['buy'] >= 10:
			total_call += 1
		elif m5['hold'] > m5['buy'] and m5['hold'] >= 300:
			total_hold += 1
		else:
			print('Minute - NONE')
	elif 'buy' in m5 and 'sell' in m5 and 'hold' not in m5:
		if m5['buy'] > m5['sell'] and m5['buy'] >= 10:
			total_call += 1
		elif m5['sell'] > m5['buy'] and m5['sell'] >= 300:
			total_put += 1
		else:
			print('Minute - NONE')
	
	if total_call == 0 and total_put == 0 and total_hold == 0:
		print('ALL IQUALS ZERO')
	else:
		if total_call > total_put and total_call > total_hold:
			Iq.buy_digital_spot_v2(asset, (CURRENT_BALANCE * 0.05), 'call', expiration_mode)
		elif total_put > total_call and total_put > total_hold:
			Iq.buy_digital_spot_v2(asset, (CURRENT_BALANCE * 0.05), 'put', expiration_mode)
		else:
			print('Espera')

	print('----------------------------')
	print(f'CALL: {total_call} - PUT: {total_put} - HOLD: {total_hold}')
	print('----------------------------')
	print('M1: ', m1)
	print('M5: ', m5)
	print('M15: ', m15)
	print('GERAL: ', geral)

try:
	while True:
		CURRENT_BALANCE = Iq.get_balance()

		if is_minute_passed():
			buyPerIndicator(CURRENT_BALANCE)

		if CURRENT_BALANCE > (INITIAL_BALANCE - (INITIAL_BALANCE * 0.2)):
			# print(Iq.get_balance())
			if is_time():
				print('\nAnalisando...')
				data = get_data(120)
				opened = data['open']
				closed = data['close']

				signal = mhi(opened, closed)
				print('MHI: ', signal)

				if signal is not None:
					print('Comprou')
					order_check, order_id = Iq.buy_digital_spot_v2(asset, (CURRENT_BALANCE * 0.05), signal, expiration_mode)
					# res = check_order(order_check, order_id)
					# print(f'Res: {res}')
			else:
				print('...')
		else:
			print('STOP LOSS')
			break
		time.sleep(1)
except KeyboardInterrupt:
	print('Parando aplicação...')