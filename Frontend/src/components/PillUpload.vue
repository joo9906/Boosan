<template>
  <div class="max-w-2xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-6">약 등록</h1>

    <div class="bg-white p-6 rounded-lg shadow-md">
      <!-- 이미지 업로드 섹션 -->
      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-bold mb-2"> 약봉투 사진 </label>
        <div
          class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center"
          @dragover.prevent
          @drop.prevent="handleDrop"
          :class="{ 'border-emerald-500': isDragging }"
        >
          <input
            type="file"
            accept="image/*"
            @change="handleFileUpload"
            class="hidden"
            ref="fileInput"
          />
          <div class="space-y-4">
            <div class="text-gray-500">
              <svg class="mx-auto h-12 w-12" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              <p class="mt-2">이미지를 드래그하거나 클릭하여 업로드하세요</p>
              <p class="text-sm">지원 형식: JPG, PNG, GIF</p>
            </div>
            <button
              @click="$refs.fileInput.click()"
              class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
            >
              파일 선택
            </button>
          </div>
        </div>
      </div>

      <!-- 이미지 미리보기 -->
      <div v-if="previewUrl" class="mb-6">
        <div class="relative">
          <img :src="previewUrl" alt="약봉투 미리보기" class="max-w-full h-auto rounded-lg" />
          <button
            @click="clearImage"
            class="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full hover:bg-red-600"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- 상태 메시지 -->
      <div v-if="uploadStatus" class="mb-4 p-4 rounded-lg" :class="uploadStatusClass">
        {{ uploadStatus }}
      </div>

      <!-- 업로드 버튼 -->
      <button
        @click="uploadPill"
        :disabled="!selectedFile || isUploading"
        class="w-full bg-emerald-600 text-white py-3 px-4 rounded-lg hover:bg-emerald-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors duration-200"
      >
        <span v-if="isUploading" class="flex items-center justify-center">
          <svg
            class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          업로드 중...
        </span>
        <span v-else>약 등록하기</span>
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PillUpload',
  data() {
    return {
      selectedFile: null,
      previewUrl: null,
      uploadStatus: '',
      isUploading: false,
      isDragging: false,
    }
  },
  computed: {
    uploadStatusClass() {
      return {
        'bg-green-100 text-green-700': this.uploadStatus.includes('완료'),
        'bg-red-100 text-red-700': this.uploadStatus.includes('오류'),
        'bg-blue-100 text-blue-700': this.uploadStatus.includes('중'),
      }
    },
  },
  methods: {
    handleDrop(e) {
      this.isDragging = false
      const file = e.dataTransfer.files[0]
      if (file && file.type.startsWith('image/')) {
        this.processFile(file)
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.processFile(file)
      }
    },
    processFile(file) {
      // 파일 크기 체크 (5MB 제한)
      if (file.size > 5 * 1024 * 1024) {
        this.uploadStatus = '파일 크기는 5MB를 초과할 수 없습니다.'
        return
      }

      // 파일 형식 체크
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
      if (!allowedTypes.includes(file.type)) {
        this.uploadStatus = '지원하지 않는 이미지 형식입니다.'
        return
      }

      this.selectedFile = file
      this.previewUrl = URL.createObjectURL(file)
      this.uploadStatus = ''
    },
    clearImage() {
      this.selectedFile = null
      this.previewUrl = null
      this.uploadStatus = ''
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
    },
    async uploadPill() {
      if (!this.selectedFile) return

      this.isUploading = true
      this.uploadStatus = '업로드 중...'

      const formData = new FormData()
      formData.append('image', this.selectedFile)

      try {
        const response = await axios.post('http://localhost:8000/medical/pillupload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })

        this.uploadStatus = `업로드 완료: ${response.data.name} (${response.data.type})`
        this.clearImage()

        // 3초 후 상태 메시지 초기화
        setTimeout(() => {
          this.uploadStatus = ''
        }, 3000)
      } catch (error) {
        console.error('Upload error:', error)
        this.uploadStatus = error.response?.data?.error || '업로드 중 오류가 발생했습니다.'
      } finally {
        this.isUploading = false
      }
    },
  },
}
</script>

<style scoped>
.border-dashed {
  border-style: dashed;
}
</style>
