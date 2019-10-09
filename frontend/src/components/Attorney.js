import React from "react";
import PropTypes from 'prop-types';

function Attorney(props) {
    const { id, full_name, address, bar_id, organization, toggleEditing } = props;
    const attorneyStyle = { display: 'grid', gridTemplateColumns: '270px 270px 270px', margin: '10px',
        border: '1px solid black', borderRadius: '15px', padding: '10px', width: '860px' };

    return (
        <div className="attorney" id={id} style={attorneyStyle}>
            <div style={{gridColumn: "1 / 3"}}>Full Name: {full_name}</div>
            <button type="button" style={{marginLeft: "20px"}} onClick={toggleEditing}>Edit</button>
            <div>Organization: {organization}</div>
            <div>Bar ID: {bar_id}</div>
            <div>Address: {address}</div>
        </div>
    );
};

Attorney.propTypes = {
    id: PropTypes.string,
    full_name: PropTypes.string,
    address: PropTypes.string,
    bar_id: PropTypes.string,
    organization: PropTypes.string,
    toggleEditing: PropTypes.func
}

export default Attorney;