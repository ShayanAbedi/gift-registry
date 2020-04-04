Vue.component('modal', {
  template: '#modal-template'
});

var app = new Vue({
  el: '#app',

  //------- data --------
  data: {
    serviceURL: 'https://info3103.cs.unb.ca:8038',
    mainPage: true,
    authenticated: false,
    loggedIn: null,
    loginModal: false,
    presentsData: null,
    userData: null,
    editModal: false,
    addModal: false,
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
    },
    addedPresent: {
      present_name: '',
      link: '',
      img_url: ''
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

    addPresent(userId) {
      axios
        .post(this.serviceURL + '/users/' + userId + '/presents', {
          present_name: this.addedPresent.present_name,
          link: this.addedPresent.link,
          img_url: this.addedPresent.img_url
        })
        .then(response => {
          this.addedPresent.present_name = '';
          this.addedPresent.link = '';
          this.addedPresent.img_url = '';
          alert('Present added successfully!');
        })
        .catch(e => {
          console.log(e);
          alert('Unable to add the present to database');
        });
    },

    deletePresent(userId, presentId) {
      axios
        .delete(this.serviceURL + '/users/' + userId + '/presents/' + presentId)
        .then(response => {
          axios
            .get(this.serviceURL + '/presents')
            .then(response => {
              this.presentsData = response.data.presents;
            })
            .catch(e => {
              alert('Unable to retrieve the presents back');
              console.log(e);
            });
          alert('Deleting the present with ID ' + presentId);
        })
        .catch(e => {
          alert('Unable to delete present: ' + presentId);
          console.log(e);
        });
    },

    selectPresent(presentId) {
      this.showEditModal();
      for (element in this.presentsData) {
        if (this.presentsData[element].present_id == presentId) {
          this.selectedPresent = this.presentsData[element];
        }
      }
    },

    updatePresent(userId, presentId) {
      axios
        .put(this.serviceURL + '/users/' + userId + '/presents/' + presentId, {
          present_name: this.selectedPresent.present_name,
          link: this.selectedPresent.link,
          img_url: this.selectedPresent.img_url
        })
        .then(response => {
          alert('Present updated successfully!');
        })
        .catch(e => {
          console.log(e);
          alert('Unable to modify the present on the database');
        });
    },

    showEditModal() {
      this.editModal = true;
    },

    hideModal() {
      this.editModal = false;
    },
    updateModal(userId, presentId) {
      this.updatePresent(userId, presentId);
      this.editModal = false;
    },
    addToModal() {
      axios
        .get(this.serviceURL + '/users/' + this.input.username)
        .then(response => {
          this.userData = response.data.user;
          this.addPresent(this.userData.user_id);
        })
        .catch(e => {
          alert('Unable to retrieve the user info back');
          console.log(e);
        });
      this.addModal = false;
    }
  }
  //------- END methods --------
});
