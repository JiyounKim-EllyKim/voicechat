from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()
# print(os.environ['OPENAI_API_KEY'])               # 실행해서 출력하고 지워도 로그가 남으니까 절대 토큰값을 프린트해서 확인하지 말것.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def stt(audio):

    # 파일로 변환
    output_filename = 'input.mp3'
    audio.export(output_filename, format='mp3')     # 녹음을 하고 나면 바로 input.mp3 파일로 저장해줌.

    with open('input.mp3', 'rb') as f:              # read binary를 사용해서 읽음. 이미 이진 데이터임. text가 아님.
        transcription = client.audio.transcriptions.create(
            model="whisper-1",      # whisper라는 모델에 쏘면 OpenAI에서 받아서 바꾸고 다시 쏴줌.
            file=f,
            language='ko'           # 한국어로 인지하도록 함.
        )
        # print(transcription.text)

    # 음원파일 삭제
    os.remove('input.mp3')          # 텍스트로 변환해서 남기고 나면 음원 파일을 삭제해도 무방하다.
    return transcription.text

def ask_gpt(messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        top_p=1,
        max_completion_tokens=4096,
    )
    return response.choices[0].message.content

def tts(response: str):
    filename = 'output.mp3'
    with client.audio.speech.with_streaming_response.create(
        model='tts-1',
        voice='nova',
        input=response,
    ) as rest:
        rest.stream_to_file(filename)

    # 음원을 base64 문자열로 인코딩 처리
    with open('output.mp3', 'rb') as f:
        data = f.read()
        base64_encoded = base64.b64encode(data).decode()    # 이진 데이터 -> base64 인코딩(이진) -> 문자열로 디코딩

    os.remove(filename)
    return base64_encoded


