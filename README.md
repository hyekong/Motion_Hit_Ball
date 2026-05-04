# OpenCV 기반 비전 실시간 모션 인터랙션 게임 🎯

JetRover 로봇 카메라와 OpenCV를 활용한 실시간 모션 감지 게임

---

## 프로젝트 개요

JetRover 로봇에 탑재된 카메라로부터 실시간 영상을 입력받아, OpenCV 기반의 영상처리 파이프라인을 구축하여 모션 인터랙션 게임을 구현하였습니다.

원본 영상을 그레이스케일로 변환하여 연산량을 줄이고, 가우시안 블러를 적용하여 카메라 노이즈를 제거한 뒤, 연속 프레임 간 차분(absdiff)과 이진화(threshold)를 통해 움직임이 발생한 영역을 객체로 추출합니다. 추출된 움직임 객체와 화면 내 공의 ROI 영역을 비교하여 충돌 여부를 실시간으로 판정합니다.

---

## 시연 영상

> 추후 GIF 또는 영상 링크 추가 예정

---

## 주요 기능

- **실시간 모션 감지** — 연속 프레임 간 픽셀 차이를 비교하여 움직임 검출
- **ROI 기반 충돌 판정** — 공 주변 영역에서 움직임 비율이 10% 초과 시 터치 인정
- **터치 감지 시 효과** — 충돌 지점에서 파티클이 사방으로 퍼지며 소멸, 공 색상 랜덤 변경

---

## 기술 스택

| 구분 | 내용 |
|------|------|
| 언어 | Python 3 |
| 라이브러리 | OpenCV (cv2) |
| 장비 | JetRover (Jetson Nano B01 / HD Camera / ROS) |

---

## 알고리즘 (5단계 파이프라인)

### [1단계] OpenCV VideoCapture를 통한 영상 입력

```python
capture = cv2.VideoCapture(0)
```

### [2단계] 좌우 반전 → 그레이스케일 변환 → 가우시안 블러(노이즈 제거)

```python
frame = cv2.flip(frame, 1)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray_frame = cv2.GaussianBlur(gray, (21, 21), 0)
```

### [3단계] 이전 프레임과 차분(absdiff) → 이진화(threshold)

```python
diff_frame = cv2.absdiff(pre_gray_frame, gray_frame)
_, thresh_frame = cv2.threshold(diff_frame, 25, 255, cv2.THRESH_BINARY)
```

### [4단계] ROI 영역 움직임 판정

```python
cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
roi = thresh_frame[y1:y2, x1:x2]
movement_pixel = cv2.countNonZero(roi)

area = (x2 - x1) * (y2 - y1)
if area > 0 and movement_pixel > area * 0.1:
    score += 1
```

### [5단계] 파티클 생성 및 색상 변경

```python
for i in range(10):
    p = Particle(red_ball.x, red_ball.y, red_ball.color)
    particles.append(p)

red_ball.color = get_random_color()
```

---

## 프로젝트 구조

```
Motion_Hit_Ball/
├── hit_ball_v2.py    # 메인 게임 코드
└── README.md
```

---

## 설치 및 실행

### 요구 사항

- Python 3.7 이상
- JetRover 로봇 (또는 웹캠)

### 설치

```bash
pip install opencv-python
```

### 실행

```bash
python hit_ball_v2.py
```

카메라 앞에서 손을 움직여 공을 터치하세요. **ESC** 키를 누르면 종료됩니다.

---

## 결과

JetRover 로봇에 탑재된 카메라와 OpenCV를 활용하여, 별도의 센서 없이 사용자의 움직임을 실시간으로 감지하는 인터랙티브 게임을 구현하였습니다. 일반 웹캠이 아닌 실제 로봇 환경의 영상 입력을 활용하여 로봇과 사용자 간의 상호작용 가능성을 확인하였습니다.

---

## 향후 계획

- JetRover 로봇 팔(6DOF)과 연동하여 공 위치에 따라 로봇 팔이 물리적으로 반응하는 기능 추가
- 3D 깊이 카메라를 활용한 거리 기반 난이도 조절 시스템 도입

---

## 라이선스

MIT License
