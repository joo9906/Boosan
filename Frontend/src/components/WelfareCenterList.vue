<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">복지센터 목록</h2>
    <div class="mb-6">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="복지센터 검색..."
        @input="filterCenters"
        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
      />
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="center in paginatedCenters"
        :key="center.id"
        class="bg-white p-6 rounded-lg shadow-md"
      >
        <h3 class="text-xl font-semibold text-gray-800 mb-4">{{ center.name }}</h3>
        <p class="text-gray-600 mb-2">
          <span class="font-medium">주소:</span> {{ center.address }}
        </p>
        <p class="text-gray-600 mb-2">
          <span class="font-medium">전화번호:</span> {{ center.tel }}
        </p>
        <p class="text-gray-600"><span class="font-medium">유형:</span> {{ center.type }}</p>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div class="mt-8 flex justify-center space-x-2">
      <button
        @click="currentPage--"
        :disabled="currentPage === 1"
        class="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
      >
        이전
      </button>
      <span class="px-4 py-2 text-gray-600"> {{ currentPage }} / {{ totalPages }} </span>
      <button
        @click="currentPage++"
        :disabled="currentPage === totalPages"
        class="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
      >
        다음
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'WelfareCenterList',
  data() {
    return {
      centers: [],
      searchQuery: '',
      filteredCenters: [],
      currentPage: 1,
      itemsPerPage: 20,
    }
  },
  computed: {
    paginatedCenters() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredCenters.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredCenters.length / this.itemsPerPage)
    },
  },
  methods: {
    async fetchCenters() {
      try {
        const response = await axios.get('http://localhost:8000/welfare/centers/')
        this.centers = response.data
        this.filteredCenters = response.data
      } catch (error) {
        console.error('Error fetching welfare centers:', error)
      }
    },
    filterCenters() {
      if (!this.searchQuery) {
        this.filteredCenters = this.centers
      } else {
        const query = this.searchQuery.toLowerCase()
        this.filteredCenters = this.centers.filter(
          (center) =>
            center.name.toLowerCase().includes(query) ||
            center.address.toLowerCase().includes(query) ||
            center.type.toLowerCase().includes(query)
        )
      }
      this.currentPage = 1 // 검색 시 첫 페이지로 이동
    },
  },
  mounted() {
    this.fetchCenters()
  },
}
</script>

<style scoped>
.welfare-center-list {
  padding: 20px;
}

.search-box {
  margin-bottom: 20px;
}

.search-box input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.centers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.center-card {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.center-card h3 {
  margin-top: 0;
  color: #2c3e50;
}

.center-card p {
  margin: 5px 0;
  color: #666;
}
</style>
