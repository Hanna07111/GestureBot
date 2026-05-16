import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

from gesture_control.gesture_classifier import recognize_gesture
from gesture_control.gesture_to_cmd import gesture_to_twist

MODEL_PATH = os.path.expanduser('~/motionbot_ws/hand_landmarker.task')

class GestureContoller(Node):
    def __init__(self):
        super().__init__('gesture_controller')

        # 상태 변수 추가
        self.speed = 2.0
        
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # 웹캠 열기
        self.cap = cv2.VideoCapture(0)

        # MediaPipe Tasks 초기화 (Task API 활용)
        base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
        self.detector = vision.HandLandmarker.create_from_options(options)

        # 0.05에 한 번씩 프레임 읽기
        self.time = self.create_timer(0.05, self.process_frame)

    # 프레임 읽기
    def process_frame(self):
        ret, frame = self.cap.read()

        # 읽혀진 프레임 없으면 그냥 넘어감
        if not ret:
            return

        # frame bgr -> rgb (mediapipe는 rgb로 인식)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # frame을 mp.Image로 감싸기
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        # hand landmark detecting
        result = self.detector.detect(mp_image)
        msg = Twist()

        if result.hand_landmarks:
            # 인식한 손 landmark 그리기
            for hand_landmark in result.hand_landmarks:
                for lm in hand_landmark:
                    h, w, _ = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

            # 제스처 인식
            gesture = recognize_gesture(result.hand_landmarks[0])

            # 제스처에 따라 로봇 제어
            msg = gesture_to_twist(gesture, self.speed)

        # 손동작을 아무것도 인식하지 못했을 경우
        else: 
            msg = gesture_to_twist('stop', self.speed)
        
        # msg publish
        self.publisher.publish(msg)
        cv2.imshow('Gesture Control', frame)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = GestureContoller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
