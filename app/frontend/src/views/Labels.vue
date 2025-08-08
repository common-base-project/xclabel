<template>
  <el-table :data="labels">
    <el-table-column prop="name" label="Label" />
  </el-table>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
const labels = ref([])
onMounted(async () => {
  const res = await api.get('/labels/')
  labels.value = res.data
})
</script>
