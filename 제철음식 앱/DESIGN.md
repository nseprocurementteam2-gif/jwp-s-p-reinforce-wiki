# Season Quest Design System: Cottagecore Discovery

## 1. 개요 (Overview)
'Season Quest'는 제철 음식 발견과 수집을 'Cottagecore Gamification' 컨셉으로 풀어낸 프리미엄 앱입니다. 모든 인터페이스는 마치 따뜻한 정원이나 정성스럽게 꾸민 스크랩북을 만지는 듯한 **촉각적(Tactile)**이고 **포근한(Cozy)** 경험을 제공합니다.

- **브랜드 페르소나:** 빛나고, 양육하며, 풍성함 (Radiant, Nurturing, Abundant)
- **핵심 키워드:** RPG 어드벤처, 전원생활(Cottagecore), 말랑말랑한 인터랙션(Squishy), 소장 가치

## 2. 디자인 원칙 (Design Principles)
1. **촉각적 즐거움 (Tactile Joy):** 모든 버튼과 카드는 물리적인 깊이감(border-b-4)을 가지며, 클릭 시 실제로 눌리는 듯한 애니메이션을 제공합니다.
2. **유기적 입체감 (Organic Depth):** 부드러운 파스텔 톤의 배경과 대비되는 선명한 하이라이트를 통해 정보의 계층을 입체적으로 표현합니다.
3. **보상형 탐험 (Rewarding Exploration):** 퀘스트 완성, 배지 수집, 실시간 알람 등 게임 요소를 UI 곳곳에 배치하여 사용자의 행동을 유도합니다.

## 3. 컬러 팔레트 (Color Palette)
| 구분 | 색상명 | 코드 | 용도 |
| :--- | :--- | :--- | :--- |
| **Primary** | Soft Mint | `#346859` | 성장, 채소, 주요 액션 버튼 |
| **Secondary** | Sunny Yellow | `#765B06` | 보상, 성취, 특산물 알람 |
| **Tertiary** | Peach Blossom | `#874F4C` | 과일, 단백질, 컬렉션 하이라이트 |
| **Background** | Warm Paper | `#FAF9F6` | 전체 배경, 종이 질감의 중립색 |
| **Container** | Fresh Sprout | `#B4EBD8` | 상단 바, 프로필 배경 |

## 4. 타이포그래피 (Typography)
- **Primary Font:** `Plus Jakarta Sans`
  - 기하학적이고 둥근 서체를 사용하여 낙천적이고 현대적인 느낌을 줍니다.
  - Headlines: Extra Bold (800-900)로 설정하여 "퀘스트 제목" 같은 힘을 줍니다.
  - Body: Medium (500)으로 가독성과 따뜻함을 유지합니다.

## 5. 주요 UI 요소 (Key Elements)
- **Bento Grid:** 정보의 중요도에 따라 크기가 다른 카드들을 배치하여 시각적 리듬감을 줍니다.
- **3D Press Buttons:** 하단에 4px의 짙은 테두리를 두어 입체감을 주고, 클릭 시 `translate-y-1` 효과를 적용합니다.
- **Tonal Layers:** 검은색 그림자 대신 배경색의 짙은 톤을 사용하여 부드러운 깊이감을 표현합니다.
- **Micro-Animations:** 티커(Ticker) 스크롤, 알람 모달의 펄스 효과 등을 통해 살아있는 듯한 인터페이스를 구현합니다.

---
*Last Updated: 2026-05-08 by Youngja (Antigravity)*
