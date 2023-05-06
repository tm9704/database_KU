# 필요한 모듈 import
from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from flask import current_app as app
main = Blueprint('main', __name__, url_prefix='/')  # url_prefix : '/'로 url을 붙여라
import json
import app.main.dbFunction as dbFunction
import app.main.makeGamenum as mkGamenum          #게임넘버 생성하는 함수
import math

databaseFunction = dbFunction.DatabaseFunction()

@main.route('/main', methods=['GET'])
def index():
    list = databaseFunction.getRankList()
    return render_template('/main/index.html',list=list)
@main.route('/main', methods=['POST'])
def index_post():
   if request.method == 'POST':
       id = request.form['id']
       passwd = request.form['passwd']
       isSuccess, nick, name = databaseFunction.checkLoginDB(id, passwd)
       databaseFunction.initialgameDB(id,mkGamenum.timearr(id))      #로그인시 game_log초기값 설정
       list = databaseFunction.getRankList()

       ban_list = databaseFunction.banList()
       print(ban_list)
       if isSuccess:
           for i in ban_list:
               if i['id'] ==id:
                   return render_template('/main/login.html', isLogin="ban", banReason=i['reason']) #밴 로그인 불가
           session['id'] = id
           session['nick'] = nick
           session['name'] = name
           if session['id'] == "user": #관리자 계정
               return render_template('/main/manager.html')
           return render_template('/main/index.html',list=list)
       else:
           return render_template('/main/login.html', isLogin="Fail")
   else:
       pass


@main.route('/game', methods = ['GET'])
def game():
    return render_template('/main/game.html')


@main.route('/gameAPI', methods=['POST'])
def post_game():
    if request.method == 'POST':
        id_this=session['id']            #현재 id를 id_this변수에 대입
        jsonGameResult = request.get_json()
        str_myGame_receive = jsonGameResult['str_myGame_give']   #내가 고른 선택들의 배열
        str_comGame_receive = jsonGameResult['str_comGame_give'] #컴퓨터가 고른 선택들의 배열
        result_receive = jsonGameResult['result_give']           #승패결과
        date_arr_receive = jsonGameResult['date_arr_give']       #게임했을때 시간
        if result_receive=="Win":                                #승패결과가 Win이면 id와 date를 기준으로 최근 point를 +100
            point_receive=databaseFunction.getCurPoint(id_this)
            point_receive+=100
        elif result_receive=="Lose":                             #승패결과가 Lose이면 id와 date를 기준으로 최근 point를 -100
            point_receive=databaseFunction.getCurPoint(id_this)
            point_receive-=100

        Game_num=mkGamenum.timearr(id_this)                      #현재id를 넣어서 게임넘버를 생성


        databaseFunction.gameDataToDB(id_this,str_myGame_receive, str_comGame_receive, result_receive,date_arr_receive,point_receive,Game_num)
        return 'ok'

@main.route('/rank', methods = ['GET'])
def rank():
    list = databaseFunction.getRankList()
    myRank = databaseFunction.getMyRank(session['id']) #내랭킹 가져오기
    return render_template('/main/rank.html', list = list, myRank = myRank)

@main.route('/myprofile', methods = ['GET'])
def myprofile():
    myRank = databaseFunction.getMyRank(session['id'])
    myPf = databaseFunction.getMyProfile(session['id'])
    return render_template('/main/myprofile.html',myPf = myPf, myRank = myRank)


@main.route('/login', methods = ['GET'])
def login():
    return render_template('/main/login.html')

@main.route('/login', methods = ['POST'])
def registerAccount():
    if request.method == 'POST':
        id = request.form['id']
        passwd = request.form['passwd']
        nick = request.form['nick']
        name = request.form['name']
        isSuccessRegister = databaseFunction.accountDataToDB(id,passwd,nick,name)
        if isSuccessRegister:
            return render_template('/main/login.html', beforeRegister="True")
        else:
            return render_template('/main/register.html', beforeRegister="False")
    else:
        pass

@main.route('/register', methods = ['GET'])
def register():
    return render_template('/main/register.html')

@main.route('/logout',methods=['GET'])
def logout():
    session.pop('id',None)
    return render_template('/main/index.html')

@main.route('/manager', methods=['GET'])
def manager():
    return render_template('/main/manager.html')

@main.route('/gamelog', methods = ['POST'])
def logSearch():
    if request.method == 'POST':
        searchText = request.form['searchText']
        vaild, log_list = databaseFunction.searchLog(searchText)
        if(vaild):
            return render_template('/main/gamelog.html', logList = log_list)
        else:
            flash("검색한 유저가 존재하지 않습니다.")
            return redirect(url_for('main.gamelog'))
    else:
        pass


@main.route('/ban', methods = ['POST'])
def ban():
    if request.method == 'POST':
        id = request.form['banId']
        reason = request.form['banReason']
        databaseFunction.banUser(id,reason)
        return redirect(url_for('main.user'))
    else:
        pass

@main.route('/unban', methods = ['POST'])
def unban():
    if request.method == 'POST':
        id = request.form['unbanId']
        databaseFunction.unbanUser(id)
        return redirect(url_for('main.user'))
    else:
        pass

@main.route('/gamelog', methods = ['GET'])
def gamelog():
    if(session['id'] != 'user'):
        return render_template('/main/undefined.html')
    log_list = databaseFunction.getGameLog()
    return render_template('/main/gamelog.html',logList = log_list)


@main.route('/delete/<uid>', methods = ['GET'])
def delete(uid):
    valid = databaseFunction.deleteGameLog(uid)
    if(valid):
        return redirect(url_for('main.gamelog'))
    else:
        flash("해당 유저의 최근 기록은 삭제가 불가능합니다.")
        return redirect(url_for('main.gamelog'))

@main.route('/user', methods = ['GET'])
def user():
    if (session['id'] != 'user'):
        return render_template('/main/undefined.html')
    user_list = databaseFunction.getProfile()
    ban_list = databaseFunction.banList()
    return render_template('/main/user.html', userList = user_list, banList = ban_list)

@main.route('/user', methods = ['POST'])
def userlogSearch():
    if request.method == 'POST':
        searchText = request.form['searchText']
        vaild, user_list = databaseFunction.searchUserLog(searchText)
        if(vaild):
            return render_template('/main/user.html', userList = user_list)
        else:
            flash("검색한 유저가 존재하지 않습니다.")
            return redirect(url_for('main.user'))
    else:
        pass

@main.route('/userprofile/<uid>', methods = ['GET'])
def userprofile(uid):
    if(session['id'] != 'user'):
        return render_template('/main/undefined.html')
    myRank = databaseFunction.getMyRank(uid)
    myPf = databaseFunction.getMyProfile(uid)
    return render_template('/main/userprofile.html',myPf = myPf, myRank = myRank)
