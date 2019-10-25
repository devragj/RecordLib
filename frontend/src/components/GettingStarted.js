import React from "react";
import Container from "@material-ui/core/Container"

import ApplicantHolderWrapper from "./ApplicantHolder";

function GettingStarted(props) {
    const gettingStartedStyle = { margin: '15px', border: '1px solid black', borderRadius: '25px', padding: '10px', width: '950px' };
    return (
        <Container>
            <div className="gettingStarted" style={gettingStartedStyle}>
                <ApplicantHolderWrapper />
            </div>
        </Container>
    );
};

export default GettingStarted;