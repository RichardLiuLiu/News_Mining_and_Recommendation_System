import Base from './Base/Base';
import App from './App/App';
import Login from './Login/Login';
import SignUp from './SignUp/SignUp';
import Auth from './Auth/Auth';
import AboutUs from './AboutUs/AboutUs';

const routes = {
    component: Base,
    childRoutes: [
        {
            path: '/',
            getComponent: (location, callback) => {
                if (Auth.isUserAuthenticated()) {
                    callback(null, App);
                } else {
                    callback(null, Login);
                }
            }
        },
        {
            path: '/login',
            component: Login
        },
        {
            path: '/signup',
            component: SignUp
        },
        {
            path: '/logout',
            onEnter: (nextState, replace) => {
                Auth.deauthenticateUser();
                replace('/');
            }
        },
        {
            path: '/about',
            component: AboutUs
        }
    ]
};

export default routes;