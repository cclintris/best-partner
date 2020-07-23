import React, { Component } from 'react'
import { Router, Switch, Route } from 'react-router-dom'

import history from './history'

import main from './views/main'

export class Routes extends Component {
    render() {
        return (
            <Router history = { history }>
                <Switch>
                    <Route path = '/' exact component = { main }></Route>
                </Switch>
            </Router>
        )
    }
}

export default Routes
