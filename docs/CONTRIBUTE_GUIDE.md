# 🖥️ Github 사용 방법

## 절대 master 브랜치에서 작업하지 않습니다

- 해당 레포지토리를 fork 하여 본인 Github 레포에서도 확인할 수 있어요 !
- 0번부터 6번까지 천천히 따라해보기 !
- 0번 ~ 1번 까지는 처음만 진행
- 이후로는 <code><b>(작업 전) 2번 ~ (작업 후) 5번</b></code> 까지 진행합니다.

## 🔑 0. 깃 레포 접근 권한 부여
1. GitHub에서 해당 레포지토리로 이동합니다
1. Settings 탭을 클릭합니다
1. 왼쪽 메뉴에서 Collaborators를 선택합니다
1. Collaborators 섹션에서 Add people 버튼을 클릭합니다
1. 팀원들의 GitHub 사용자 이름을 입력하고 Add를 클릭합니다
1. 팀원들이 초대를 수락하면 레포지토리에 접근하여 브랜치를 생성하고 PR을 할 수 있습니다

## 🛠️ 1. 깃 클론 받기
- fork를 받아 클론 받는 방법을 추천합니다
> 참고 사이트 : [[Github] 외부저장소 fork, pull, request, 동기화 하기](https://velog.io/@jisubin12/Github-%EC%99%B8%EB%B6%80%EC%A0%80%EC%9E%A5%EC%86%8C-fork-pull-request-%EB%8F%99%EA%B8%B0%ED%99%94-%ED%95%98%EA%B8%B0)
- 레포지토리를 처음 클론할 때 다음 명령어를 사용합니다<br>
    - [참고]  원하는 경로의 상위 폴더에서 clone 진행을 해야 상위 폴더에서 해당 레포지토리 이름명으로 된 폴더가 생성됨
> 예시) D:\ 에서 git clone 진행 시 D:\SSAFY_Algorithm_stduy\ 으로 clone 진행

```bash
git clone https://github.com/SorrowAddict/SSAFY_Algorithm_study.git
cd SSAFY_Algorithm_study
```

## ⚙️ 2. 작업 전 준비
- 작업을 시작하기 전에 master 브랜치에서 최신 코드를 반영합니다 (pull 작업)
> <code>git checkout <branch명></code>, <code>git switch <branch명></code> -> 해당 브랜치 접속<br>
<code>git pull origin <branch명></code> -> 원격 저장소(origin)에서 해당 브랜치의 최신 변경 사항을 가져옴
```bash
git checkout master
git switch master
git pull origin master
```

## 🌿 3. 브랜치 생성 및 작업
- 새로운 작업을 시작할 때는 브랜치를 생성하고 해당 브랜치로 이동합니다
- 브랜치명은 자유입니다 (이름으로 하셔도 되고 닉네임으로 하셔도 됩니다)
> <code>git switch -c <branch명></code> or <code>git checkout -b <branch명></code> -> 해당 브랜치를 생성하면서  접속</code><br>
> <code>git branch <branch명></code> -> 해당 브랜치 생성  <span style="color:red"><b>[초기에만 진행합니다]</b></span><br>
<code>git checkout <branch명></code> or <code>git switch <branch명></code> -> 해당 브랜치 접속
```bash
git branch <이 부분 branch명 변경!>
git checkout <이 부분 branch명 변경!>
```
예시)
```bash
git branch sorrowaddict
git checkout sorrowaddict
```

- <b>브랜치 생성 후 개인 이름 or 닉네임으로 된 <span style="color:red;">폴더 안에서만 작업</span>합니다</b>

## ✔️ 4. 작업 완료 후 스테이징, 커밋 및 푸시
- 개인 이름 or 닉네임으로 된 폴더를 제외한 곳에서 작업하고 PR merge 요청을 할 시 오류가 발생할 수 있음
    - 기본적으로 다른 폴더는 수정하지 않습니다
    - 오류 발생 시 MM !
- add, commit, push를 하기전에 <b>꼭 !</b> <code>git checkout <branch></code>를 통해 본인 브랜치에 접속했는 지 확인합니다
```bash
git add .
git commit -m "커밋 메세지"
git push origin <branch명>
```

## 📥 5. Pull Request (PR) 생성
- GitHub에서 브라우저를 열고 레포지토리로 이동한 후, 새로 푸시한 브랜치에서 Pull Request를 생성합니다
- 팀원들의 코드 리뷰 후, PR이 승인되면 master 브랜치에 merge합니다
- PR의 경우 1주일에 1번만 진행합니다

## 📝 6. 우리만의 Git Commit 규칙 (권고 사항)
- 파일명은 자유입니다
- git commit 메세지 양식은 기본적으로 <b>자유</b>입니다 !
- 따라서 자유롭게 커밋 메세지를 작성하셔도 됩니다 !!!

git commit -m "[문제출처] 문제번호 - 문제이름"

예시입니다  ->  <code>git commit -m "[BOJ] 2839 - 설탕배달"</code>

예시입니다  ->  <code>git commit -m "왜 이렇게 어려움 !!!!!"</code>

<br><br><br>

# 📚 [참고 사항] Git Commit 협업 규칙

### 🗂️ 커밋 메시지의 7가지 규칙
1. 제목과 본문을 빈 행으로 구분한다.
1. 제목은 50글자 이내로 제한한다.
1. 제목의 첫 글자는 대문자로 작성한다.
1. 제목 끝에는 마침표를 넣지 않는다.
1. 제목은 명령문으로 사용하며 과거형을 사용하지 않는다.
1. 본문의 각 행은 72글자 내로 제한한다.
1. 어떻게 보다는 무엇과 왜를 설명한다.
<br>

### 커밋 메세지 구조
```
// Header, Body, Footer는 빈 행으로 구분한다.
타입(스코프): 주제(제목) // Header(헤더)

본문 // Body(바디)

바닥글 // Footer
```

#### 사용 예시
```
git commit -m "fix: Safari에서 모달을 띄웠을 때 스크롤 이슈 수정

모바일 사파리에서 Carousel 모달을 띄웠을 때,
모달 밖의 상하 스크롤이 움직이는 이슈 수정.

resolves: #1137"
```

| **타입**   | **설명**                                     |
|------------|----------------------------------------------|
| `feat`     | 새로운 기능에 대한 커밋                      |
| `fix`      | 버그 수정에 대한 커밋                        |
| `build`    | 빌드 관련 파일 수정에 대한 커밋              |
| `chore`    | 그 외 자잘한 수정에 대한 커밋 (예: 설정 변경) |
| `ci`       | CI 관련 설정 수정에 대한 커밋               |
| `docs`     | 문서 수정에 대한 커밋                        |
| `style`    | 코드 스타일 혹은 포맷 등에 관한 커밋 (기능 변경 없음) |
| `refactor` | 코드 리팩토링에 대한 커밋 (기능 변경 없음)   |
| `test`     | 테스트 코드 추가 및 수정에 대한 커밋         |
<br>

Body는 Header에서 표현할 수 없는 상세한 내용을 적는다.

Header에서 충분히 표현할 수 있다면 생략 가능하다.

Footer는 바닥글로 어떤 이슈에서 왔는지 같은 참조 정보들을 추가하는 용도로 사용한다.

예를 들어 특정 이슈를 참조하려면 Issues #1234 와 같이 작성하면 된다.

Footer는 생략 가능하다.