import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';  // new
import UsersList from './components/UsersList';
import AddUser from './components/AddUser';

class App extends Component {

  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };
  

 
constructor() {
  super();
  this.state = {
    users: [],
    username: '',
    email: '',
  };
  this.handleChange = this.handleChange.bind(this);
  this.addUser = this.addUser.bind(this);  // new
};


  addUser(event) {
    event.preventDefault();
    console.log('sanity check!');
    console.log(this.state);  
  };
  
 
 
  componentDidMount() {
    this.getUsers();
  };

  getUsers() {
  axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)  // new
  .then((res) => { this.setState({ users: res.data.data.users }); })
  .catch((err) => { console.log(err); });
};

render() {
  return (
    <section className="section">
      <div className="container">
        <div className="columns">
          <div className="column is-half">  {/* new */}
            <br/>
            <h1 className="title is-1">All Users</h1>
            <hr/><br/>
            <AddUser
              username={this.state.username}
              email={this.state.email}
              addUser={this.addUser}
              handleChange={this.handleChange}  // new
            />

            {/* new */}
            <br/><br/>  {/* new */}
            <UsersList users={this.state.users}/>
          </div>
        </div>
      </div>
    </section>
  )
}

};
ReactDOM.render(
  <App />, 
  document.getElementById('root')
  
);