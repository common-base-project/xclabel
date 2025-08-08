<template>
  <el-table :data="samples">
    <el-table-column prop="id" label="ID" />
  </el-table>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
const samples = ref([])
onMounted(async () => {
  const res = await api.get('/samples/')
  samples.value = res.data
})
</script>
