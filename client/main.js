Vue.component('modal', {
  template: '#modal-template'
});

var app = new Vue({
  el: '#app',

  //------- data --------
  data: {
    serviceURL: 'https://info3103.cs.unb.ca:8004',
    mainPage: true,
    loginModal: false,
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

    /*addPresent(presentId){
      axios
      .post(this.serviceURL + '/users/' + userId + '/presents/'+ presentId)

    },*/

    deletePresent(userId, presentId) {
      axios
        .delete(this.serviceURL + '/users/' + userId + '/presents/'+ presentId)
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
          alert("deleted present with ID: " + presentId);
        })
        .catch(e => {
          alert('Unable to delete present: ' + presentId);
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

    updatePresent(userId, presentId){
      axios
        .put(this.serviceURL + '/users/' + userId + '/presents/'+ presentId)
        .then(response => {
          present_id = presentId;
          present_name = this.input.pn;
          link = this.input.lnk;
          img_url = this.input.img;
        })
        .catch(e => {
          console.log(e.response);
          alert('Unable to modufy db');
        });
    },

    showModal() {
      this.editModal = true;
    },

    hideModal(userId,presentId) {
      this.updatePresent(userId,presentId);
      this.editModal = false;
    }
  }
  //------- END methods --------
});
