<template>
  <el-table :data="tasks">
    <el-table-column prop="name" label="Task" />
  </el-table>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
const tasks = ref([])
onMounted(async () => {
  const res = await api.get('/tasks/')
  tasks.value = res.data
})
</script>
