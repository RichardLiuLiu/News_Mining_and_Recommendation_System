import React from 'react';
import LoginForm from './LoginForm';
import PropTypes from 'prop-types';
import Auth from '../Auth/Auth';

class Login extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            errors: {},
            userinfo: {
                email: '',
                password: ''
            }
        };
        this.submitForm = this.submitForm.bind(this);
        this.changeForm = this.changeForm.bind(this);
    }
    submitForm(event) {
        event.preventDefault();

        const email = this.state.userinfo.email;
        const password = this.state.userinfo.password;

        console.log('email:', email);
        console.log('password:', password);

        // Post data
        const url = "http://" + window.location.hostname + ":3000" + "/auth/login";
        const request = new Request(
            url,
            {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

        fetch(request).then(res => {
            if (res.status === 200) {
                this.setState({errors:{}});
                res.json().then(json => {
                    console.log(json);
                    Auth.authenticateUser(json.token, email);
                    this.context.router.replace('/');
                });
            } else {
                console.log("Login failed");
                res.json().then(json => {
                    const errors = json.errors ? json.errors : {};
                    errors.summary = json.message;
                    this.setState({errors});
                });
            }
        });
    }

    changeForm(event) {
        const field = event.target.name;
        const userinfo = this.state.userinfo;
        userinfo[field] = event.target.value;

        this.setState({userinfo});
    }

    render() {
        return (
            <LoginForm
                onSubmit={this.submitForm}
                onChange={this.changeForm}
                errors={this.state.errors}
                userinfo={this.state.userinfo} />
        );
    }
}

Login.contextTypes = {
    router: PropTypes.object.isRequired
}

export default Login;