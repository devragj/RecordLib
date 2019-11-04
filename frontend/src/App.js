import React from "react";
import CSSBaseline from "@material-ui/core/CssBaseline";
import Navbar from "./components/Navbar";
import About from "./components/About";
import UserProfile from "./components/UserProfile";
import NotFound from "./components/NotFound";
import PetitionProcess from "./components/PetitionProcess"
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

function App() {
    return (<main className="content" style={{ margin: '0px'}}>
        <React.Fragment>
            <CSSBaseline/>
            <Router>
                <Navbar></Navbar>
                <Switch>
                    <Route path="/about">
                        <About/>
                    </Route>
                    <Route path="/profile">
                        <UserProfile/>
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

export default App;
