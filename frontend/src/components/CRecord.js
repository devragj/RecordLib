import React from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import CasesWrapper from "./Cases";
import DefendantWrapper from "./Defendant";
import AddCaseWrapper from "./AddCase";
import { CRECORD_ID } from "../normalize";

/**
 * Component that displays a criminal record.
 * It has information about the defendant and a list of cases.
 */
function CRecord(props) {
    const { defendant, cRecordId } = props;
    const cRecordStyle = {margin: '15px', border: '1px solid black', borderRadius: '25px', padding: '10px', width: '950px'};
    return (
        <div className="cRecord" style={cRecordStyle}>
            <DefendantWrapper defendantId={defendant}/>
            <AddCaseWrapper />
            <CasesWrapper cRecordId={cRecordId} />

        </div>
    );
};

CRecord.propTypes = {
    defendant: PropTypes.string.isRequired,
    cRecordId: PropTypes.string.isRequired
};

function mapStateToProps(state) {
    return {defendant: state.entities.cRecord[CRECORD_ID].defendant, cRecordId: CRECORD_ID};
};

const CRecordWrapper = connect(mapStateToProps)(CRecord);
export default CRecordWrapper;