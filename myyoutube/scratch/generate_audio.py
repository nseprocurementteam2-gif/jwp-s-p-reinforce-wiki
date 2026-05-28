import asyncio
import edge_tts
import ssl

# Bypass SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

async def generate_tts(text, output_file):
    voice = "ko-KR-SunHiNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

if __name__ == "__main__":
    texts = [
        "또 작심삼일인가요? 당신의 의지력이 약해서가 아닙니다. 설계가 잘못되었을 뿐입니다. 기억하세요. 우리는 목표의 수준까지 올라가는 게 아니라, 내가 만든 시스템의 수준까지 떨어집니다.",
        "첫 번째 오류, '미래의 나'를 너무 믿는 근거 없는 자신감입니다. 보통 예상보다 1.7배의 시간이 더 걸리죠. 100% 빽빽한 계획은 무조건 터집니다. 해결책은 '70%의 법칙'입니다. 딱 70%만 계획하고 나머지 30%는 여백으로 비워두세요. 완수했을 때의 성취감이 내일의 동력이 됩니다.",
        "두 번째 오류, 뇌를 고민하게 만드는 모호한 지시입니다. '영어 공부'처럼 막연한 계획은 결정 피로를 유발합니다. 해결책은 '스위치 행동 설계'입니다. 계획을 '동사, 대상, 수량'으로 쪼개세요. 저녁 먹고 커피 마시면 책상에 앉아 단어 10개 외운다처럼 상황과 행동을 엮으세요.",
        "세 번째 오류, '최상의 컨디션'만 생각한 완벽주의입니다. 계획이 무너지는 건 최악인 날을 계산하지 않았기 때문이죠. 해결책은 '최소한의 자존심' 루틴입니다. 아픈 날에도 5분만 책상에 앉아 책을 펴보세요. 흐름을 끊지 않는 것 자체가 강력한 성공 경험이 됩니다.",
        "완벽한 플래너를 기다리지 마세요. 대충, 빨리, 잘의 원칙을 기억하세요. 일단 70%만 적고 시작하는 것, 그것이 인생을 바꾸는 시스템의 시작입니다. 지금 바로 시작하세요."
    ]
    
    for i, text in enumerate(texts):
        output = f"scratch/audio_{i}.mp3"
        asyncio.run(generate_tts(text, output))
        print(f"Generated {output}")
