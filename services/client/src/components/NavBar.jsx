import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = (props) => (
  // eslint-disable-next-line
  <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
    <Link to="#" className="navbar-brand">
      <strong className="navbar-item">{props.title}</strong>
    </Link>
    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>
    <div className="collapse navbar-collapse" id="navbarSupportedContent">
      <ul className="navbar-nav mr-auto">
        <li className="nav-item">
          <Link to="/" className="nav-link">Home</Link>
        </li>
        <li className="nav-item">
          <Link to="/about" className="nav-link">About</Link>
        </li>
        {props.isAuthenticated &&
        <li className="nav-item">
          <Link to="/status" className="nav-link">User Status</Link>
        </li>
        }
      </ul>
      <ul className="navbar-nav mr-auto">
        {!props.isAuthenticated &&
        <li className="nav-item">
          <Link to="/register" className="nav-link">Register</Link>
        </li>
        }
        {!props.isAuthenticated &&
        <li className="nav-item">
          <Link to="/login" className="nav-link">Log In</Link>
        </li>
        }
        {props.isAuthenticated &&
        <li className="nav-item">
          <Link to="/logout" className="nav-link">Log Out</Link>
        </li>
        }
      </ul>
    </div>
  </nav>
)

export default NavBar;