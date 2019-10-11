import React from "react";
import PropTypes from 'prop-types';

import EditField from "./EditField";

/**
 * Component to edit a alias, including supplying values to a newly-created alias.
 */
function EditAlias(props) {
    const { id, name, modifier } = props;
    const aliasStyle = {  };

    /**
     * This function starts with the modifier function, which expects a key,value pair
     * and returns a function which takes a key and returns a function which expects a value.
     */

    return (
        <div className="editAlias" id={id} style={aliasStyle}>
            <EditField item={name} label="" modifier={modifier} />
        </div>
    );
}

EditAlias.propTypes = {
    id: PropTypes.string,
    name: PropTypes.string,
    modifier: PropTypes.func
}

export default EditAlias;