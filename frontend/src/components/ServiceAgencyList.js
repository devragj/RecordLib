import React, { useState } from "react"
import { connect } from "react-redux"
import FormControl from "@material-ui/core/FormControl"
import InputLabel from "@material-ui/core/InputLabel"
import TextField from "@material-ui/core/TextField"
import PropTypes from 'prop-types';

import { updateServiceAgency, createNewServiceAgency } from "../actions"

/**
 * NB - ServiceAgencies in state will look like:
 *  
 * serviceAgencies: {
 *      index: [id1, id2, id3]
 *      entities: {
 *          {id1: {
 *              name: ....}}     
 *      }
 * }
 * 
 */



/**
 * List for displaying the service agencies that should receive a set of petitions. 
 * @param {} props 
 */
function ServiceAgencyList(props) {
    const { serviceAgencies, updateServiceAgency, createNewServiceAgency } = props
   
    const [needAnother, setNeedAnother] = useState(true)
    const [newServiceAgency, setNewServiceAgency] = useState(
        {
            id: "serviceAgency" + (serviceAgencies.length + 1).toString(), 
            name: ""
        })

    const handleSAEdit = (serviceAgency) => {
        return(
            () => updateServiceAgency(serviceAgency)
        )
    }


    const handleNewServiceAgencyChange = (e) => {
        setNewServiceAgency({
            name: e.target.value
        })
    }

    const handleNewServiceAgencyComplete = (e) => {
        createNewServiceAgency({
            id: e.target.id,
            name: e.target.value
        })
    }

    return(
        <div>
            {serviceAgencies.result.map(idx => {
                return(
                    <TextField 
                        id={serviceAgencies.entities[idx].id} 
                        label="Service Agency" 
                        value={serviceAgencies.entities[idx].name}
                        onChange={handleSAEdit(serviceAgencies.entities[idx])}
                        margin="normal"
                        variant="filled"/>
                )
            })}
            {
                needAnother ? 
                <TextField 
                    id={newServiceAgency.id}
                    label="Server Agency"
                    value={newServiceAgency.name}
                    onChange={handleNewServiceAgencyChange}
                    onBlur={handleNewServiceAgencyComplete} 
                    margin="normal"
                    variant="filled" /> :
                ""
            }
        </div>
    ) 
}


function mapStateToProps(state) {
    return {
        serviceAgencies: state.serviceAgencies
    }
}

function mapDispatchToProps(dispatch) {
    return {
        updateServiceAgency: (serviceAgency) => dispatch(updateServiceAgency(serviceAgency)),
        createNewServiceAgency: (serviceAgency) => dispatch(createNewServiceAgency(serviceAgency)),
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(ServiceAgencyList)