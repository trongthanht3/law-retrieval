import streamlit as st
import requests
import pandas as pd
import re

st.title('Law Retrieval - Hỗ trợ tra cứu văn bản quy phạm pháp luật Việt Nam ⚖')

def pre_process(text):
    """
    Pre-process the text
    :param text: string
    :return: string
    """
    text = str(text)
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = re.sub('@[^\s]+', 'AT_ABC', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'([\w]+\) )', '.', text)
    text = re.sub(r'([\d]+\. )', '', text)
    text = re.sub(
        r'[^aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0-9., ]',
        '', text)
    text = text.replace('.', '. ')
    text = text.replace(' .', '. ')
    text = re.sub(r'[\s]+', ' ', text)
    text = text.strip('.')
    text = text.strip('\'"')
    text = text.strip()
    text = text.lower()
    return text

main_container = st.container()

customized_button = st.markdown("""
            <style >
            .stDownloadButton, div.stButton {text-align:center}
            .stDownloadButton button, div.stButton > button:first-child {
                # background-color: #ADD8E6;
                # color:#000000;
                padding-left: 20px;
                padding-right: 20px;
                height: 56px
            }

            # .stDownloadButton button:hover, div.stButton > button:hover {
            #     background-color: #ADD8E6;
            #     color:#000000;
            # }
                }
            </style>""", unsafe_allow_html=True)

if 'result' not in st.session_state:
    st.session_state['result'] = pd.DataFrame()

if 'removeFullExpire' not in st.session_state:
    st.session_state['removeFullExpire'] = False

# def checkRemoveFullExpire():
#     st.session_state['removeFullExpire'] = True

def queryAPI(query):
    url = "http://localhost:5000/api/v1/lawRetrievalRouter/lawRetrieval"
    payload = {
        "query": f"{query}",
        "top_n": 30
    }
    response = requests.request("POST", url, json=payload)
    st.session_state['result'] = response.json()
    return response.json()


with main_container:
    inputText_col, submitButton_col = main_container.columns(spec=(8, 2))
    res = ""
    with inputText_col:
        search_bar_text = st.text_input('Tìm kiếm luật', '')
        st.checkbox("Bỏ văn bản hết hiệu lực toàn bộ", key="removeFullExpire")
    with submitButton_col:
        st.text(' ')
        st.button("🍳", type="primary", on_click=queryAPI, args=(pre_process(search_bar_text),))

    # main_container.dataframe(df_result)

    N_cards_per_row = 1
    if search_bar_text != '':
        queryAPI(search_bar_text)
        main_container.subheader('Kết quả tra cứu')
        df_result = pd.json_normalize(st.session_state['result'])
        df_result.dropna(subset=['law_name'], inplace=True)
        for n_row, row in df_result.reset_index().iterrows():
            if st.session_state.removeFullExpire:
                if row['isExpire'] == "Trạng thái:Hết hiệu lực toàn bộ":
                    continue
            i = n_row % N_cards_per_row
            if i == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
            # draw the card
            with cols[n_row % N_cards_per_row]:
                st.markdown(f"#### :blue[{str(row['law_name']).strip()}] - {str(row['description']).strip()}")
                if row['isExpire'] == "Trạng thái:Hết hiệu lực toàn bộ":
                    st.caption(
                        f":green[{str(row['expDate']).replace(':', ': ').strip()}] - :red[{str(row['isExpire']).replace(':', ': ').strip()}]")
                else:
                    st.caption(
                        f":green[{str(row['expDate']).replace(':', ': ').strip()}] - :green[{str(row['isExpire']).replace(':', ': ').strip()}]")
                st.caption(f"{str(row['url']).strip()}")
                st.markdown(f"**{str(row['article_name']).strip()}**")
                st.markdown(f"*{str(row['article_content']).strip()}*")
                st.markdown(f"*Độ tương quan: {row['score']}*")
