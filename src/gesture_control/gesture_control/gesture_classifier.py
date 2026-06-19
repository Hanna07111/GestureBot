import math

# 두 지점 사이의 거리 계산
def distance(a,b):
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

# 손가락이 위로 펴져있는지 확인 (y는 작을 수록 위쪽)
def is_finger_up(landmarks, tip, pip):
    return landmarks[tip].y < landmarks[pip].y 

# 손가락이 펴져있는지 확인
def is_finger_extended(landmarks, tip, mcp):
    return distance(landmarks[tip], landmarks[mcp]) > 0.1   

def recognize_gesture(hand_landmarks):
    lm = hand_landmarks

    # 엄지 up&down
    # 엄지가 위(아래)를 향함 + 손목보다 위(아래)에 있음
    thumb_up = lm[4].y < lm[3].y and lm[4].y < lm[0].y
    thumb_down = lm[4].y > lm[3].y and lm[4].y > lm[2].y

    # 나머지 손가락 위로 펴져있는지 측정
    index_up = is_finger_up(lm,8,6) #검지 
    middle_up = is_finger_up(lm,12,10) #중지
    ring_up = is_finger_up(lm,16,14) #약지
    pinky_up = is_finger_up(lm,20,18) #새끼

    # 각 손가락이 펴져있는지 확인
    index_extended = is_finger_extended(lm, 8, 5)
    middle_extended = is_finger_extended(lm, 12, 9)
    ring_extended = is_finger_extended(lm, 16, 13)
    pinky_extended = is_finger_extended(lm, 20, 17)

    # 엄지-검지 거리 측정
    thumb_index_close = distance(lm[4], lm[8]) < 0.05

    # 속도 증/감
    # 화면 상단에 손이 있으면 -> 속도 증가
    if lm[0].y < 0.33:
        return 'speed_up'

    # 화면 하단에 손이 있으면 -> 속도 감소
    if lm[0].y > 0.9:
        return 'speed_down'

    # OK 제스처: 엄지-검지 거리 가깝고, 나머지 손가락 펴짐 -> 정지
    if thumb_index_close and middle_up and ring_up and pinky_up:
        return 'stop'

    # V자: 검지 + 중지 -> 직진
    if index_up and middle_up and not ring_up and not pinky_up:
        return 'forward'
    
    # 손바닥 펼치기: 모든 손가락이 펴짐 -> 후진
    if all([thumb_up, index_up, middle_up, ring_up, pinky_up]):
        return 'backward'

    # 오른쪽을 가리킴: 검지 손가락이 오른쪽을 가리킴-> 오른쪽으로 회전 
    # 왼쪽을 가리킴: 검지 손가락이 왼쪽을 가리킴 -> 왼쪽으로 회전
    if index_extended and not middle_extended and not ring_extended and not pinky_extended:
        if lm[0].x < lm[8].x:
            return 'right'
        else:
            return 'left'

    
    # Nav2 
    # 세 손가락 들기 -> 목표지점까지 자율주행
    if index_up and middle_up and ring_up and not pinky_up:
        return 'goal'

    
    # # 주먹: 모든 손가락이 접힘 -> 정지
    # if not any([thumb_up, index_up, middle_up, ring_up, pinky_up]):
    #     return 'stop'

    # # 앞을 가리킴: 검지만 펴짐 -> 직진
    # if index_up and not thumb_up and not middle_up and not ring_up and not pinky_up:
    #     return 'forward'