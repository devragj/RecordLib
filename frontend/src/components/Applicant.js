import React from "react";
import PropTypes from 'prop-types';

import Aliases from "./Aliases";
import Address from "./Address";

function Applicant(props) {
    const { first_name, last_name, date_of_birth, date_of_death, aliases, ssn, address, modifier } = props;
    const name = first_name + " " + last_name;
    const applicantStyle = { display: 'grid', gridTemplateColumns: '400px 250px', margin: '15px', border: '1px solid black', borderRadius: '5px', padding: '10px', width: '670px' };
    const buttonStyle = { width: "150px", height: "28px", justifySelf: "right", marginRight: "20px" };
    const toggleEditing = () => modifier('editing', true);

    return (
        <div className="applicant" style={applicantStyle}>
            <div>Name: {name}</div>
            <button type="button" style={buttonStyle} onClick={toggleEditing}>Edit</button>
            <div>DOB: {date_of_birth}</div>
            <div>Deceased Date: {date_of_death}</div>
            <div>Social Security Number: {ssn}</div>
            <div></div>
            <div><Address address={address} header='Address:' /></div>
            <div><Aliases editing={false} aliases={aliases}/></div>
        </div>
    );
}

Applicant.propTypes = {
    first_name: PropTypes.string,
    last_name:  PropTypes.string,
    date_of_birth:  PropTypes.string,
    date_of_death:  PropTypes.string,
    aliases: PropTypes.array,
    ssn: PropTypes.string,
    address: PropTypes.shape({
        line_one: PropTypes.string,
        city_state_zip: PropTypes.string
    }),
    modifier: PropTypes.func
}

export default Applicant;