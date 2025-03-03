# 동시 작업 수행은 파이썬에서 제공하는 cocurrent 모듈을 이용한다.
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


# 수행할 태스크를 request로 요청을 보낸다.
def send_request(var: str):
    response = requests.get(f"http://localhost:8000/context?var={var}")
    return response.json()


if __name__ == "__main__":
    # 최대 10개의 워커를 가진 스레드 풀을 생성해, 각 스레드에 요청을 할당한다.
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_request, str(i)) for i in range(10)]

    for future in as_completed(futures):
        print(future.result())
