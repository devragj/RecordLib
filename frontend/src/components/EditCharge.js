import React from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import EditField from "./EditField";
import SentencesWrapper from "./Sentences";
import { editField } from "../actions";

function EditCharge(props) {
    const { id, offense, grade, statute, disposition, disposition_date, modifier } = props;
    const chargeStyle = { display: 'grid', gridTemplateColumns: '450px 350px', margin: '15px', border: '1px solid black', borderRadius: '10px', padding: '10px', width: '820px' };

    const getPropertyModifier = key => {
        return value => modifier(key, value);
    }

    return (
        <div className="editCharge" id={id} style={chargeStyle}>
            <EditField item={offense} label="Offense: " modifier={getPropertyModifier('offense')} />
            <EditField item={grade} label="Grade: " modifier={getPropertyModifier('grade')} />
            <EditField item={statute} label="Statute: " modifier={getPropertyModifier('statute')} />
            <EditField item={disposition} label="Disposition: " modifier={getPropertyModifier('disposition')} />
            <EditField item={disposition_date} label="Disposition Date: " modifier={getPropertyModifier('disposition_date')} />
            <SentencesWrapper chargeId={id} editing={true}/>
        </div>
    );
}

EditCharge.propTypes = {
    id: PropTypes.string,
    offense: PropTypes.string,
    grade: PropTypes.string,
    statute: PropTypes.string,
    disposition: PropTypes.string,
    disposition_date: PropTypes.string,
    modifier: PropTypes.func
}

function mapStateToProps(state, ownProps) {
    return state.entities.charges[ownProps.chargeId];
};

function mapDispatchToProps(dispatch, ownProps) {
    return { modifier: (key, value) => {
            dispatch(editField('charges', ownProps.chargeId, key, value))
        }
    };
};

const EditChargeWrapper = connect(mapStateToProps, mapDispatchToProps)(EditCharge);
export default EditChargeWrapper;