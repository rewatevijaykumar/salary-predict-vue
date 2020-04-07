import Vue from 'vue';
import VueRouter from 'vue-router';
import Salary from '../components/Salary.vue';
import Book from '../components/Book.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Salary',
    component: Salary,
  },
  {
    path: '/book',
    name: 'Book',
    component: Book,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
