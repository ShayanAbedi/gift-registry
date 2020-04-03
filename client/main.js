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


    addPresent(){
      this.showModal();
      axios
        .post(this.serviceURL + '/users/4/presents', {
          present_name : "Name",
          link : "Link",
          img_url : "URL",
          user_id : "4"
        })
        .then(response => {
          console.log(response);
          this.hideModal();
        })
        .catch(e => {
          alert("problem adding new present");
          console.log(e);
        })

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
          alert('deleted present with ID: ' + presentId);
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
          alert('Unable to modify db');
        });
    },

    showModal() {
      this.editModal = true;
    },

    hideModal() {
      this.editModal = false;
    },
    updateModal(userId, presentId, pName, imgUrl, link) {
      this.updatePresent(userId, presentId, pName, imgUrl, link);
      this.editModal = false;
    }
  }
  //------- END methods --------
});
