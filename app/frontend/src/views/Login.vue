<template>
  <el-form :model="form" class="login-form" @submit.prevent="submit">
    <el-form-item label="Username">
      <el-input v-model="form.username" />
    </el-form-item>
    <el-form-item label="Password">
      <el-input type="password" v-model="form.password" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" native-type="submit">Login</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { reactive } from 'vue'
import api from '../api'
const form = reactive({ username: '', password: '' })
const submit = async () => {
  await api.post('/login/', form)
}
</script>

<style scoped>
.login-form { max-width: 300px; margin: 100px auto; }
</style>
