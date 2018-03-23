import './Base.css';

import React from 'react';
import Auth from '../Auth/Auth';
import { Link } from 'react-router';

class Base extends React.Component {
    render() {
        return (
            <div>
                <nav className="nav-bar indigo lighten-1">
                    <div className="nav-wrapper">
                        <a className="brand-logo" href="/"> Tap News </a>
                        <ul id="nav-modbile" className="right">
                            { Auth.isUserAuthenticated() ?
                                (<div>
                                    <li><Link to="/about">About us</Link></li>
                                    <li>{ Auth.getEmail()}</li>
                                    <li><Link to="/logout">Log out</Link></li>
                                </div>) :
                                (<div>
                                    <li><Link to="/about">About us</Link></li>
                                    <li><Link to="/login">Log in</Link></li>
                                    <li><Link to="/signup">Sign up</Link></li>
                                </div>)
                            }
                        </ul>
                    </div>
                </nav>
                <br />
                {this.props.children}
            </div>
        );
    };
}

export default Base;
