<template>
  <div class="flex flex-col h-full w-full bg-[#ECF6FF] font-sans">
    <!-- 상단 고정 영역 -->
    <div class="relative flex-shrink-0" style="height: 265px">
      <button
        @click="goBack"
        class="absolute top-[30px] left-[37px] flex h-[47px] w-[111px] items-center justify-center rounded-[20px] bg-[#327BDF] text-center text-[22px] font-bold text-white"
      >
        뒤로가기
      </button>
      <h1
        class="absolute top-[95px] left-[30px] font-pretendard text-[56px] font-bold leading-[67px] text-black"
      >
        복지센터 목록
      </h1>
      <div class="absolute top-[180px] left-[30px] h-[58px] w-[324px]">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="복지센터 검색"
          @input="filterCenters"
          class="h-full w-full rounded-[20px] border border-black bg-white py-2 pl-5 pr-[80px] text-[26px] font-normal text-[#6F6F6F] placeholder-[#6F6F6F] focus:outline-none"
        />
        <button
          @click="filterCenters"
          class="absolute right-[0px] top-[0px] flex h-full w-[68px] items-center justify-center rounded-[20px] bg-[#D9D9D9]"
        >
          <span class="text-center text-[19px] font-bold text-black">검색</span>
        </button>
      </div>
    </div>

    <!-- 카드+페이지네이션 묶음 -->
    <div class="flex flex-col flex-1 items-center justify-between min-h-0">
      <div class="w-full flex-1 overflow-y-auto px-5 space-y-5">
        <WelfareCenterCard v-for="center in paginatedCenters" :key="center.id" :center="center" />
      </div>
      <div class="mt-4 mb-4 flex justify-center space-x-2">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
        >
          이전
        </button>
        <span class="px-4 py-2 text-gray-600">{{ currentPage }} / {{ totalPages }}</span>
        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
        >
          다음
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import WelfareCenterCard from '@/components/WelfareCenterCard.vue'

export default {
  name: 'WelfareCenterList',
  components: {
    WelfareCenterCard,
  },
  data() {
    return {
      centers: [],
      searchQuery: '',
      currentPage: 1,
      itemsPerPage: 10,
    }
  },
  computed: {
    filteredCenters() {
      if (!this.searchQuery) return this.centers
      const query = this.searchQuery.toLowerCase()
      return this.centers.filter(
        (center) =>
          center.name.toLowerCase().includes(query) ||
          center.address.toLowerCase().includes(query) ||
          (center.type && center.type.toLowerCase().includes(query))
      )
    },
    paginatedCenters() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      return this.filteredCenters.slice(start, start + this.itemsPerPage)
    },
    totalPages() {
      return Math.ceil(this.filteredCenters.length / this.itemsPerPage) || 1
    },
  },
  methods: {
    async fetchCenters() {
      try {
        const response = await axios.get('http://localhost:8000/api/welfare/centers/')
        this.centers = response.data
      } catch (error) {
        console.error('Error fetching welfare centers:', error)
      }
    },
    filterCenters() {
      this.currentPage = 1
    },
    goBack() {
      this.$router.go(-1)
    },
  },
  mounted() {
    this.fetchCenters()
  },
}
</script>

<style scoped>
.font-pretendard {
  font-family: 'Pretendard', sans-serif;
}
</style>
