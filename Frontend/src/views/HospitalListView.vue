<template>
  <div class="relative mx-auto h-[844px] w-[390px] overflow-y-auto bg-[#ECF6FF] p-5 font-sans">
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
      병원 목록
    </h1>

    <!-- 검색창 -->
    <div class="absolute top-[180px] left-[30px] h-[58px] w-[324px]">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="병원 검색"
        @input="filterHospitals"
        class="h-full w-full rounded-[20px] border border-black bg-white py-2 pl-5 pr-[80px] text-[26px] font-normal text-[#6F6F6F] placeholder-[#6F6F6F] focus:outline-none"
      />
      <button
        @click="filterHospitals"
        class="absolute right-[0px] top-[0px] flex h-full w-[68px] items-center justify-center rounded-[20px] bg-[#D9D9D9]"
      >
        <span class="text-center text-[19px] font-bold text-black">검색</span>
      </button>
    </div>

    <!-- 병원 목록 -->
    <div class="mt-[265px] space-y-5">
      <HospitalCard v-for="hospital in filteredHospitals" :key="hospital.id" :hospital="hospital" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import HospitalCard from '@/components/HospitalCard.vue'

export default {
  name: 'HospitalList',
  components: {
    HospitalCard,
  },
  data() {
    return {
      hospitals: [],
      searchQuery: '',
      filteredHospitals: [],
    }
  },
  methods: {
    async fetchHospitals() {
      try {
        const response = await axios.get('http://localhost:8000/api/medical/hospitals/')
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
    },
    goBack() {
      this.$router.go(-1)
    },
  },
  mounted() {
    this.fetchHospitals()
  },
}
</script>

<style scoped>
.font-pretendard {
  font-family: 'Pretendard', sans-serif;
}
</style>
