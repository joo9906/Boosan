<script>
export default {
  name: 'App',
}
</script>

<template>
  <div class="min-h-screen flex flex-col font-['Noto_Sans_KR']">
    <nav class="bg-white shadow-md sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link
              to="/"
              class="text-2xl font-bold text-emerald-600 hover:text-emerald-700 transition-colors"
            >
              부산시 노인복지
            </router-link>
          </div>
          <div class="flex items-center space-x-8">
            <router-link
              to="/welfare-centers"
              class="text-gray-700 hover:text-emerald-600 hover:bg-gray-50 px-4 py-2 rounded-md font-medium transition-colors"
              active-class="text-emerald-600 bg-gray-50"
            >
              복지센터
            </router-link>
            <router-link
              to="/hospitals"
              class="text-gray-700 hover:text-emerald-600 hover:bg-gray-50 px-4 py-2 rounded-md font-medium transition-colors"
              active-class="text-emerald-600 bg-gray-50"
            >
              병원
            </router-link>
            <router-link
              to="/register"
              class="text-gray-700 hover:text-emerald-600 hover:bg-gray-50 px-4 py-2 rounded-md font-medium transition-colors"
              active-class="text-emerald-600 bg-gray-50"
            >
              회원가입
            </router-link>
            <router-link to="/quiz"> 퀴즈 풀러가기 </router-link>
          </div>
        </div>
      </div>
    </nav>
    <main class="flex-1 bg-gray-50 p-8">
      <div class="max-w-7xl mx-auto">
        <router-view />
      </div>
    </main>
  </div>
</template>

<style>
#app {
  font-family: 'Noto Sans KR', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #ffffff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.brand-link {
  color: #42b983;
  text-decoration: none;
  transition: color 0.3s;
}

.brand-link:hover {
  color: #3aa876;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: #2c3e50;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-link:hover {
  color: #42b983;
  background-color: #f8f9fa;
}

.nav-link.router-link-active {
  color: #42b983;
  background-color: #f8f9fa;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #f8f9fa;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    padding: 1rem;
  }

  .nav-brand {
    margin-bottom: 1rem;
  }

  .nav-links {
    width: 100%;
    justify-content: center;
    gap: 1rem;
  }
}
</style>
