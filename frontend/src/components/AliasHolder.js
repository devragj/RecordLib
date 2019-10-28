import React from "react";
import { connect } from 'react-redux';

import Alias from "./Alias";
import EditAlias from "./EditAlias";
import { editAlias } from "../actions";

/**
 * Connected component for a Alias, which can be in edit mode.
 * The editing prop determines the mode, and is passed in from the parent case.
 * Props which are properties of the alias are passed to a child
 * presentational component, which is either Alias or EditAlias.
 * These components also receive a dispatching function, which is used by the
 * EditAlias component to send changes to the redux store.
 */
function AliasHolder(props) {
    return (
        <div className="aliasHolder" >
            { !props.editing?
                <Alias {...props} />
                : <EditAlias {...props} />
            }
        </div>
    );
};

function mapStateToProps(state, ownProps) {
    return { name: state.applicantInfo.aliases[ownProps.aliasId] };
};

/**
 * The modifier function takes a key,value pair
 * and associates the value with that key in the Alias
 * object being edited.  It is used by the EditAlias component.
 */
function mapDispatchToProps(dispatch, ownProps) {
    return {
        modifier: (value) => {
            dispatch(editAlias(ownProps.aliasId, value))
        }
    };
};

const AliasHolderWrapper = connect(mapStateToProps, mapDispatchToProps)(AliasHolder);
export default AliasHolderWrapper;