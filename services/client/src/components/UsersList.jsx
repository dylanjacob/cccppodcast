import React from 'react';

const UsersList = (props) => {
  return (
    <div>
      <table className="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Username</th>
            <th scope="col">Email</th>
            <th scope="col">Active?</th>
          </tr>
        </thead>
        <tbody>
      {
        props.users.map((user, i) => {
          return (
                <tr id="user" key={ user.id }>
                  <th scope="row">{ i + 1 }</th>
                  <td>{ user.username }</td>
                  <td>{ user.email }</td>
                  <td>{ user.active ? 'YES' : 'NO'  }</td>
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