import React from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import Sentences from "./Sentences";
import EditBox from "./EditBox";
import { editField } from "../actions";

function Charge(props) {
    const { id, offense, grade, statute, disposition, disposition_date, sentences, modifier } = props;
    const chargeStyle = { display: 'grid', gridTemplateColumns: '450px 350px', margin: '15px', border: '1px solid black', borderRadius: '10px', padding: '10px', width: '820px' };

    return (
        <div className="charge" id={id} style={chargeStyle}>
            <div>Offense: {offense}</div>
            <EditBox title="Grade: " item={grade} modifier={modifier} />
            <div>Statute: {statute}</div>
            <div>Disposition: {disposition}</div>
            <div>Disposition Date: {disposition_date}</div>
            <Sentences sentences={sentences} chargeId={id} />
        </div>
    );
}

Charge.propTypes = {
    id: PropTypes.string,
    offense: PropTypes.string,
    grade: PropTypes.string,
    statute: PropTypes.string,
    disposition: PropTypes.string,
    disposition_date: PropTypes.string,
    sentences: PropTypes.array.isRequired
}

function mapStateToProps(state, ownProps) {
    return state.entities.charges[ownProps.chargeId];
};

function mapDispatchToProps(dispatch, ownProps) {
    return { modifier: item => {
            dispatch(editField('charges', ownProps.chargeId, 'grade', item))
        }
    };
};

const ChargeWrapper = connect(mapStateToProps, mapDispatchToProps)(Charge);
export default ChargeWrapper;