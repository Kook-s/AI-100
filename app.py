import streamlit as st
from openai import OpenAI
import os
from PIL import Image

# OpenAI API 키 설정
os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 웹페이지 제목 및 스타일 설정
st.markdown("""
    <style>
        .title {
            font-size: 3em;
            margin-bottom: 20px;
        }
        .stSelectbox, .stMultiselect {
            font-size: 1.2em;
        }
        .stButton button {
            background-color: #4A90E2;
            color: white;
            font-size: 1.2em;
            padding: 10px 20px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# 웹페이지 제목
st.markdown('<div class="title">🎨 ColorMate</div>', unsafe_allow_html=True)

# 설명 박스 추가
st.markdown("""
    <div style="padding: 20px; border-radius: 10px; margin-top: 20px; background-color: #f9f9f9;">
        ColorMate에서 자신의 퍼스널 컬러를 진단 받으세요!<br>
        각각의 항목을 입력 후 사진을 선택 및 촬영 하여 추천을 받시면 됩니다.<br>
        (사진 선택은 필수가 아닌 선택이기 때문에 항목 선택만으로도 진단이 가능합니다.)
    </div>
""", unsafe_allow_html=True)

# 선택 항목 정의
genders = ["선택해주세요.", "남성", "여성", "기타"]
styles = ["캐주얼", "포멀", "스포츠", "빈티지", "모던", "스트리트", "럭셔리", "아웃도어", "힙스터", "비즈니스 캐주얼"]
hair_styles_male = ["선택해주세요.", "댄디", "청량한", "투블럭", "레이어드", "웨이브", "머리 연장", "댄스 헤어"]
hair_styles_female = ["선택해주세요.", "긴 머리", "단발", "포니테일", "레이어드", "웨이브"]
hair_styles_other = ["선택해주세요.", "긴 머리", "단발", "포니테일", "댄디", "청량한", "투블럭", "레이어드", "웨이브", "머리 연장", "댄스 헤어"]
seasons = ["선택해주세요.", "봄", "여름", "가을", "겨울"]
skin_tones = ["선택해주세요.", "밝은 피부", "중간 피부", "어두운 피부"]

# 선택 항목 UI
selected_gender = st.selectbox("😁성별을 선택하세요.", genders)
progress = 0

if selected_gender == "남성":
    hair_styles = hair_styles_male
elif selected_gender == "여성":
    hair_styles = hair_styles_female
else:
    hair_styles = hair_styles_other

if selected_gender != "선택해주세요.":
    progress += 20

selected_season = st.selectbox("🌱선호하는 계절을 선택하세요", seasons)
if selected_season != "선택해주세요.":
    progress += 20

selected_styles = st.multiselect("👕평소에 입는 스타일을 선택하세요. (중복 선택 가능)", styles)
if selected_styles:
    progress += 20

selected_hair_style = st.selectbox("💈헤어 스타일을 선택하세요.", hair_styles)
if selected_hair_style != "선택해주세요.":
    progress += 20

# 피부 톤 선택 (색상 선택 기능 추가)
selected_skin_tone = st.selectbox("🧴피부 톤을 선택하세요.", skin_tones)
if selected_skin_tone != "선택해주세요.":
    progress += 20

custom_skin_tone = st.color_picker("🎨혹은 피부 톤을 직접 선택하세요.", "#f1c27d")

# 진행률 표시
st.progress(progress)
st.write(f"진행률: {progress}%")

# 이미지 업로드 또는 촬영
uploaded_image = st.file_uploader("사진을 업로드하거나 촬영하세요. (갤러리 선택 혹은 촬영)", type=["jpg", "jpeg", "png"])

# 모든 필수 항목이 선택되었는지 확인
if st.button("퍼스널 컬러 추천 받기"):
    if selected_gender == "선택해주세요." or selected_season == "선택해주세요." or not selected_styles or selected_hair_style == "선택해주세요." or selected_skin_tone == "선택해주세요.":
        st.warning("모든 항목을 선택해야 합니다.")
    else:
        skin_tone = selected_skin_tone if selected_skin_tone != "기타" else custom_skin_tone
        user_input = f"""
        계절: {selected_season}
        스타일: {', '.join(selected_styles)}
        헤어 스타일: {selected_hair_style}
        피부 톤: {skin_tone}
        성별: {selected_gender}
        """

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            image_info = f"이미지와 함께 업로드된 사진 참고"
        else:
            image_info = "업로드된 이미지 없음"
        
        user_input += f"\n이미지 정보: {image_info}"
        
        with st.spinner('결과를 생성 중입니다...'):
            # GPT-4를 사용하여 퍼스널 컬러 텍스트 생성
            chat_completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": f"다음 정보를 기반으로 퍼스널 컬러를 추천해 주세요:\n{user_input}"
                    }
                ]
            )
            
            result = chat_completion.choices[0].message.content
            st.write("추천된 퍼스널 컬러:")
            # st.write(result)
            
            st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; margin-top: 20px; background-color: #f9f9f9;">
                    ${result}
                </div>
            """, unsafe_allow_html=True)
            
            st.write("추천된 퍼스널 컬러 이미지:")
            # DALL-E 3를 사용하여 예시 이미지 생성 (실사같은 한국인 이미지)
            image_prompt = f"Realistic image of a Korean person with the personal color recommendation: {result}"
            response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url
            st.image(image_url, caption='Example Image for Your Personal Color', use_column_width=True)
            
            # 업로드된 이미지가 있는 경우 표시
            if uploaded_image is not None:
                st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)
