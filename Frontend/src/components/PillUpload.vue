<template>
  <div class="max-w-2xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-6">약 등록</h1>

    <div class="bg-white p-6 rounded-lg shadow-md">
      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-bold mb-2"> 약봉투 사진 </label>
        <input
          type="file"
          accept="image/*"
          @change="handleFileUpload"
          class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
      </div>

      <div v-if="previewUrl" class="mb-6">
        <img :src="previewUrl" alt="약봉투 미리보기" class="max-w-full h-auto rounded-lg" />
      </div>

      <div v-if="uploadStatus" class="mb-4 p-4 rounded-lg" :class="uploadStatusClass">
        {{ uploadStatus }}
      </div>

      <button
        @click="uploadPill"
        :disabled="!selectedFile || isUploading"
        class="w-full bg-emerald-600 text-white py-2 px-4 rounded-lg hover:bg-emerald-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {{ isUploading ? '업로드 중...' : '약 등록하기' }}
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
    }
  },
  computed: {
    uploadStatusClass() {
      return {
        'bg-green-100 text-green-700': this.uploadStatus.includes('완료'),
        'bg-red-100 text-red-700': this.uploadStatus.includes('오류'),
      }
    },
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.selectedFile = file
        this.previewUrl = URL.createObjectURL(file)
        this.uploadStatus = ''
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
        this.selectedFile = null
        this.previewUrl = null
      } catch (error) {
        console.error('Upload error:', error)
        this.uploadStatus = '업로드 중 오류가 발생했습니다.'
      } finally {
        this.isUploading = false
      }
    },
  },
}
</script>
