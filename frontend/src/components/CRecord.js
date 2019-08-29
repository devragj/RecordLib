import React from "react";
import PropTypes from 'prop-types';
import Cases from "./Cases";
import Defendant from "./Defendant"

/**
 * Component that displays a criminal record.
 * It has information about the defendant and a list of cases.
 */
function CRecord(props) {
    const cRecordStyle = {margin: '15px', border: '1px solid black', borderRadius: '25px', padding: '10px', width: '950px'};
    const { defendant, cases } = props
    return (
        <div className="cRecord" style={cRecordStyle}>
            <Defendant {...defendant}/>
            <Cases cases={cases}/>
        </div>
    );
}

CRecord.propTypes = {
    defendant: PropTypes.object.isRequired,
    cases: PropTypes.array.isRequired
}

export default CRecord;