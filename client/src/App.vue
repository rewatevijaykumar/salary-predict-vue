<template>
  <div id="app">
    <div id="nav">
      <div class="row h-100 justify-content-center align-items-center">
      <router-link to="/"><h2>Home</h2></router-link>
      <div class="vl ml-2 mr-2"></div>
      <router-link to="/book"><h2>Book</h2></router-link>
      <div class="vl ml-2 mr-2"></div>
      <router-link to="/about"><h2>About</h2></router-link>
      </div>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
.vl {
  border-left: 2px solid #42b983;
  height: 50px;
}
h2 {
margin: 0;
font-size: 1.6rem;
font-weight: bold;
}
</style>
