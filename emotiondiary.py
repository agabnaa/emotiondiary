import streamlit as st
import json
import pandas as pd

st.markdown(
    """
    <style>
    /* 배경 애니메이션 */
    @keyframes gradientBG {
      0% {
        background-position: 0% 50%;
      }
      50% {
        background-position: 100% 50%;
      }
      100% {
        background-position: 0% 50%;
      }
    }
    .stApp {
      background: linear-gradient(-45deg, #fce4ec, #f8bbd0, #AFDDFF, #E8F9FF);
      background-size: 400% 400%;
      animation: gradientBG 15s ease infinite;
      color: white;
    }

    /* 상단 헤더 투명 처리 */
    [data-testid="stHeader"] {
      background-color: rgba(0, 0, 0, 0) !important;
      box-shadow: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import streamlit as st
import json
import pandas as pd
import random

# 감성어 사전 불러오기
with open('SentiWord_info.json', encoding='utf-8-sig') as f:
    SentiWord_info = json.load(f)

sentiword_dic = pd.DataFrame(SentiWord_info)

# 감정 점수 계산 함수 (점수 범위 -2~2 → 1~10 점수 변환)
def calculate_sentiment(text):
    total_score = 0
    count = 0

    # 단어 길이 내림차순 정렬(긴 단어부터 처리)
    sorted_dic = sentiword_dic.sort_values(by='word', key=lambda x: x.str.len(), ascending=False)

    text_copy = text  # 텍스트 복사본

    for _, row in sorted_dic.iterrows():
        word = row['word']
        polarity = row['polarity']
        if word in text_copy:
            try:
                score = float(polarity)
            except:
                score = 0
            total_score += score
            count += 1
            text_copy = text_copy.replace(word, "")  # 중복 처리 방지

    if count == 0:
        return 5  # 단어 없으면 중립(10단계 중 중간 값 5점)

    avg_score = total_score / count

    # 점수 변환: -2~2 범위 → 1~10 점수
    sentiment_score = int(round((avg_score + 2) * (9 / 4) + 1))
    sentiment_score = max(1, min(sentiment_score, 10))

    return sentiment_score

# 점수별 노래 리스트 (예시: 제목, 가수, Spotify 링크)
songs_by_score = {
    1: [
        ("노래1-1", "가수1-1", "https://www.youtube.com/"),
        ("노래1-2", "가수1-2", "https://www.youtube.com/"),
        ("노래1-2", "가수1-2", "https://www.youtube.com/"),
        ("노래1-1", "가수1-1", "https://www.youtube.com/"),
        ("노래1-2", "가수1-2", "https://www.youtube.com/"),
        ("노래1-2", "가수1-2", "https://www.youtube.com/"),
    ],
    2: [
        ("노래2-1", "가수2-1", "노래링크"),
        ("노래2-2", "가수2-2", "노래링크"),
    ],
    # 3~10도 마찬가지
    5: [
        ("중립적 노래 제목1", "가수5", "https://open.spotify.com/track/xxxx5"),
        ("중립적 노래 제목2", "가수6", "https://open.spotify.com/track/xxxx6"),
    ],
    6: [
        ("노래6-1", "가수6-1", "노래링크"),
        ("노래6-2", "가수6-2", "노래링크"),
    ],
    10: [
        ("기분 좋은 노래 제목1", "가수7", "https://open.spotify.com/track/xxxx7"),
        ("기분 좋은 노래 제목2", "가수8", "https://open.spotify.com/track/xxxx8"),
    ],
}

def recommend_song(score):
    if score in songs_by_score:
        song = random.choice(songs_by_score[score])
        title, artist, link = song
        return f"🎵 {title} - {artist}\n[Spotify 듣기]({link})"
    else:
        return "🎵 추천할 노래가 없습니다."

# Streamlit UI
st.title("감정일기 분석 & 노래 추천")

user_input = st.text_area("오늘 하루를 일기로 적어주세요 👇", height=200)

if st.button("감정 분석 시작"):
    if user_input.strip() == "":
        st.warning("내용을 입력해주세요.")
    else:
        score = calculate_sentiment(user_input)
        st.subheader("감정 분석 결과")
        st.write(f"감정 점수 (1~10): **{score}점**")

        emotions = {
            1: "😢 매우 부정", 2: "🙁 부정", 3: "😟 조금 부정", 4: "😕 약간 부정",
            5: "😐 중립", 6: "🙂 약간 긍정", 7: "😊 긍정", 8: "😄 매우 긍정",
            9: "🤩 극도로 긍정", 10: "🥳 최고로 긍정"
        }
        st.write(f"예측 감정: {emotions.get(score, '알 수 없음')}")

        st.subheader("노래 추천 🎶")
        st.markdown(recommend_song(score), unsafe_allow_html=True)
