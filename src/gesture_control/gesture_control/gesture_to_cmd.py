from geometry_msgs.msg import Twist

def gesture_to_twist(gesture, speed=0.3):
    msg = Twist()

    if gesture=='forward':
        msg.linear.x = speed
    elif gesture=='backward':
        msg.linear.x = -speed
    elif gesture =='left':
        msg.linear.x = speed
        msg.angular.z = speed
    elif gesture == 'right':
        msg.linear.x = speed
        msg.angular.z = -speed
    
    return msg

# def update_speed(gesture, speed):
#     if gesture == 'speed_up':
#         speed = min(speed+0.1, 1.0) # 최대 1.0
#     elif gesture == 'speed_down':
#         speed = max(speed-0.1, 0.1) # 최소 0.1
#     return speed 
