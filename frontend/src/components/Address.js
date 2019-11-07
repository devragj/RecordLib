import React from "react";
import PropTypes from 'prop-types';

function Address(props) {
    const { header, address } = props;
    const addressStyle = { gridColumn: "1 / 3",  margin: '25px 0', width: '425px' };

    return (
        <div className="address" style={addressStyle}>
            <div>{header}</div>
            <div>{address.line_one}</div>
            <div>{address.city_state_zip}</div>
        </div>
    );
}

Address.propTypes = {
    header: PropTypes.string,
    address: PropTypes.shape({
        line_one: PropTypes.string,
        city_state_zip: PropTypes.string
    })
}

export default Address;