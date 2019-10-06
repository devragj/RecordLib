import React from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import Case from "./Case";
import EditCase from "./EditCase";
import { editField, toggleEditing } from "../actions";

function CaseHolder(props) {
    return (
        <div className="caseHolder" >
            { !props.editing?
                <Case {...props} />
                : <EditCase {...props} />
            }
        </div>
    );
};

function mapStateToProps(state, ownProps) {
    return state.entities.cases[ownProps.caseId];
};

/**
 * The modifier function takes a key,value pair
 * and associates the value with that key in the Case
 * object being edited.  It is used by the EditCase component.
 */
function mapDispatchToProps(dispatch, ownProps) {
    return {
        modifier: (key, value) => {
            dispatch(editField('cases', ownProps.caseId, key, value))
        },
        toggleEditing: () => dispatch(toggleEditing(ownProps.caseId))
    };
};

const CaseHolderWrapper = connect(mapStateToProps, mapDispatchToProps)(CaseHolder);
export default CaseHolderWrapper;