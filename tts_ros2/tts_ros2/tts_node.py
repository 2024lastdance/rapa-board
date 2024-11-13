import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import subprocess

class TTSListener(Node):
    def __init__(self):
        super().__init__('tts_listener')

        # ROS2 토픽 구독
        self.subscription = self.create_subscription(
            String,
            'gui_text',  # 원본 텍스트 토픽
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning

        # 텍스트를 발행할 새로운 퍼블리셔 추가
        self.publisher_ = self.create_publisher(String, 'dynamic_text', 10)  # 새로 발행할 토픽

    def listener_callback(self, msg):
        text = msg.data  # 메시지에서 텍스트 추출
        self.get_logger().info(f'Received message: "{text}"')

        # espeak를 사용하여 TTS 처리
        if text == "따라와" or text == "달아 와" or text == "가람 화" \
        or text == "하라 와" or text == "단어" or text == "더러워" \
        or text == "더라고요" or text == "날아와":
            subprocess.run(['espeak', "따라가겠습니다"])
            processed_msg = String()
            processed_msg.data = "follow"  # 동일한 텍스트를 발행
            self.publisher_.publish(processed_msg)
            self.get_logger().info(f'Published processed message: follow')
            
        if text == "멈춰" or text == "엄청" or text == "온천" \
        or text == "몸채" or text == "헌터" or text == "홈쳐" \
        or text == "정직" or text == "성직" or text == "상지" \
        or text == "없 죠" or text == "었죠" or text == "정지":
            subprocess.run(['espeak', "멈추겠습니다."])
            processed_msg = String()
            processed_msg.data = "stop"  # 동일한 텍스트를 발행
            self.publisher_.publish(processed_msg)
            self.get_logger().info(f'Published processed message: stop')

def main(args=None):
    rclpy.init(args=args)

    tts_listener = TTSListener()

    rclpy.spin(tts_listener)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
