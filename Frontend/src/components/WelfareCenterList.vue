<template>
  <div class="relative mx-auto h-[844px] w-[390px] overflow-hidden bg-[#ECF6FF] p-5 font-sans">
    <!-- 뒤로가기 버튼 -->
    <button
      @click="goBack"
      class="absolute top-[30px] left-[37px] flex h-[47px] w-[111px] items-center justify-center rounded-[20px] bg-[#327BDF] text-center text-[22px] font-bold text-white"
    >
      뒤로가기
    </button>

    <!-- 페이지 제목 -->
    <h1
      class="absolute top-[95px] left-[30px] font-pretendard text-[56px] font-bold leading-[67px] text-black"
    >
      복지센터 목록
    </h1>

    <!-- 검색창 -->
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

    <!-- 복지센터 목록 -->
    <div
      class="absolute top-[265px] left-0 right-0 mx-auto h-[1750px] w-full overflow-y-auto px-5 space-y-5"
    >
      <WelfareCenterCard v-for="center in paginatedCenters" :key="center.id" :center="center" />
    </div>

    <!-- 페이지네이션 -->
    <div class="absolute left-0 right-0 bottom-4 flex justify-center space-x-2">
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
</template>

<script>
import WelfareCenterCard from '@/components/WelfareCenterCard.vue'

export default {
  components: { WelfareCenterCard },
  data() {
    return {
      centers: [],
      searchQuery: '',
      currentPage: 1,
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
      const start = (this.currentPage - 1) * 10
      return this.filteredCenters.slice(start, start + 10)
    },
    totalPages() {
      return Math.ceil(this.filteredCenters.length / 10) || 1
    },
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    filterCenters() {
      this.currentPage = 1
    },
  },
  mounted() {
    // 실제 API 연동 시 아래 부분을 axios로 교체
    this.centers = Array.from({ length: 30 }, (_, i) => ({
      id: i + 1,
      name: `복지센터 ${i + 1}`,
      address: `부산시 구군 ${(i % 5) + 1}`,
      type: `유형${(i % 3) + 1}`,
      tel: `051-0000-00${i + 1}`,
    }))
  },
}
</script>

<style scoped>
.font-pretendard {
  font-family: 'Pretendard', sans-serif;
}
</style>
