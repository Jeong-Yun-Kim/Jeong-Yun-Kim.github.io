export const profile = {
  name: '김정윤',
  englishName: 'Jeong-Yun Kim',
  focus: 'Robotics · Autonomous Driving · Backend',
  intro: 'ROS2, 로봇 제어, 자율주행 시뮬레이션과 서버 개발을 중심으로 프로젝트를 진행하고 있습니다.',
  about: '센서와 로봇의 동작을 연결하고, 작업 결과를 서버와 화면에서 확인할 수 있는 시스템을 만듭니다. 구현 과정과 검증 조건을 기록하며 하드웨어부터 API, 사용자 화면까지 연결하는 개발을 하고 있습니다.',
  education: '충북대학교 지능로봇공학과',
  educationPeriod: '2025.03 – 재학 중',
  github: 'https://github.com/Jeong-Yun-Kim',
  email: 'jeongyun061030@gmail.com',
  updated: '2026.10.13',
};

export const activities = [
  { period: '2026', title: '충청 ICT 이노베이션스퀘어 개발 역량 강화 멘토링', description: 'Double Click 팀으로 본선 10팀에 진출. CausalRoboQC의 기획과 로봇·서버·웹앱 통합 개발.', href: '/projects/causalroboqc/' },
  { period: '2026', title: 'Double Click 로봇 프로젝트', description: '로봇팔·비전·서버를 연결하는 프로젝트 진행. 리니어 이송 보관대 기반 자동 피킹 시스템의 구성과 개발 계획 정리.', href: '/projects/#research' },
  { period: '2025.03 –', title: '충북대학교 지능로봇공학과', description: '재학 중. 로봇 제어, 자율주행 시뮬레이션, 프로그래밍 프로젝트 수행.', href: '/about/' },
];

export const awards = [
  { year: '2025', scope: '교내', name: '지능로봇공학과 동아리 경진대회', result: '최우수상' },
  { year: '2025', scope: '교내', name: '자율주행 CAN 통신 실무 프로젝트 경진대회', result: '우수상' },
  { year: '', scope: '교내', name: '미래자동차 혁신융합사업단 자율주행 경진대회', result: '최우수상' },
];

export const skills = [
  { category: 'Robotics', names: ['ROS2', 'Python', 'C++', 'Serial'], evidence: '로봇팔 명령·상태 처리, 작업 시퀀스와 장비 간 통신 구현', href: '/projects/mirobot-ros2/' },
  { category: 'Autonomous Driving', names: ['CARLA', 'Autoware', 'Hybrid A*'], evidence: '주행·신호·주차 통합 시나리오와 평가 로깅 구성', href: '/projects/carla-autonomous-driving/' },
  { category: 'Vision', names: ['OpenCV', 'ArUco', 'YOLOv5'], evidence: '제품 ID 유지, Pick/Place 검증, 큐브 인식·좌표 처리', href: '/projects/causalroboqc/' },
  { category: 'Backend', names: ['FastAPI', 'SQLite', 'WebSocket'], evidence: '주문·공정 상태 관리, 제품 이력 저장과 실시간 화면 연동', href: '/projects/smart-factory-server/' },
  { category: 'Data & Interface', names: ['Flutter', 'scikit-learn', 'PyTorch', 'Ollama'], evidence: '제품 조회 웹앱, 합성 데이터 기반 보조 분석, DB 근거 기반 코파일럿', href: '/projects/causalroboqc/' },
  { category: 'Environment', names: ['Linux', 'Git', 'Docker Compose', 'Raspberry Pi'], evidence: '현장 서버와 노트북 AI 서버를 분리한 실행·통합 환경 구성', href: '/projects/causalroboqc/' },
];
