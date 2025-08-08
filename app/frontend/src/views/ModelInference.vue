<template>
  <el-form :model="form" @submit.prevent="submit">
    <el-form-item label="Input">
      <el-input v-model="form.input" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" native-type="submit">Run</el-button>
    </el-form-item>
  </el-form>
  <div v-if="result">Result: {{ result }}</div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import api from '../api'
const form = reactive({ input: '' })
const result = ref('')
const submit = async () => {
  const res = await api.post('/inference/', form)
  result.value = res.data.result
}
</script>
