const $computer=document.querySelector('#computer');
const $scissor=document.querySelector('#scissor');
const $rock=document.querySelector('#rock');
const $paper=document.querySelector('#paper');
const $score=document.querySelector('#score');
const $new_game=document.querySelector('#new_game');

const rspX={       //한 그림을 삼등분해서 나타냄
    scissor:'-1120px', //가위
    rock:'0px',//바위
    paper:'-560px'//보
};

const RSP_num={   //가위바위보의 상수화
    scissor:1,
    rock:0,
    paper:-1,
};

//이미지를 불러올수있는 변수 만들기
const IMG='static/img/rsp.jpg';

let comGame = 'scissor'; //초기값
let replay=false;         //버튼 재클릭 방지를 위한 변수
let already_replay=0;    //'새 게임'버튼 재클릭 방지를 위한 변수
let score=0;             //총 점수 변수
let message='';          //한 판의 결과를 위한 변수
let myWin=0;             //삼세판 판정을 위한 변수
let comWin=0;
var date_arr             //현재 날짜 변수
var result               //게임결과
var str_myGame=''        //내가 선택한 배열
var str_comGame=''       //컴퓨터가 선택한 배열

function dataSave(str_myGame,str_comGame,result,date_arr){
    var gameResult={
        'str_myGame_give' : str_myGame,
        'str_comGame_give' : str_comGame,
        'result_give' : result,
        'date_arr_give' : date_arr
       };
    $.ajax({
        type: 'POST',
        url: '/gameAPI',
        dataType: 'json',
        data: JSON.stringify(gameResult),
        contentType:"application/json; charset=UTF-8",
        success: function(response){
            alert("ajax success");
        }
    })
}
const comHandChange= () => {    //그림이 빠르게 변하기 위한 함수
    if(comGame=='scissor'){
    comGame='rock';
    }
    else if(comGame=='rock'){
    comGame='paper';
    }
    else if(comGame=='paper'){
    comGame='scissor';
    }
    $computer.style.background=`url(${IMG}) ${rspX[comGame]} 0`;
    $computer.style.backgroundSize='auto 500px';
}

const clickButton=()=>{ //아무 버튼이 클릭되면 들어가는 함수
    if(event.target.textContent=='새 게임'){  //'새게임'버튼이 눌렸을때
        $score.innerHTML="게임 시작!!"+"<br>0(나) : 0(컴퓨터)";
        already_replay+=1;
        if(already_replay>1)                 //'새 게임'버튼이 여러번 눌리는걸 방지
            return;
        replay=true;                         //처음 새 게임버튼 눌러야 작동함
        myWin=0;                             //점수 초기화
        comWin=0;
        intervalid=setInterval(comHandChange,50);
        return;
    }
    if(replay){               //새 게임된 상태에서 가위,바위,보 버튼 눌리면 들어감
    clearInterval(intervalid);//그림 바뀌던게 멈춤
    replay=false;

    //조건부 연산자를 통해 내가 선택하는 변수를 만들어줌
    const myGame=event.target.textContent=='가위' ? 'scissor'
    : event.target.textContent=='바위' ? 'rock'
    : 'paper';

    str_myGame=str_myGame.concat(myGame); //나의 선택들의 배열 (사용자 가위바위보 선택)
    str_comGame=str_comGame.concat(comGame); //컴퓨터 선택들의 배열 (cpu 가위바위보 선택)

    const myScore=RSP_num[myGame];   //내가 고른 선택
    const comScore=RSP_num[comGame]; //컴퓨터의 선택
    const difference=myScore-comScore; //둘의 값의 차이

    //컴퓨터와의 게임 규칙
    if(difference==0){
        console.log('Draw');
        message='무승부';
    } else if(difference==-1 || difference==2){
        console.log('myWin');
        myWin+=1;
        message='승리';
    } else if(difference==-2 || difference==1){
       console.log('comWin');
       comWin+=1;
       message='패배';
    }
    //결과창에 출력
    if(myWin==2){
        let today=new Date()     //게임한 날짜
        $score.innerHTML="최종 승리!!"+"<br>"+myWin+"(나) : "+comWin+"(컴퓨터)";
        already_replay=0;
        result="Win"             //결과는 win
        date_arr=today.toLocaleString();  //현재 날짜정보 대입
        dataSave(str_myGame,str_comGame,result,date_arr);  //내선택,컴퓨터선택, 승패결과, 현재날짜 넘겨줌
        str_myGame=''
        str_comGame=''
    } else if(comWin==2){
        let today=new Date()     //게임한 날짜
        $score.innerHTML="최종 패배..."+"<br>"+myWin+"(나) : "+comWin+"(컴퓨터)";
        already_replay=0;
        result="Lose"
        date_arr=today.toLocaleString();
        dataSave(str_myGame,str_comGame,result,date_arr);
        str_myGame=''
        str_comGame=''
    } else{
        $score.innerHTML="결과: "+message+"<br>"+myWin+"(나) : "+comWin+"(컴퓨터)";
        str_myGame=str_myGame.concat('/');           //내선택들, 컴퓨터선택들의 배열을 생성
        str_comGame=str_comGame.concat('/');
        setTimeout(()=>{                             //2초뒤에 다시 셔플
            replay=true;
            intervalid=setInterval(comHandChange,50)
        },1000);
    };
  };
}

$new_game.addEventListener('click', clickButton);   //버튼 눌리는걸 기다림
$scissor.addEventListener('click', clickButton);
$rock.addEventListener('click', clickButton);
$paper.addEventListener('click', clickButton);