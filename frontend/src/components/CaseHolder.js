import React from "react";
import { connect } from 'react-redux';

import Case from "./Case";
import EditCase from "./EditCase";
import { editField, toggleEditing } from "../actions";

/**
 * Connected component for a Case, which can be in edit mode.
 * The editing prop determines the mode.
 * Props which are properties of the case are passed to a child
 * presentational component, which is either Case or EditCase.
 * Theses components also receive a dispatching function, which is used by the
 * EditCase component to send changes to the redux store.
 */
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