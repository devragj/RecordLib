import React from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import Container from "@material-ui/core/Container"

import Attorneys from "./Attorneys";

function DownloadPetitions(props) {
    const { attorneys } = props;
    const downloadPetitionStyle = { margin: '15px', border: '1px solid black', borderRadius: '25px', padding: '10px', width: '950px' };
    return (
        <Container>
            <div className="downloadPetition" style={downloadPetitionStyle}>
                    <Attorneys attorneys={attorneys} />
            </div>
        </Container>
    );
};

DownloadPetitions.propTypes = {
    attorneys: PropTypes.array.isRequired
};

function mapStateToProps(state) {
    return { attorneys: state.petitionPackage.attorneysList };
};

const DownloadPetitionsWrapper = connect(mapStateToProps)(DownloadPetitions);
export default DownloadPetitionsWrapper;