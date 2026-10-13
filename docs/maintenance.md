# 포트폴리오 관리

사이트 수정·검사·배포를 위한 관리 문서. 아래 파일 경로는 저장소 루트 기준.

- 사이트: https://jeong-yun-kim.github.io/
- 저장소: https://github.com/Jeong-Yun-Kim/Jeong-Yun-Kim.github.io

## 설치와 로컬 실행

Node.js 24와 npm 사용. `.nvmrc` 제공.

```bash
npm ci
npm run dev
```

터미널에 표시되는 로컬 주소 접속. 기본 포트는 4321.

## 검사와 빌드

```bash
npm run check
npm run build
npm run validate
# 위 세 단계 한 번에 실행
npm run verify
```

`dist/`에 정적 HTML·CSS·이미지 생성. `npm run preview`로 빌드 결과 확인.

`validate`는 생성된 모든 HTML의 내부 링크·앵커·이미지, 제목 구조, 주요 SEO 태그, 외부 링크 속성, 일부 개인정보 패턴과 임시 문구를 검사한다. 실제 브라우저·실기기 확인을 대체하지 않는다.

## 배포

저장소는 public이며 Settings → Pages → Source가 **GitHub Actions**로 설정되어 있다.

```bash
# 처음 내려받기
git clone https://github.com/Jeong-Yun-Kim/Jeong-Yun-Kim.github.io.git
cd Jeong-Yun-Kim.github.io
npm ci
# 콘텐츠 수정 후 검사·반영
npm run verify
git add .
git commit -m "Update portfolio content"
git push origin main
```

이후 `main`에 push할 때마다 타입 검사·빌드·링크 검증 후 자동 배포된다. Actions 탭의 **Deploy portfolio to GitHub Pages**에서 수동 실행도 가능하다. Pull request에서는 배포 없이 빌드·검증만 실행한다. Node.js 24와 Ubuntu 24.04를 사용한다.

`astro.config.mjs`의 `site`는 위 기본 주소, `base`는 `/`이다. 사용자 Pages 저장소이므로 저장소 이름을 base path에 넣지 않는다. 각 경로는 `index.html`이 있는 디렉터리로 출력되어 상세 페이지 직접 접속·새로고침을 지원한다. 존재하지 않는 경로는 `/404.html`을 사용한다.

## 콘텐츠 수정

| 수정 대상 | 파일 |
| --- | --- |
| 소개·공개 연락처·활동·수상·기술 | `src/data/profile.ts` |
| 대표 프로젝트 상세 콘텐츠 | `src/data/projects.json` |
| 아카이브·학습 저장소 | `src/data/archive.ts` |
| 이력서 레이아웃 | `src/pages/resume.astro` |
| 전체 디자인·반응형·인쇄 | `src/styles/global.css` |
| 공통 메뉴·SEO | `src/layouts/Base.astro` |

이력서와 홈은 동일한 프로필·프로젝트 데이터를 사용한다. 이력서 화면의 **인쇄 / PDF 저장** 버튼 또는 브라우저 인쇄 기능 사용. 인쇄 시 메뉴·버튼·Footer가 숨겨지고 A4용 스타일이 적용된다.

## 프로젝트 추가

`src/data/projects.json`의 기존 항목을 복사하여 다음 필드를 실제 근거로 수정한다. 필드 형식은 `src/data/types.ts`의 `Project` 참조.

1. `slug`: 중복되지 않는 영어 소문자와 하이픈. `/projects/<slug>/`가 자동 생성됨.
2. `title`, `summary`, `period`, `periodNote`, `team`, `role`, `status`: 실제 개발 기록에 맞게 작성.
3. `overview`부터 `evaluation`, `results`, `limits`: 구현·개인 역할·검증 조건·한계 구분.
4. `metrics`: 측정 근거가 있을 때만 입력. 없으면 빈 배열 `[]`.
5. `links`: 일반 방문자가 접근할 수 있는 GitHub·시연·문서 주소만 입력.
6. `image`, `imageAlt`, `imageCaption`: 실제 화면·사진 또는 정확한 구성도 사용.
7. `featured`: 대표 여부. 홈에서는 `true`만 표시되며 검증 스크립트가 4–6개를 요구함.

대표 외 프로젝트도 상세 데이터를 추가할 수 있다. 아카이브 페이지의 대표 목록은 `featured`를 기준으로 표시된다. 간단한 기록만 필요한 프로젝트는 `src/data/archive.ts`에 추가.

## 이미지 추가

파일을 `public/images/`에 저장하고 `/images/파일명.webp`처럼 참조한다. 사진·화면은 WebP, 정확한 도식은 SVG 권장. 의미 있는 영문 파일명과 설명형 alt를 사용한다. 브라우저 주소창·즐겨찾기·개인 연락처 등 불필요한 정보는 포함하지 않는다. 원본 비공개 영상과 연구 자료를 저장소에 복사하지 않는다.

현재 사진·화면은 제공된 CausalRoboQC 시연 영상에서 필요한 프레임만 발췌·압축한 자료다. 도식은 공개 코드·개발 기록을 토대로 제작했다. Open Graph 커버는 `/images/og-cover.png`, favicon은 `/favicon.svg`.

## 공개 범위와 유지보수

- 사용자가 공개 연락처로 지정한 이메일을 사용. 전화번호·주소·학번·사적 기록·비공개 코드는 제외.
- 비공개 저장소는 접근 불가능한 GitHub 버튼 대신 공개 가능한 설명만 제공.
- CARLA NMPC 설계와 Stock 실측 결과, CausalRoboQC 합성 데이터와 실기기 검증, Mirobot 기존 시연과 최신 분리본의 상태를 구분.
- 상세 기준과 제외 항목은 `docs/content-review.md` 참조.
- 테스트 수치는 원본 프로젝트 기록이며 사이트 구축 시 재실행한 결과가 아님.
- 프로젝트 데이터 갱신 후 `npm run verify` 실행 및 브라우저 확인.
- GitHub Pages 공식 워크플로 문서: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## 주요 구조

```text
src/
  components/       공통 프로젝트·링크 표시
  data/             프로필·프로젝트 콘텐츠
  layouts/          공통 HTML·메타데이터
  pages/            홈·소개·아카이브·상세·이력서·404
  styles/           화면·인쇄 스타일
public/             실제 이미지·도식·favicon·robots
scripts/            생성 결과 검증
.github/workflows/  빌드·검증·배포
docs/               콘텐츠 검토·유지보수 기록
```

