import React from "react";
import PropTypes from 'prop-types';

function Alias(props) {
    const { name, id } = props;
    const aliasStyle = {  };

    return (
        <div className="alias" id={id} style={aliasStyle}>
            <div>{name}</div>
        </div>
    );
}

Alias.propTypes = {
    name: PropTypes.string,
    id: PropTypes.string
}

export default Alias;