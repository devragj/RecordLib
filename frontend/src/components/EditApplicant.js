import React from "react";
import PropTypes from 'prop-types';

import Aliases from "./Aliases";
import EditField from "./EditField";

function EditApplicant(props) {
    const { first_name, last_name, date_of_birth, date_of_death, aliases, ssn, address, modifier } = props;
    const applicantStyle = { display: 'grid', gridTemplateColumns: '400px 300px', margin: '15px', border: '1px solid black', borderRadius: '5px', padding: '10px', width: '720px' };
    const buttonStyle = { width: "150px", height: "28px", justifySelf: "right", marginRight: "20px" };

    /**
     * This function starts with the modifier function, which expects a key,value pair
     * and returns a function which takes a key and returns a function which expects a value.
     */
    const getPropertyModifier = key => {
        return value => modifier(key, value);
    }



    const toggleEditing = () => modifier('editing', false);

    return (
        <div className="applicant" style={applicantStyle}>
            <div>
                <EditField item={first_name} label="First Name: " modifier={getPropertyModifier('first_name')} />
                <EditField item={last_name} label="Last Name: " modifier={getPropertyModifier('last_name')} />
            </div>
            <button type="button" style={buttonStyle} onClick={toggleEditing}>Done Editing</button>
            <EditField item={date_of_birth} label="DOB: " modifier={getPropertyModifier('date_of_birth')} />
            <EditField item={date_of_death} label="Deceased Date: " modifier={getPropertyModifier('date_of_death')} />
            <EditField item={ssn} label="Social Security Number: " modifier={getPropertyModifier('ssn')} />
            <EditField item={address} label="Address: " modifier={getPropertyModifier('address')} />
            <div>Aliases: <Aliases editing={true} aliases={aliases}/></div>
        </div>
    );
}

EditApplicant.propTypes = {
    first_name: PropTypes.string,
    last_name:  PropTypes.string,
    date_of_birth:  PropTypes.string,
    date_of_death:  PropTypes.string,
    aliases: PropTypes.array,
    ssn: PropTypes.string,
    address: PropTypes.string,
    modifier: PropTypes.func
}

export default EditApplicant;