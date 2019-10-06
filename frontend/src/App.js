import React, {useState} from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { fetchCRecord } from "./actions";
import CSSBaseline from "@material-ui/core/CssBaseline";
import Container from "@material-ui/core/Container"
import Navbar from "./components/Navbar";
import About from "./components/About";
import NotFound from "./components/NotFound";
import PetitionProcess from "./components/PetitionProcess"
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";



/**
 * Parent component
 *
 * The user can upload a Summary PDF file.
 * Clicking "Upload" will send the file to the backend
 * to be processed into a CRecord.
 * The returned JSON will be processed and sent to the redux store.
 * After that, this component can render a child CRecord component.
 */
function App(props) {
    return (<main className="content" style={{ margin: '0px'}}>
        <React.Fragment>
            <CSSBaseline/>
            <Router>
                <Navbar></Navbar>
                <Switch>
                    <Route path="/about">
                        <About/>
                    </Route>
                    <Route path="/">
                        <PetitionProcess/>
                    </Route>
                    <Route>
                        <NotFound/>
                    </Route>
                </Switch>
            </Router>



        </React.Fragment>
    </main>);
};

App.propTypes = {
    cRecordPresent: PropTypes.bool,
    fetchCRecord: PropTypes.func.isRequired
};

function mapStateToProps(state) {
    return { cRecordPresent: state.entities? true: false };
};

function mapDispatchToProps(dispatch) {
    return { fetchCRecord: file => dispatch(fetchCRecord(file)) };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);