import React from 'react';
import SignUpForm from './SignUpForm';
import PropTypes from 'prop-types';
import Auth from '../Auth/Auth';

class SignUp extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            errors: {},
            userinfo: {
                email: '',
                password: '',
                confirm_password: ''
            }
        };
        this.submitForm = this.submitForm.bind(this);
        this.changeForm = this.changeForm.bind(this);
    }
    submitForm(event) {
        event.preventDefault();

        const email = this.state.userinfo.email;
        const password = this.state.userinfo.password;
        const confirm_password = this.state.userinfo.confirm_password;

        console.log('email:', email);
        console.log('password:', password);
        console.log('confirm_password:', confirm_password);

        if (password !== confirm_password) {
            return;
        }

        // Post data
        const url = "http://" + window.location.hostname + ":3000" + "/auth/signup";
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
                this.setState({errors: {}});
                res.json().then(json => {
                    console.log(json);
                    Auth.authenticateUser(json.token, email);
                    this.context.router.replace('/login');
                });
            } else {
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

        if (this.state.userinfo.password !== this.state.userinfo.confirm_password) {
            const errors = this.state.errors;
            errors.password = "Password and Confirm Password don't match.";
            this.setState({errors});
        } else {
            const errors = this.state.errors;
            errors.password = "";
            this.setState({errors});
        }
    }

    render() {
        return (
            <SignUpForm
                onSubmit={this.submitForm}
                onChange={this.changeForm}
                errors={this.state.errors}
                userinfo={this.state.userinfo} />
        );
    }
}

SignUp.contextTypes = {
    router: PropTypes.object.isRequired
}

export default SignUp;