import React from 'react';

const UsersList = (props) => {
  return (
    <div>
      <h2>All Users</h2>
      <table className="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">ID</th>
            <th scope="col">Username</th>
            <th scope="col">Email</th>
            <th scope="col">Active</th>
            <th scope="col">Admin</th>
          </tr>
        </thead>
        <tbody>
      {
        props.users.map((user, i) => {
          return (
                <tr id="user" key={ user.id }>
                  <th scope="row">{ i + 1 }</th>
                  <td>{ user.id }</td>
                  <td>{ user.username }</td>
                  <td>{ user.email }</td>
                  <td>{ user.active ? 'YES' : 'NO'  }</td>
                  <td>{ user.admin ? 'YES' : 'NO' }</td>
                </tr>
          )
        })
      }
        </tbody>
      </table>
    </div>
  )
};

export default UsersList;