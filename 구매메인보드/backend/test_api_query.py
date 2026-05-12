import requests
import json

API_KEY = "dc6036868177c098f44b4a6af509bf85c33e30f602e8895a0a51908879970845"
API_URL_BASE = "https://apis.data.go.kr/1230000/ao/PriceInfoService"

def test_query(operation, params):
    url = API_URL_BASE + "/" + operation
    params["serviceKey"] = API_KEY
    params["type"] = "json"
    
    try:
        response = requests.get(url, params=params, timeout=5)
        print(f"\n=== Test: {operation} ===")
        print(f"Status: {response.status_code}")
        
        # 1. UTF-8로 디코딩 시도
        try:
            decoded_data = response.content.decode('utf-8')
            data = json.loads(decoded_data)
            print("성공: UTF-8 디코딩")
        except Exception as e:
            print(f"실패: UTF-8 디코딩 ({e})")
            # 2. EUC-KR로 디코딩 시도
            try:
                decoded_data = response.content.decode('euc-kr')
                data = json.loads(decoded_data)
                print("성공: EUC-KR 디코딩")
            except Exception as e2:
                print(f"실패: EUC-KR 디코딩 ({e2})")
                return
                
        items = data.get("response", {}).get("body", {}).get("items", [])
        if items:
            item = items[0]
            # 출력 시 에러 방지를 위해 repr 사용
            print(f"품명 (repr): {repr(item.get('prdnm'))}")
            print(f"규격 (repr): {repr(item.get('spec'))}")
            
            # 직접 출력 시도 (에러 무시)
            try:
                print(f"품명: {item.get('prdnm')}")
            except:
                print("품명 출력 실패 (인코딩 에러)")
        else:
            print("No items found.")
            
    except Exception as e:
        print(f"Error: {e}")

test_query("getStdMarkUprcinfoList", {
    "numOfRows": 5,
    "pageNo": 1,
    "inqryDiv": "1",
    "inqryBgnDate": "20230101",
    "inqryEndDate": "20231231"
})
