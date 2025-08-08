<template>
  <el-form :model="form" @submit.prevent="submit">
    <el-form-item label="Name">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" native-type="submit">Save</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { reactive } from 'vue'
import api from '../api'
const form = reactive({ name: '' })
const submit = async () => {
  await api.post('/agent/', form)
}
</script>
