import React from "react";
import PropTypes from 'prop-types';

import EditField from "./EditField";

/**
 * Component to edit a attorney, including supplying values to a newly-created attorney.
 */
function EditAttorney(props) {
    const { modifier, id, full_name, address, bar_id, organization, toggleEditing} = props;
    const attorneyStyle = { display: 'grid', gridTemplateColumns: '270px 270px 270px', margin: '10px',
        border: '1px solid black', borderRadius: '15px', padding: '10px', width: '860px' };

    /**
     * This function starts with the modifier function, which expects a key,value pair
     * and returns a function which takes a key and returns a function which expects a value.
     */
    const getPropertyModifier = key => {
        return value => modifier(key, value);
    }

    return (
        <div className="editAttorney" id={id} style={attorneyStyle}>
            <div style={{gridColumn: "1 / 3"}}>
                <EditField item={full_name} label="Full Name: " modifier={getPropertyModifier('full_name')} />
            </div>
            <button type="button" style={{marginLeft: "20px"}} onClick={toggleEditing}>Done Editing</button>
            <EditField item={organization} label="Organization: " modifier={getPropertyModifier('organization')} />
            <EditField item={bar_id} label="Bar ID: " modifier={getPropertyModifier('bar_id')} />
            <EditField item={address} label="Address: " modifier={getPropertyModifier('address')} />
        </div>
    );
};

EditAttorney.propTypes = {
    id: PropTypes.string,
    full_name: PropTypes.string,
    address: PropTypes.string,
    bar_id: PropTypes.string,
    organization: PropTypes.string,
    toggleEditing: PropTypes.func,
    modifier: PropTypes.func
}

export default EditAttorney;