import cv2
import random

# 사용자 Ball 클래스
class Ball(object):
    def __init__(self):
        super().__init__()
        print("Ball object is created")
        self.radius = 0
        (self.x, self.y) = (0, 0)
        self.is_active = False
        self.color = (0, 0, 255)  # 초기 색상 (빨강)
    def __del__(self):
        print("Ball object is deleted")

# 파티클 클래스
class Particle(object):
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.vx = random.uniform(-5, 5)   # x 방향 속도
        self.vy = random.uniform(-5, 5)   # y 방향 속도
        self.life = 15  # 남은 프레임 수

def get_random_position(frame_width, frame_height, radius):
    x = random.randint(radius, frame_width - radius)
    y = random.randint(radius, frame_height - radius)
    return (x, y)

def get_random_color():
    """랜덤 색상 생성 (BGR)"""
    b = random.randint(0, 255)
    g = random.randint(0, 255)
    r = random.randint(0, 255)
    return (b, g, r)

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    exit("Could not open webcam")

frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 공 초기화
red_ball = Ball()
red_ball.radius = 20
(red_ball.x, red_ball.y) = get_random_position(frame_width, frame_height, red_ball.radius)
red_ball.is_active = True

score = 0
pre_gray_frame = None
particles = []  # 파티클 리스트

while True:
    (ret, frame) = capture.read()
    if frame is None:
        print("Cannot capture frame")
        break

    # 좌우반전
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 가우시안 필터링 (노이즈 제거)
    gray_frame = cv2.GaussianBlur(gray, (21, 21), 0)

    # 첫 프레임 저장
    if pre_gray_frame is None:
        pre_gray_frame = gray_frame.copy()
        continue

    # 움직임 감지
    diff_frame = cv2.absdiff(pre_gray_frame, gray_frame)

    # 이진화
    _, thresh_frame = cv2.threshold(diff_frame, 25, 255, cv2.THRESH_BINARY)

    # 공과 충돌
    if red_ball.is_active:
        (x1, y1) = (max(0, red_ball.x - red_ball.radius),
                    max(0, red_ball.y - red_ball.radius))
        (x2, y2) = (min(frame_width, red_ball.x + red_ball.radius),
                    min(frame_height, red_ball.y + red_ball.radius))

        # ROI 영역 지정
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        roi = thresh_frame[y1:y2, x1:x2]

        # ROI 영역에서의 움직임
        movement_pixel = cv2.countNonZero(roi)

        # 민감도 설정
        area = (x2 - x1) * (y2 - y1)
        if area > 0 and movement_pixel > area * 0.1:
            score += 1
            print(f"터치 점수 : {score}")

            # ★ 파티클 생성 (충돌 위치에서 10개)
            for i in range(10):
                p = Particle(red_ball.x, red_ball.y, red_ball.color)
                particles.append(p)

            # 공 색상 변경
            red_ball.color = get_random_color()

            # 공 위치 재배치
            (red_ball.x, red_ball.y) = get_random_position(frame_width, frame_height, red_ball.radius)

    # 파티클 업데이트 및 그리기
    alive_particles = []
    for p in particles:
        p.x += p.vx
        p.y += p.vy
        p.life -= 1
        if p.life > 0:
            radius = max(1, p.life // 3)  # 점점 작아짐
            cv2.circle(frame, (int(p.x), int(p.y)), radius, p.color, -1)
            alive_particles.append(p)
    particles = alive_particles

    # 화면에 공 그리기
    cv2.circle(frame, (red_ball.x, red_ball.y), red_ball.radius, red_ball.color, -1)

    # 화면에 점수 표시
    cv2.putText(frame, f"Score : {score}", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Game", frame)
    pre_gray_frame = gray_frame.copy()

    if cv2.waitKey(20) == 27:
        break

capture.release()
cv2.destroyAllWindows()