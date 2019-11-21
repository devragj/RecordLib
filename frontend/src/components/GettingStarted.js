import React from "react";
import Container from "@material-ui/core/Container"
import Paper from "@material-ui/core/Paper"
import { makeStyles } from "@material-ui/core/styles"

const useStyles = makeStyles(theme =>  {
    return({
        paper: {
            padding: theme.spacing(3),
            marginTop: theme.spacing(3),
        }
    })
})

import ApplicantHolderWrapper from "./ApplicantHolder";
import NameSearch from "./NameSearch"
function GettingStarted(props) {
    const classes = useStyles()
    const gettingStartedStyle = { margin: '15px', border: '1px solid black', borderRadius: '25px', padding: '10px', width: '950px' };
    return (
        <Container>
            <Paper className={classes.paper}>
                <div className="gettingStarted" style={gettingStartedStyle}>
                    <ApplicantHolderWrapper />
                </div>
                <NameSearch />
            </Paper>
        </Container>
    );
};

export default GettingStarted;