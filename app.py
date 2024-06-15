import os
from openai import OpenAI
import streamlit as st
import time

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


st.title('슈퍼 시나리오 봇 😍')

keyword = st.text_input('키워드를 입력하세요.')

if st.button('생성하기'):
    with st.spinner('생성중 입니다.'):
        time.sleep(5)
    
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": keyword,
                },
                {
                    "role": "system",
                    "content": "입력 받은 키워드에 대한 흥미진진한 300자 이내의 시나리오를 작성해줘",
                }
            ],
        model="gpt-4o",
        )

    result = chat_completion.choices[0].message.content
    st.write(result)


# if st.button('찾아보기'):
#     url = 'https://edu.spartacodingclub.kr/random/?'+ title
#     st.image(url)
#     st.write(title)

# key = st.secrets['API_KEY']
# st.write(key)

# st.title('나의 첫 웹페이지')
# st.subheader('제 이름은요', divider = 'rainbow')

# if st.button('이름보기'):
#     st.write('여러분을 환영합니다.')
                
# age =  st.slider("몇살이니",0,130,25) #최소/최대/현재
# st.write('im', age , 'year old')

#=======================================================================================

# import streamlit as st

# col1, col2 = st.columns(2) # 두 개의 컬럼 생성. 표현하고 싶은 내용을 열 데이터로 나눠 보여주고 싶을 떄 사용합니다.

# with col1:
#     text1 = st.text_input("form을 이용하지 않는 경우")
#     text2 = st.text_area("form을 이용하지 않는 경우")
#     st.write("1번 입력값: " + text1)
#     st.write("2번 입력값: " + text2)


# with col2:
#     with st.form("form을 사용합니다"):
#         text3 = st.text_input("form을 이용하는 경우")
#         text4 = st.text_area("form을 이용하는 경우")
#         submitted = st.form_submit_button("제출")

#         if submitted:
#             st.write("1번 입력값: " + text3)
#             st.write("2번 입력값: " + text4)
#         else:
#             st.write("1번 입력값: ")
#             st.write("2번 입력값: ")