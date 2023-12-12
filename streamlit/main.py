import streamlit as st
import requests
import pandas as pd
import re
from streamlit_extras.stateful_button import button
from streamlit_modal import Modal

import streamlit.components.v1 as components

st.title('Law Retrieval - Hỗ trợ tra cứu văn bản quy phạm pháp luật Việt Nam ⚖')


def pre_process(text):
    """
    Pre-process the text
    :param text: string
    :return: string
    """
    text = str(text)
    text = re.sub(r'\n', ' ', text)
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
st.markdown("""
                <html>
                    <head>
                    <style>
                        ::-webkit-scrollbar {
                            width: 30px;
                            }

                            /* Track */
                            ::-webkit-scrollbar-track {
                            background: #f1f1f1;
                            }

                            /* Handle */
                            ::-webkit-scrollbar-thumb {
                            background: #888;
                            }

                            /* Handle on hover */
                            ::-webkit-scrollbar-thumb:hover {
                            background: #555;
                            }
                    </style>
                    </head>
                    <body>
                    </body>
                </html>
                """, unsafe_allow_html=True)
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
    st.session_state['id_query'] = None

if 'removeFullExpire' not in st.session_state:
    st.session_state['removeFullExpire'] = False


# def checkRemoveFullExpire():
#     st.session_state['removeFullExpire'] = True

@st.cache_data
def queryAPI(query, top_n=10):
    url = "http://localhost:5000/api/v1/lawRetrievalRouter/lawRetrieval"
    payload = {
        "query": f"{query}",
        "top_n": top_n
    }
    response = requests.request("POST", url, json=payload)
    st.session_state['result'] = response.json()['data']
    st.session_state['id'] = response.json()['id']
    return response.json()


def feedbackAPI(query_id, law_id, article_id, user_label):
    url = "http://localhost:5000/api/v1/lawRetrievalRouter/userFeedback"
    payload = {
        "query_id": query_id,
        "law_id": law_id,
        "article_id": article_id,
        "user_label": user_label
    }
    response = requests.request("POST", url, json=payload)
    return response.json()


with main_container:
    inputText_col, number_of_result_col, submitButton_col = main_container.columns(spec=(8, 2, 2))
    res = ""
    with inputText_col:
        search_bar_text = st.text_input('Tìm kiếm văn bản', '')
        st.checkbox("Bỏ văn bản hết hiệu lực toàn bộ", key="removeFullExpire")
    with number_of_result_col:
        number_of_result = st.selectbox("Giới hạn truy vấn",options=(10,20,50,100), label_visibility="hidden")
    with submitButton_col:
        st.text(' ')
        st.button("🍳", type="primary", on_click=queryAPI, args=(pre_process(search_bar_text),))

    # main_container.dataframe(df_result)

    N_cards_per_row = 1
    if search_bar_text != '':
        queryAPI(query=search_bar_text, top_n=number_of_result)
        if st.session_state['result'] == []:
            main_container.subheader("Không tìm thấy kết quả 🥲")
        else:
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
                    button_key_count = n_row
                    score_col, feedback_col_positive, feedback_col_negative = st.columns(spec=(6, 1, 1))
                    with score_col:
                        st.markdown(f"*Điểm tương quan: {row['score']}*")
                    with feedback_col_positive:
                        if st.button("👍", type="secondary", on_click=feedbackAPI, help="Văn bản này là chính xác",
                                     args=(
                                         st.session_state['id'], row['law_id'], row['article_id'], True),
                                     key=f"positive_{n_row}"):
                            score_col.markdown(":green[Feedback thành công, cảm ơn bạn đã đóng góp!] 👍🏼👍🏼👍🏼")
                    with feedback_col_negative:
                        if st.button("👎", type="secondary", args=(
                            st.session_state['id'], row['law_id'], row['article_id'], False),
                                     help="Văn bản này chưa chính xác", key=f"negative_{n_row}"):
                            score_col.markdown(":green[Feedback thành công, cảm ơn bạn đã đóng góp!] 👍🏼👍🏼👍🏼")
                    # if button_status:
                    #     st.markdown(":green[Feedback thành công, cảm ơn bạn đã đóng góp!]")
