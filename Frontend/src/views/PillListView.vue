<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">내가 등록한 약 목록</h2>

    <div v-if="pills.length === 0" class="text-gray-500">등록된 약이 없습니다.</div>

    <div v-else class="grid grid-cols-1 gap-4">
      <div v-for="pill in pills" :key="pill.id" class="p-4 border rounded shadow">
        <h3 class="text-lg font-semibold">{{ pill.name }} ({{ pill.type }})</h3>
        <p class="text-sm text-gray-500">등록일: {{ pill.date_added }}</p>
        <img v-if="pill.image" :src="pill.image" alt="약 이미지" class="mt-2 w-32" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const pills = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/medical/pills/', {
      withCredentials: true,
    })
    pills.value = response.data
  } catch (error) {
    console.error('약 목록 불러오기 실패', error)
  }
})
</script>
