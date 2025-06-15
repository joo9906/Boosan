<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">병원 목록</h2>
    <div class="mb-6">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="병원 검색..."
        @input="filterHospitals"
        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
      />
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="hospital in paginatedHospitals"
        :key="hospital.id"
        class="bg-white p-6 rounded-lg shadow-md"
      >
        <h3 class="text-xl font-semibold text-gray-800 mb-4">{{ hospital.name }}</h3>
        <p class="text-gray-600 mb-2">
          <span class="font-medium">주소:</span> {{ hospital.address }}
        </p>
        <p class="text-gray-600 mb-2">
          <span class="font-medium">전화번호:</span> {{ hospital.tel }}
        </p>
        <p class="text-gray-600"><span class="font-medium">진료과목:</span> {{ hospital.type }}</p>
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
  name: 'HospitalList',
  data() {
    return {
      hospitals: [],
      searchQuery: '',
      filteredHospitals: [],
      currentPage: 1,
      itemsPerPage: 20,
    }
  },
  computed: {
    paginatedHospitals() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredHospitals.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredHospitals.length / this.itemsPerPage)
    },
  },
  methods: {
    async fetchHospitals() {
      try {
        const response = await axios.get('http://localhost:8000/medical/hospitals/')
        this.hospitals = response.data
        this.filteredHospitals = response.data
      } catch (error) {
        console.error('Error fetching hospitals:', error)
      }
    },
    filterHospitals() {
      if (!this.searchQuery) {
        this.filteredHospitals = this.hospitals
      } else {
        const query = this.searchQuery.toLowerCase()
        this.filteredHospitals = this.hospitals.filter(
          (hospital) =>
            hospital.name.toLowerCase().includes(query) ||
            hospital.address.toLowerCase().includes(query) ||
            hospital.type.toLowerCase().includes(query)
        )
      }
      this.currentPage = 1 // 검색 시 첫 페이지로 이동
    },
  },
  mounted() {
    this.fetchHospitals()
  },
}
</script>

<style scoped>
.hospital-list {
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

.hospitals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.hospital-card {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hospital-card h3 {
  margin-top: 0;
  color: #2c3e50;
}

.hospital-card p {
  margin: 5px 0;
  color: #666;
}
</style>
