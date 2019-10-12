import React from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Cases from "./Cases";
import ApplicantHolderWrapper from "./ApplicantHolder";

import { CRECORD_ID } from "../normalize";

/**
 * Component that displays a criminal record.
 * It has information about the defendant and a list of cases.
 */
function CRecord(props) {
    const { cases } = props;
    const cRecordStyle = {margin: '15px', border: '1px solid black', borderRadius: '25px', padding: '10px', width: '950px'};
    return (
        <div className="cRecord" style={cRecordStyle}>
            <ApplicantHolderWrapper />
            <Cases cases={cases} />
        </div>
    );
};

CRecord.propTypes = {
    cases: PropTypes.array.isRequired
};

function mapStateToProps(state) {
    return state.crecord.cRecord[CRECORD_ID];
};

const CRecordWrapper = connect(mapStateToProps)(CRecord);
export default CRecordWrapper;