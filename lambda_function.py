from binance import Client
import os


def lambda_handler(event, context):
    bot = Client(api_key=os.environ.get('api_key'), api_secret=os.environ.get('secret'))
    
    #alert 메시지 내용
    data = eval(event['body'])
    print(data)
    
    #잔고 가져오기
    info = bot.futures_account_balance()
    
    for i in info:
        if i['asset'] == 'USDT':
            balance = i['balance']
    
    balance = float(balance)
    print("balance : ", balance)
    
    #레버리지 설정하기
    bot.futures_change_leverage(symbol = 'BTCUSDT', leverage = 20)
    
    #진입수량 계산하기
    btc_close = data['bar']['close']
    btc_close = float(btc_close)
    entry_amount = float((round((round(balance)) * 19 / btc_close, 3)))
    
    #현재 포지션 가져오기
    get_position = bot.futures_position_information(symbol="BTCUSDT")
    positionAmt = float(get_position[0]['positionAmt'])
    print("position_amount : ", positionAmt)
    
    
    #주문하기
    
    #롱 포지션 진입
    if (data['position'] == "Long1" or data['position'] == "Long2" or data['position'] == "Long3" or data['position'] == "Long4" 
            or data['position'] == "Long5" or data['position'] == "Long6" or data['position'] == "Long7" or data['position'] == "Long8" 
            or data['position'] == "Long0" or data['position'] == "LongF" 
            or data['position'] == "l11" or data['position'] == "l21" or data['position'] == "l22"
            or data['position'] == "l31" or data['position'] == "l32" or data['position'] == "l33"
            or data['position'] == "Bull" or data['position'] == "Bottom" or data['position'] == "maLong" or data['position'] == "LongEntry"):
                
        if positionAmt == 0: #포지션이 없을 때
            order = bot.futures_create_order(symbol="BTCUSDT", side="BUY", type="MARKET", quantity=entry_amount)
            print("롱 자리 초기 진입! entry_amount : ", entry_amount)
            print(order)
        elif positionAmt < 0: #숏 포지션을 잡고 있을 때
            order = bot.futures_create_order(symbol="BTCUSDT", side="BUY", type="MARKET", quantity=abs(positionAmt)*2)
            print("숏 포지션 청산 후 롱 진입!")
            print(order)
        elif positionAmt > 0: #롱 포지션을 이미 잡고 있을 때
            print("롱 신호가 왔지만 이미 롱 포지션을 잡고 있어 패스. positionAmt : ", positionAmt)
            pass

    #롱 포지션 청산
    elif (data['position'] == "Exit Long1" or data['position'] == "Exit Long2" or data['position'] == "Exit Long3" or data['position'] == "Exit Long4"
            or data['position'] == "Exit Long5" or data['position'] == "Exit Long6" or data['position'] == "Exit Long7" or data['position'] == "Exit Long8"
            or data['position'] == "Exit Long0" or data['position'] == "Exit LongF"
            or data['position'] == "Exit l11" or data['position'] == "Exit l21" or data['position'] == "Exit l22"
            or data['position'] == "Exit l31" or data['position'] == "Exit l32" or data['position'] == "Exit l33" 
            or data['position'] == "Exit Bull" or data['position'] == "Exit Bottom" or data['position'] == "Exit maLong"
            or data['comment'] == "Close Long1" or data['comment'] == "Close Long2" or data['comment'] == "Close Long3" or data['comment'] == "Close Long4"
            or data['comment'] == "Close Long5" or data['comment'] == "Close Long6" or data['comment'] == "Close Long7" or data['comment'] == "Close Long8"
            or data['comment'] == "Close Long0" or data['comment'] == "Close LongF"
            or data['comment'] == "Close l11" or data['comment'] == "Close l21" or data['comment'] == "Close l22" 
            or data['comment'] == "Close l31" or data['comment'] == "Close l32" or data['comment'] == "Close l33"
            or data['comment'] == "Close Bull" or data['comment'] == "Close Bottom" or data['comment'] == "Close maLong"or data['comment'] == "Exit Long"):
                
        if positionAmt <= 0: # 숏 포지션을 잡고 있거나 포지션이 없는 경우
            print("롱 청산 신호가 왔지만 숏 포지션을 잡고 있거나 포지션이 없음. positionAmt : ", positionAmt)
            pass
        elif positionAmt > 0: # 롱 포지션을 잡고 있는 경우
            order = bot.futures_create_order(symbol="BTCUSDT", side="SELL", type="MARKET", quantity=positionAmt)
            print("롱 포지션 청산! positionAmt : ", positionAmt)
            print(order)
    
    #숏 포지션 진입
    elif (data['position'] == "Short1" or data['position'] == "Short2" or data['position'] == "Short3"
            or data['position'] == "Short4" or data['position'] == "Short5" 
            or data['position'] == "Top" or data['position'] == "maShort" or data['position'] == "Bear"
            or data['position'] == "s11" or data['position'] == "s13"
            or data['position'] == "s22" or data['position'] == "s31" or data['position'] == "s32"
            or data['position'] == "d0ss" or data['position'] == "d0s" or data['position'] == "ShortEntry"):
        if positionAmt == 0: #포지션이 없을 때
            order = bot.futures_create_order(symbol="BTCUSDT", side="SELL", type="MARKET", quantity=entry_amount)
            print("숏 자리 초기 진입! entry_amount : ", entry_amount)
            print(order)
        elif positionAmt > 0: #롱 포지션을 잡고 있을 때
            order = bot.futures_create_order(symbol="BTCUSDT", side="SELL", type="MARKET", quantity=abs(positionAmt)*2)
            print("롱 포지션 청산 후 숏 진입!")
            print(order)
        elif positionAmt < 0: #숏 포지션을 이미 잡고 있을 때
            print("숏 신호가 왔지만 이미 숏 포지션을 잡고 있어 패스. positionAmt : ", positionAmt)
            pass
        
    #숏 포지션 청산
    elif (data['position'] == "Exit Short1" or data['position'] == "Exit Short2" or data['position'] == "Exit Short3"
            or data['position'] == "Exit Short4" or data['position'] == "Exit Short5" 
            or data['position'] == "Exit Top" or data['position'] == "Exit maShort" or data['position'] == "Exit Bear"
            or data['position'] == "Exit s11" or data['position'] == "Exit s13"
            or data['position'] == "Exit s22" or data['position'] == "Exit s31" or data['position'] == "Exit s32"
            or data['position'] == "Exit d0ss" or data['position'] == "Exit d0s"
            or data['comment'] == "Close Short1" or data['comment'] == "Close Short2" or data['comment'] == "Close Short3"
            or data['comment'] == "Close Short4" or data['comment'] == "Close Short5" 
            or data['comment'] == "Close Top" or data['comment'] == "Close maShort" or data['comment'] == "Close Bear"
            or data['comment'] == "Close s11" or data['comment'] == "Close s13"
            or data['comment'] == "Close s22" or data['comment'] == "Close s31" or data['comment'] == "Close s32"
            or data['comment'] == "Close d0ss" or data['comment'] == "Close d0s" or data['comment'] == "Exit Short"):
                
        if positionAmt >= 0: # 롱 포지션을 잡고 있거나 포지션이 없는 경우
            print("숏 청산 신호가 왔지만 롱 포지션을 잡고 있거나 포지션이 없음. positionAmt : ", positionAmt)
            pass
        elif positionAmt < 0: # 숏 포지션을 잡고 있는 경우
            order = bot.futures_create_order(symbol="BTCUSDT", side="BUY", type="MARKET", quantity=abs(positionAmt))
            print("숏 포지션 청산! positionAmt : ", positionAmt)
            print(order)
    
    else:
        print("알 수 없는 문제가 발생했음.")
        raise ValueError

        
        
        

# 신호 가이드라인

# 지정가
# "{'market': 'BTCUSDT', 'side': 'SELL', 'volume': '0.001', 'price': '50000.00', 'ord_type': 'limit'}"

# 시장가
# "{'market': 'BTCUSDT', 'side': 'SELL', 'volume': '0.001', 'ord_type': 'market'}"

# 청산
# "{'market': 'BTCUSDT', 'ord_type': 'close'}"


#현재 포지션 가져오기
def get_position_amt(bot, symbol):
    get_position = bot.futures_position_information(symbol=symbol)
    amt = float(get_position[0]['positionAmt'])
    return amt

#주문 일괄 청산
def close_all_position(bot, symbol):
    print("close_all_position!")
    amt = get_position_amt(bot, symbol)
    
    if amt > 0: #롱포지션이라는 의미
        close_order = bot.futures_create_order(symbol=symbol, side="SELL", type="MARKET", quantity=amt)
        print(close_order)
    elif amt < 0: #숏포지션이라는 의미
        close_order = bot.futures_create_order(symbol=symbol, side="BUY", type="MARKET", quantity=abs(amt))
        print(close_order)
    else:
        print("no position : amt is zero!")