import store from '@/state/store'

export default [{
    path: '/',
    meta: {
        authRequired: true
    },
    name: 'enterprise',
    component: () => import('./views/1/enterprise'),
},
{
    path: '/login',
    name: 'login',
    component: () => import('./views/account/login'),
    meta: {
        beforeResolve(routeTo, routeFrom, next) {
            // If the user is already logged in
            if (store.getters['auth/loggedIn']) {
                // Redirect to the home page instead
                next({
                    name: 'enterprise'
                })
            } else {
                // Continue to the login page
                next()
            }
        },
    },
},
{
    path: '/register',
    name: 'register',
    component: () => import('./views/account/register'),
    meta: {
        beforeResolve(routeTo, routeFrom, next) {
            // If the user is already logged in
            if (store.getters['auth/loggedIn']) {
                // Redirect to the home page instead
                next({
                    name: 'enterprise'
                })
            } else {
                // Continue to the login page
                next()
            }
        },
    },
},
{
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import('./views/account/forgot-password'),
    meta: {
        beforeResolve(routeTo, routeFrom, next) {
            // If the user is already logged in
            if (store.getters['auth/loggedIn']) {
                // Redirect to the home page instead
                next({
                    name: 'enterprise'
                })
            } else {
                // Continue to the login page
                next()
            }
        },
    },
},
{
    path: '/logout',
    name: 'logout',
    meta: {
        authRequired: true,
        beforeResolve(routeTo, routeFrom, next) {
            if (process.env.VUE_APP_DEFAULT_AUTH === "firebase") {
                store.dispatch('auth/logOut')
            } else {
                store.dispatch('authfack/logout')
            }
            const authRequiredOnPreviousRoute = routeFrom.matched.some(
                (route) => route.push('/login')
            )
            // Navigate back to previous page, or home as a fallback
            next(authRequiredOnPreviousRoute ? {
                name: 'default'
            } : {
                ...routeFrom
            })
        },
    },
},
{
    path: '/subscribe',
    name: 'Subscribe',
    component: () => import('./views/1/subscribe'),
    meta: {
        authRequired: true,
    },
},
{
    path: '/enterprise',
    name: 'Enterprise',
    component: () => import('./views/1/enterprise'),
    meta: {
        authRequired: true,
    },
},
{
    path: '/chart',
    name: 'Chart',
    component: () => import('./views/1/chart'),
    meta: {
        authRequired: true,
    },
},
{
    path: '/credit-report',
    name: 'Credit-report',
    component: () => import('./views/1/credit-report'),
    meta: {
        authRequired: true,
    },
},
{
    path: '/decision-report',
    name: 'Decision-report',
    component: () => import('./views/1/decision-report'),
    meta: {
        authRequired: true,
    },
},
]