Vue.component('modal', {
  template: '#modal-template'
});

var app = new Vue({
  el: '#app',

  //------- data --------
  data: {
    serviceURL: 'http://info3103.cs.unb.ca:8038',
    mainPage: true,
    authenticated: false,
    loggedIn: null,
    presentsData: null,
    editModal: false,
    input: {
      username: '',
      password: ''
    },
    selectedPresent: {
      present_name: '',
      link: '',
      img_url: '',
      user_name: '',
      present_id: '',
      user_id: ''
    }
  },
  methods: {
    login() {
      if (this.input.username != '' && this.input.password != '') {
        axios
          .post(this.serviceURL + '/signin', {
            username: this.input.username,
            password: this.input.password
          })
          .then(response => {
            if (response.data.status == 'success') {
              this.authenticated = true;
              this.loggedIn = response.data.username;
            }
            console.log(this.loggedIn);
          })
          .catch(e => {
            alert('The username or password was incorrect, try again');
            this.input.password = '';
            console.log(e);
          });
      } else {
        alert('A username and password must be present');
      }
    },

    logout() {
      axios
        .delete(this.serviceURL + '/signin')
        .then(response => {
          location.reload();
          alert('You logged out successfully!');
        })
        .catch(e => {
          console.log(e);
        });
    },

    getPresents() {
      axios
        .get(this.serviceURL + '/presents')
        .then(response => {
          this.presentsData = response.data.presents;
        })
        .catch(e => {
          alert('Unable to retrieve the presents back');
          console.log(e);
        });
    },

    selectPresent(presentId) {
      this.showModal();
      for (element in this.presentsData) {
        if (this.presentsData[element].present_id == presentId) {
          this.selectedPresent = this.presentsData[element];
        }
      }
    },
    showModal() {
      this.editModal = true;
    },

    hideModal() {
      this.editModal = false;
    }
  }
  //------- END methods --------
});
