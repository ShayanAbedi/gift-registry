// register modal component
Vue.component('modal', {
  template: '#modal-template'
});

var app = new Vue({
  el: '#app',

  //------- data --------
  data: {
    serviceURL: 'https://info3103.cs.unb.ca:8038',
    authenticated: false,
    schoolsData: null,
    loggedIn: null,
    editModal: false,
    input: {
      username: '',
      password: ''
    }
  }
});
