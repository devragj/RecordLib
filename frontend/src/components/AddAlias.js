import React, { useState }  from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addAlias } from "../actions/applicant.js";

function AddAlias(props) {
    const { adder } = props;
    const [name, setName] = useState("");

    const handleChange = event => setName(event.target.value);
    const handleClick = () => {
        adder(name);
        setName("");
    }

    return (
        <div className="addAlias" >
           <span style={{marginLeft: "20px"}}>Alias: </span>
           <input type="text" value={name} onChange={handleChange} />
           <button type="button" style={{marginLeft: "20px"}} onClick={handleClick}>Add Alias</button>
        </div>
    );
}

function mapDispatchToProps(dispatch) {
    return { adder: name => {
            dispatch(addAlias(name));
        }
    };
};

AddAlias.propTypes = {
    /**
     * The callback which adds the alias to state.
     */
    adder: PropTypes.func.isRequired
}

const AddAliasWrapper = connect(null, mapDispatchToProps)(AddAlias);
export default AddAliasWrapper;