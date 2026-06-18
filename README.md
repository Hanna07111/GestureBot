# GestureBot

손동작 기반 모바일 로봇 제어 시스템

---

## 패키지 구조

```
motionbot_ws/
├── src/
│   └── gesture_control/
│       ├── gesture_control/
│       │   ├── __init__.py
│       │   ├── gesture_classifier.py   # 제스처 분류 로직
│       │   ├── gesture_controller.py   # ROS2 메인 노드
│       │   ├── gesture_to_cmd.py       # 제스처 → cmd_vel 변환
│       │   └── nav_goal_publisher.py   # Nav2 목표 지점 전송
│       ├── launch/
│       │   └── gesture_control.launch.py
│       ├── package.xml
│       ├── setup.cfg
│       └── setup.py
├── hand_landmarker.task
├── maze_map.pgm
├── maze_map.yaml
└── set_params.sh
```

---

## 설치 방법

### 의존성 설치

```bash
# ROS2 TurtleBot4 관련
sudo apt install ros-humble-turtlebot4-simulator
sudo apt install ros-humble-turtlebot4-navigation

# Nav2
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup

# cv_bridge
sudo apt install ros-humble-cv-bridge

# Python 패키지
pip3 install mediapipe opencv-python 'numpy<2'
```

### MediaPipe 모델 다운로드

[hand_landmarker.task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)를 다운로드 후 `motionbot_ws/` 에 저장

### 빌드

```bash
cd ~/motionbot_ws
colcon build --symlink-install
source install/setup.bash
```

---

## 실행 방법

### 1. launch 파일 실행

```bash
ros2 launch gesture_control gesture_control.launch.py
```

### 2. 파라미터 설정

```bash
chmod +x set_params.sh
./set_params.sh
```

---

## GPU 설정 (NVIDIA + Intel 하이브리드)

```bash
# ~/.bashrc에 추가
export __NV_PRIME_RENDER_OFFLOAD=1
export __GLX_VENDOR_LIBRARY_NAME=nvidia
```
