APP_NAME = "인공지능 기반 공정데이터 분석 및 예측용 공정진단시스템"

MONITOR_INPUT_LIST = [
    "VFA",
    "Alk",
    "VFA/Alk",
    "Biogas Production",
    "Biogas Yield",
    "VSRem",
]
MONITOR_PLOT_LIST = ["예측", "추세"]

PREDICTED_RANGE = 15
LEARNING_RANGE = 30
ROLLING_RANGE = 10
ROLLING_RATIO = 1

LOG_EXCUTE = ["프로그램 실행 완료",
              "루트 폴더에서 불러오기 완료",
              "지정 폴더에서 불러오기 완료",
              "데이터 내보내기 완료",
              "데이터 추가 완료", #4
              "완료", #5
              "데이터 부분 분석 완료",
              "데이터 전체 분석 완료",
              "추세 그래프 산출 완료",
              "예측 그래프 산출 완료",
              ]

LOG_ERROR = ["오류 : data 없음",
             "오류 : 파일 미선택",
             "오류 : 확장자 불일치",
             "오류 : data 범주 불일치",
             "오류 : 데이터 파일 사용중",
             "오류 : 데이터 분석 범위 미달", #5
             "오류 : 루트에 데이터 없음",
             "오류 : Time 유효성 불합격",
             "경고 : 데이터 수 부족",
             "오류 : 0인 데이터 입력",
             "오류 : 비어있는 입력란",
             "경고 : 0인 데이터 존재"
             ]