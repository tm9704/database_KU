import datetime

def timearr(id):
    d = datetime.datetime.now()
    arr = d.strftime("%Y%m%d%I%M%S")              #id받아서 시간정보랑 붙여서 게임넘버생성해서 리턴

    return id + arr