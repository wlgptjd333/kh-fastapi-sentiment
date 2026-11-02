# ============================================================
# ① 필요한 라이브러리 가져오기
# ============================================================
# APIRouter      : URL과 처리 함수를 연결
# Form           : HTML 폼의 입력값 받기
# Request        : 브라우저의 HTTP 요청 정보
# HTMLResponse   : HTML 응답 형식 지정
# Jinja2Templates: HTML 템플릿을 화면에 출력

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 앞에서 작성한 hf_model.py의 함수 가져오기
from .hf_model import get_classifier, normalize_prediction


# ============================================================
# ② 라우터와 HTML 템플릿 설정
# ============================================================
# router    : 감정분석 URL을 등록하는 객체
# templates : HTML 파일이 저장된 폴더 지정

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ============================================================
# ③ GET /predict/ : 감정분석 입력 화면 열기
# ============================================================
# 사용자가 브라우저에서 /predict/에 접속하면 실행됩니다.
# GET은 데이터를 조회하거나 화면을 요청할 때 사용합니다.

@router.get(
    "/predict/",
    response_class=HTMLResponse,
    name="predict_page"
)
def predict_page(request: Request):

    # --------------------------------------------------------
    # ④ 입력 화면에 필요한 초기값 전달
    # --------------------------------------------------------
    # text   : 처음에는 입력된 문장이 없음
    # result : 아직 분석 결과가 없음
    # error  : 오류 메시지가 없음

    return templates.TemplateResponse(
        request=request,
        name="sentiment/predict.html",
        context={
            "text": "",
            "result": None,
            "error": None
        }
    )


# ============================================================
# ⑤ POST /predict/ : 사용자가 입력한 문장 받기
# ============================================================
# HTML에서 [분석하기] 버튼을 누르면 실행됩니다.
# Form(default="")은 text 입력값을 가져옵니다.
# 입력값이 없으면 빈 문자열을 사용합니다.

@router.post(
    "/predict/",
    response_class=HTMLResponse,
    name="predict"
)
def predict(
    request: Request,
    text: str = Form(default="")
):

    # --------------------------------------------------------
    # ⑥ 입력 문장 정리
    # --------------------------------------------------------
    # strip() : 문장 앞뒤의 불필요한 공백 제거

    cleaned = text.strip()


    # --------------------------------------------------------
    # ⑦ 입력값 검사 (1~500자)
    # --------------------------------------------------------
    # 빈 문장이거나 500자를 초과하면 분석하지 않습니다.
    # 400 : 잘못된 입력 요청이라는 HTTP 상태 코드

    if not 1 <= len(cleaned) <= 500:

        return templates.TemplateResponse(
            request=request,
            name="sentiment/predict.html",
            context={
                "text": text,
                "result": None,
                "error": "문장은 1~500자로 입력하세요."
            },
            status_code=400
        )


    # --------------------------------------------------------
    # ⑧ Hugging Face 감정분석 모델 가져오기
    # --------------------------------------------------------
    # hf_model.py의 get_classifier() 호출
    # 처음에는 모델을 로딩하고 이후에는 재사용합니다.

    classifier = get_classifier()


    # --------------------------------------------------------
    # ⑨ AI 감정분석 실행
    # --------------------------------------------------------
    # cleaned : 분석할 문장
    # truncation=True : 토큰 길이가 길면 잘라서 처리
    # max_length=512  : 모델 입력의 최대 토큰 길이

    output = classifier(
        cleaned,
        truncation=True,
        max_length=512
    )


    # --------------------------------------------------------
    # ⑩ AI 분석 결과 정리
    # --------------------------------------------------------
    # normalize_prediction()으로 label과 score 추출
    # input에는 사용자가 입력한 문장을 저장합니다.
    # ** : 딕셔너리의 항목을 펼쳐서 합치는 문법

    result = {
        "input": cleaned,
        **normalize_prediction(output)
    }


    # --------------------------------------------------------
    # ⑪ 최종 분석 결과를 HTML 화면에 전달
    # --------------------------------------------------------
    # text   : 사용자가 입력한 문장
    # result : AI 분석 결과 (input, label, score)
    # error  : 오류가 없으므로 None
    # Jinja2가 전달받은 값을 HTML에 표시합니다.

    return templates.TemplateResponse(
        request=request,
        name="sentiment/predict.html",
        context={
            "text": cleaned,
            "result": result,
            "error": None
        }
    )
