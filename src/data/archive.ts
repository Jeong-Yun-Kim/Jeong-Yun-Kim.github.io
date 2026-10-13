export const archive = [
  { title: 'AI Rescue Box', category: '공간정보 · 개발 중', period: '2026.08 기록', summary: '사고 전 도면과 재난 후 공간지도를 비교하는 공간정보 모듈. 기존 포트폴리오에 RTAB-Map·nvblox 기반 SLAM과 도면 투영 시연을 정리했다.', note: '담당: 시스템 구성과 코드 개발. 정합 정확도·재난 환경 성능은 미확인. 소스는 비공개.', href: '/projects/ai-rescue-box/', linkLabel: '프로젝트 보기' },
  { title: 'TurtleBot3 UWB 위치 제어', category: 'ROS2 · 위치 제어', period: '2026.07 개발 기록', summary: 'UWB 위치와 odometry 방향을 이용한 stop-and-go 목표 위치 제어. 입력 freshness, 명시적 enable과 속도 출력 분리를 적용했다.', note: '장애물 회피와 정량 위치 정확도는 검증 범위에 포함되지 않음.', href: 'https://github.com/Jeong-Yun-Kim/Turtlebot_UWB', linkLabel: 'GitHub' },
  { title: 'UWB 양방향 통신 실험', category: 'Embedded · 통신', period: '2026.08 개발 기록', summary: 'ESP32·DWM1000에서 텍스트와 이미지 패킷을 전송하는 통신 실험. ACK·재시도·중복 억제·이미지 재조립을 구현했다.', note: 'PlatformIO CI 빌드 성공. 실제 통신·거리·처리량 시험은 미실행.', href: 'https://github.com/Jeong-Yun-Kim/UWB_Test', linkLabel: 'GitHub' },
  { title: '로봇 상태 업로더', category: 'ROS2 · HTTP', period: '2026.05 개발 기록', summary: '리더·팔로워 로봇의 배터리·속도·위치와 카메라 프레임을 HTTP로 전달하는 연결 모듈.', note: 'ROS2 상태 수집·JPEG 전송 코드 확인. 처리 성능 측정치는 제시하지 않음.', href: 'https://github.com/Jeong-Yun-Kim/robot_server', linkLabel: 'GitHub' },
];

export const studies = [
  { title: 'Baekjoon', description: '알고리즘 문제 풀이 기록', url: 'https://github.com/Jeong-Yun-Kim/Baekjoon' },
  { title: 'C++ 학습', description: 'STL과 시간 복잡도 정리', url: 'https://github.com/Jeong-Yun-Kim/coding_test_cpp' },
  { title: 'OpenCV 학습', description: '영상 처리 기초 실습', url: 'https://github.com/Jeong-Yun-Kim/Coding' },
];
