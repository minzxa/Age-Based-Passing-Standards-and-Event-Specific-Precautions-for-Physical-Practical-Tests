import random
import streamlit as st

# 1. 데이터 구조 (리스트) 선언
event_list = ["윗몸일으키기", "메디신볼", "20m달리기", "배근력"]

situp_rules = [
    "머리 뒤에서 깍지 낀 손이 풀리면 파울 처리됩니다.",
    "양쪽 팔꿈치가 무릎에 정확히 닿아야 1회로 인정됩니다.",
    "반동을 주기 위해 엉덩이가 바닥에서 떨어지면 무효입니다."
]

medicine_ball_rules = [
    "던지기 전이나 후에 발이 기준선을 밟거나 넘어가면 파울입니다.",
    "공을 한 손으로 던지거나 머리 위로 넘기지 않으면 무효입니다.",
    "공이 떨어진 지점 중 가장 가까운 흔적을 기준으로 측정합니다."
]

run_20m_rules = [
    "출발 신호가 울리기 전에 움직이면 부정 출발(파울)입니다.",
    "결승선 콘을 손으로 치거나 넘어뜨리면 감점될 수 있습니다.",
    "스파이크 착용 금지 규정을 반드시 확인해야 합니다."
]

back_strength_rules = [
    "무릎을 굽힌 상태로 당겨야 하며, 펴면서 반동을 쓰면 무효입니다.",
    "손잡이를 잡은 상태에서 팔 힘으로만 당기면 측정이 중단됩니다.",
    "상체를 뒤로 과도하게 젖히면 파울 처리됩니다."
]

# 2. 핵심 판정 함수 (def) - snake_case 준수
def evaluate_record(event_name, age, user_record):
    target_standard = 0
    unit = ""
    rules = []
    is_passed = False

    # 3. 선택구조 (if-elif-else): 종목 및 나이(1~20세)에 따른 기준 설정
    if event_name == "윗몸일으키기":
        unit = "회"
        rules = situp_rules
        if age <= 13:
            target_standard = 40
        elif age <= 16:
            target_standard = 55
        else:
            target_standard = 70
        
        if user_record >= target_standard:
            is_passed = True

    elif event_name == "메디신볼":
        unit = "m"
        rules = medicine_ball_rules
        if age <= 13:
            target_standard = 6.0
        elif age <= 16:
            target_standard = 9.0
        else:
            target_standard = 12.0
            
        if user_record >= target_standard:
            is_passed = True

    elif event_name == "20m달리기":
        unit = "초"
        rules = run_20m_rules
        if age <= 13:
            target_standard = 4.2
        elif age <= 16:
            target_standard = 3.7
        else:
            target_standard = 3.3
            
        # 달리기는 기록이 기준보다 작거나 같아야 합격
        if user_record > 0 and user_record <= target_standard:
            is_passed = True

    else:  # 배근력
        unit = "kg"
        rules = back_strength_rules
        if age <= 13:
            target_standard = 90
        elif age <= 16:
            target_standard = 140
        else:
            target_standard = 190
            
        if user_record >= target_standard:
            is_passed = True

    return target_standard, unit, is_passed, rules


# --- Streamlit 웹 UI 구성 ---
st.title("🏃‍♂️ 체대 입시 실기 합격 기준 & 규칙 가이드")
st.write("나이와 기록을 입력하거나, 랜덤 종목 뽑기 버튼을 눌러 합격 여부를 확인해보세요!")

# 사용자 입력 영역
selected_event = st.selectbox("1. 실기 종목을 선택하세요", event_list)
user_age = st.slider("2. 나이를 선택하세요 (1세 ~ 20세)", min_value=1, max_value=20, value=18)
user_score = st.number_input("3. 본인의 측정 기록을 입력하세요 (회 / m / 초 / kg)", min_value=0.0, step=0.1, value=50.0)

# 버튼 2개 나란히 배치
col1, col2 = st.columns(2)
with col1:
    check_btn = st.button("선택 종목 결과 판정하기", use_container_width=True)
with col2:
    random_btn = st.button("🎲 랜덤 종목 뽑기 & 판정하기", use_container_width=True)

# 버튼 클릭 시 실행 로직
if check_btn or random_btn:
    # 랜덤 버튼을 눌렀을 경우 random 라이브러리로 종목 재선택
    if random_btn:
        final_event = random.choice(event_list)
        st.info(f"🎲 랜덤 추첨 결과, **[{final_event}]** 종목이 선택되었습니다!")
    else:
        final_event = selected_event

    # 함수 호출하여 결과 받아오기
    standard, unit, passed, rule_list = evaluate_record(final_event, user_age, user_score)

    st.divider()
    st.subheader(f"📊 [{final_event}] 분석 결과 ({user_age}세 기준)")

    # 강조 수치(Metric) 형태로 기준과 내 기록 표시
    m_col1, m_col2 = st.columns(2)
    m_col1.metric(label="연령별 합격 기준", value=f"{standard} {unit}")
    m_col2.metric(label="나의 입력 기록", value=f"{user_score} {unit}")

    # 합격/불합격 결과 출력
    if passed:
        st.success(f"🎉 축하합니다! {user_age}세 기준({standard}{unit})을 통과하여 **합격**입니다!")
    else:
        st.error(f"💦 아쉽습니다! {user_age}세 기준({standard}{unit})에 미달하여 **불합격**입니다.")

    # 4. 반복구조 (for): 주의사항 리스트를 순회하여 테이블(표) 데이터 생성
    st.write(f"### ⚠️ {final_event} 주요 파울 및 주의사항")
    table_data = []
    for index, rule_text in enumerate(rule_list, start=1):
        table_data.append({"번호": f"규칙 {index}", "주의사항 및 파울 기준": rule_text})

    st.table(table_data)
