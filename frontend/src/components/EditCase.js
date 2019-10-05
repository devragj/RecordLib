import React from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import EditField from "./EditField";
import Charges from "./Charges";
import { editField } from "../actions";

/**
 * Component to supply values to a newly-created Case.
 */
function EditCase(props) {
    const { modifier, id, docket_number, otn, dc, status, county, judge, arrest_date, disposition_date, charges,
            total_fines, fines_paid, complaint_date, judge_address, affiant, arresting_agency, 
            arresting_agency_address} = props;
    const caseStyle = { display: 'grid', gridTemplateColumns: '270px 270px 270px', margin: '10px',
        border: '1px solid black', borderRadius: '15px', padding: '10px', width: '860px' };

    /**
     * This function starts with the modifier function, which expects a key,value pair
     * and returns a function which takes a key and returns a function which expects a value.
     */
    const getPropertyModifier = key => {
        return value => modifier(key, value);
    }

    return (
        <div className="editCase" id={id} style={caseStyle}>
            <div style={{gridColumn: "1 / 3"}}>Docket Number: {docket_number}</div>
            <EditField item={otn} label="OTN: " modifier={getPropertyModifier('otn')} />
            <EditField item={dc} label="DC: " modifier={getPropertyModifier('dc')} />
            <EditField item={status} label="Status: " modifier={getPropertyModifier('status')} />
            <EditField item={county} label="County: " modifier={getPropertyModifier('county')} />
            <EditField item={judge} label="Judge: " modifier={getPropertyModifier('judge')} />
            <EditField item={judge_address} label="Judge Address: " modifier={getPropertyModifier('judge_address')} />
            <EditField item={arrest_date} label="Arrest Date: " modifier={getPropertyModifier('arrest_date')} />
            <EditField item={disposition_date} label="Disposition Date: " modifier={getPropertyModifier('disposition_date')} />
            <EditField item={total_fines} label="Total Fines: " modifier={getPropertyModifier('total_fines')} />
            <EditField item={fines_paid} label="Fines Paid: " modifier={getPropertyModifier('fines_paid')} />
            <EditField item={complaint_date} label="Complaint Date: " modifier={getPropertyModifier('complaint_date')} />
            <EditField item={affiant} label="Affiant: " modifier={getPropertyModifier('affiant')} />
            <EditField item={arresting_agency} label="Arresting Agency: " modifier={getPropertyModifier('arresting_agency')} />
            <EditField item={arresting_agency_address} label="Arresting Agency Address: " modifier={getPropertyModifier('arresting_agency_address')} />
            <div></div>
            <div></div>
            <Charges caseId={id} charges={charges} editing={true}/>
        </div>
    );
};

EditCase.propTypes = {
    id: PropTypes.string,
    docket_number: PropTypes.string,
    otn:  PropTypes.string,
    dc: PropTypes.string,
    status:  PropTypes.string,
    county:  PropTypes.string,
    judge:  PropTypes.string,
    arrest_date:  PropTypes.string,
    disposition_date:  PropTypes.string,
    charges: PropTypes.array.isRequired,
    total_fines: PropTypes.string,
    fines_paid:  PropTypes.string,
    complaint_date:  PropTypes.string,
    judge_address: PropTypes.string,
    affiant: PropTypes.string,
    arresting_agency: PropTypes.string,
    arresting_agency_address: PropTypes.string,
    modifier: PropTypes.func
}

function mapStateToProps(state, ownProps) {
    return state.entities.cases[ownProps.caseId];
};

/**
 * This function returns a function which take a key,value pair
 * and associates the value with that key in the Case
 * object being edited.
 */
function mapDispatchToProps(dispatch, ownProps) {
    return { modifier: (key, value) => {
            dispatch(editField('cases', ownProps.caseId, key, value))
        }
    };
};

const EditCaseWrapper = connect(mapStateToProps, mapDispatchToProps)(EditCase);
export default EditCaseWrapper;