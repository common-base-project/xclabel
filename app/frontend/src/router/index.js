import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import UserManagement from '../views/UserManagement.vue'
import Tasks from '../views/Tasks.vue'
import Samples from '../views/Samples.vue'
import Labels from '../views/Labels.vue'
import ModelInference from '../views/ModelInference.vue'
import AgentConfig from '../views/AgentConfig.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/users', component: UserManagement },
  { path: '/tasks', component: Tasks },
  { path: '/samples', component: Samples },
  { path: '/labels', component: Labels },
  { path: '/inference', component: ModelInference },
  { path: '/agent', component: AgentConfig }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
