

import binascii
import pickle


if __name__ == "__main__":
    # 데이터베이스에서 가져온 직렬화된 결과를 바이트로 전환한다.
    serialized_result = binascii.unhexlify("80054B032E")

    result = pickle.loads(serialized_result)

    print(result)