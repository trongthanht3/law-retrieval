import re


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
