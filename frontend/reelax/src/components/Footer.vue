<template>
  <footer class="footer">
    <div class="footer-links">
      <p>서비스 이용 약관 | 개인정보 처리방침 | 회사 안내</p>
      <p>고객센터 | ssafy@ssafy.com, 02-000-0000</p>
      <p>REELAX | 대표 홍길동 | 서울 강남구 테헤란로 212</p>
      <p>Copyright© REELAX All rights reserved.</p>
    </div>
    <div class="footer-icons">
      <font-awesome-icon :icon="['fab', 'instagram']" />
      <font-awesome-icon :icon="['fab', 'x-twitter']" />
      <font-awesome-icon :icon="['fab', 'google']" />
    </div>
  </footer>
</template>

<style scoped>
.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 20px;
  color: white;
  margin-top: 20px;
}

.footer-links p {
  margin: 0;
  padding: 5px 0;
}

.footer-icons {
  display: flex;
  gap: 10px;
}
</style>
