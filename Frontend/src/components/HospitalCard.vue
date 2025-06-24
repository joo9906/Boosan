<template>
  <div class="h-[175px] w-[328px] rounded-[30px] bg-white p-6 shadow-md overflow-hidden">
    <p class="truncate font-pretendard text-[30px] font-normal leading-[36px] text-[#3589FD]">
      {{ hospital.type }}
    </p>
    <h3 class="mt-1 truncate font-pretendard text-[34px] font-bold leading-[41px] text-black">
      {{ hospital.name }}
    </h3>
    <p class="mt-1 truncate font-pretendard text-[19px] font-normal leading-[23px] text-[#6F6F6F]">
      {{ hospital.address }}
    </p>
    <p class="mt-1 font-pretendard text-[21px] font-normal leading-[25px] text-[#6F6F6F]">
      전화번호: {{ hospital.tel }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'HospitalCard',
  props: {
    hospital: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style scoped>
.font-pretendard {
  font-family: 'Pretendard', sans-serif;
}
</style>
