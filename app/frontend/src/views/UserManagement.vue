<template>
  <el-table :data="users">
    <el-table-column prop="username" label="Username" />
    <el-table-column prop="email" label="Email" />
  </el-table>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
const users = ref([])
onMounted(async () => {
  const res = await api.get('/users/')
  users.value = res.data
})
</script>
