import React from "react";
import { connect } from 'react-redux';

import Attorney from "./Attorney";
import EditAttorney from "./EditAttorney";
import { editAttorney, toggleEditingAttorney } from "../actions";

/**
 * Connected component for a Attorney, which can be in edit mode.
 * The editing prop determines the mode.
 * Props which are properties of the attorney are passed to a child
 * presentational component, which is either Attorney or EditAttorney.
 * Theses components also receive a dispatching function, which is used by the
 * EditAttorney component to send changes to the redux store.
 */
function AttorneyHolder(props) {
    return (
        <div className="attorneyHolder" >
            { !props.editing?
                <Attorney {...props} />
                : <EditAttorney {...props} />
            }
        </div>
    );
};

function mapStateToProps(state, ownProps) {
    return state.petitionPackage.attorneys[ownProps.attorneyId];
};

/**
 * The modifier function takes a key,value pair
 * and associates the value with that key in the Attorney
 * object being edited.  It is used by the EditAttorney component.
 */
function mapDispatchToProps(dispatch, ownProps) {
    return {
        modifier: (key, value) => {
            dispatch(editAttorney(ownProps.attorneyId, key, value))
        },
        toggleEditing: () => dispatch(toggleEditingAttorney(ownProps.attorneyId))
    };
};

const AttorneyHolderWrapper = connect(mapStateToProps, mapDispatchToProps)(AttorneyHolder);
export default AttorneyHolderWrapper;