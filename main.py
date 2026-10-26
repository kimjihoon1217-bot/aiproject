import streamlit as st
st.title('빨리빨리 다녀라')
a=st.text_input('이름을 입력해라 죽기전에')
b=st.selectbox('좋아하는 아이스크림 선택!',['민트초코','엄마는 외계인','슈팅스타'])
if st.button('인사말 생성'):
  st.write('반갑소')
