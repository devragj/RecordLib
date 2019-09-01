import React from "react";
import PropTypes from 'prop-types';

function Defendant(props) {
    const defendantStyle = {display: 'grid', gridTemplateColumns: '250px 250px', margin: '15px', border: '1px solid black', borderRadius: '5px', padding: '10px', width: '900px'};
    const { first_name, last_name, date_of_birth, date_of_death } = props
    const name = first_name + " " + last_name;

    return (
        <div className="defendant" style={defendantStyle}>
            <div>{name}</div>
            <div></div>
            <div>DOB: {date_of_birth}</div>
            <div>Deceased Date: {date_of_death}</div>

        </div>
    );
}

Defendant.propTypes = {
    first_name: PropTypes.string,
    last_name:  PropTypes.string,
    date_of_birth:  PropTypes.string,
    date_of_death:  PropTypes.string
}

export default Defendant;