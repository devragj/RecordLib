import React from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

function Defendant(props) {
    const { first_name, last_name, date_of_birth, date_of_death, aliases, ssn, address} = props;
    const name = first_name + " " + last_name;
    const defendantStyle = { display: 'grid', gridTemplateColumns: '250px 250px', margin: '15px', border: '1px solid black', borderRadius: '5px', padding: '10px', width: '900px' };

    return (
        <div className="defendant" style={defendantStyle}>
            <div>{name}</div>
            <div></div>
            <div>DOB: {date_of_birth}</div>
            <div>Deceased Date: {date_of_death}</div>
            <div>Social Security Number: {ssn}</div>
            <div>Address: {address}</div>
            <div>Aliases:
                <ul>
                    {aliases.map((alias, index) =>
                        <li key={index}> {alias} </li>
                    )}
                </ul>
            </div>
        </div>
    );
}

Defendant.propTypes = {
    first_name: PropTypes.string,
    last_name:  PropTypes.string,
    date_of_birth:  PropTypes.string,
    date_of_death:  PropTypes.string,
    aliases: PropTypes.array,
    ssn: PropTypes.string,
    address: PropTypes.string,
}

function mapStateToProps(state, ownProps) {
    return state.entities.defendant[ownProps.defendantId];
};

const DefendantWrapper = connect(mapStateToProps)(Defendant);
export default DefendantWrapper;